// Wrapper around youtube-dl to implement concurrent and _fault-tolerant_
// download of music from an Youtube playlist.
//
// Makes use of the [worker pool](https://gobyexample.com/worker-pools) pattern, and
// the control loop implements a simple state machine:
//
//     +---------+     +--------+     +---------+     +-----------+
// --->| Pending +---->| Queued +---->| Running +---->| Succeeded |
//     +---------+     +--------+     +----+----+     +-----------+
//     	    ^                              |
//     	    |                              |
//     	    |          +--------+          |
//     	     '---------+ Failed |<--------'
//                     +--------+

package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

type Status int

const (
	StatusPending Status = iota
	StatusQueued
	StatusRunning
	StatusSucceeded
	StatusFailed
)

func (s Status) String() string {
	switch s {
	case StatusPending:
		return "💤"
	case StatusQueued:
		return "📬"
	case StatusRunning:
		return "🚀"
	case StatusSucceeded:
		return "💯"
	case StatusFailed:
		return "💣"
	default:
		return ""
	}
}

type Job struct {
	Id       string
	Status   Status
	Failures int
	Tail     string
}

func draw(jobs []*Job, clear bool) {
	if clear {
		for range jobs {
			fmt.Print("\x1b[A\x1b[K") // up one, clear line
		}
	}

	for i, job := range jobs {
		var msg string
		if len(job.Tail) > 74 {
			msg = job.Tail[:71] + "..."
		} else {
			msg = job.Tail
		}

		fmt.Printf("%2d: %v %v\n", i+1, job.Status, msg)
	}
}

type Log struct {
	Id      string
	Message string
}

type Result struct {
	Id     string
	Status Status
}

func worker(queue <-chan string, logs chan<- Log, results chan<- Result) {
	for id := range queue {
		cmd := exec.Command("youtube-dl", "--no-progress", "-x", "--audio-format", "flac", "--add-metadata", "--", id)

		r, err := cmd.StdoutPipe()
		if err != nil {
			results <- Result{id, StatusFailed}
			continue
		}
		cmd.Stderr = cmd.Stdout

		err = cmd.Start()
		if err != nil {
			results <- Result{id, StatusFailed}
			continue
		}

		results <- Result{id, StatusRunning}

		scanner := bufio.NewScanner(r)
		for scanner.Scan() {
			logs <- Log{id, scanner.Text()}
		}

		err = cmd.Wait()
		if err != nil {
			results <- Result{id, StatusFailed}
			continue
		}

		results <- Result{id, StatusSucceeded}
	}
}

var (
	nJobs         = flag.Int("jobs", 5, "number of concurrent downloads")
	nRetries      = flag.Int("retries", 2, "number of retries to perform")
	retryInterval = flag.Int("interval", 30, "number of seconds to wait between retries")
)

func main() {
	flag.Parse()

	playlist := flag.Arg(0)
	if playlist == "" {
		fmt.Fprintln(os.Stderr, "missing playlist id")
		os.Exit(1)
	}

	// get list of tracks to download
	raw, err := exec.Command("youtube-dl", "--get-id", playlist).Output()
	if err != nil {
		fmt.Fprintln(os.Stderr, "error: failed to retrieve individual track ids")

		exErr := err.(*exec.ExitError)
		trimmedErr := strings.Trim(string(exErr.Stderr), "\n")
		for _, s := range strings.Split(trimmedErr, "\n") {
			fmt.Fprintln(os.Stderr, "  ↳", s)
		}

		os.Exit(1)
	}
	trimmed := strings.Trim(string(raw), "\n")
	tracks := strings.Split(trimmed, "\n")

	// launch workers
	queue := make(chan string, len(tracks))
	logs := make(chan Log)
	results := make(chan Result)
	for i := 0; i < *nJobs; i++ {
		go worker(queue, logs, results)
	}

	// launch jobs and start status tracking
	jobs := make([]*Job, len(tracks))
	idx := make(map[string]int)
	for i, t := range tracks {
		queue <- t

		jobs[i] = &Job{Id: t, Status: StatusQueued}
		idx[t] = i
	}
	draw(jobs, false)

	// control loop
	for completed := 0; completed < len(tracks); {
		select {
		case log := <-logs:
			job := jobs[idx[log.Id]]
			job.Tail = log.Message

		case result := <-results:
			job := jobs[idx[result.Id]]
			job.Status = result.Status

			switch result.Status {
			case StatusSucceeded:
				completed++

			case StatusFailed:
				job.Failures++
				if job.Failures > *nRetries {
					completed++
					break
				}

				job.Status = StatusPending
				go func() {
					time.Sleep(time.Duration(*retryInterval) * time.Second)

					queue <- result.Id
					results <- Result{result.Id, StatusQueued}
				}()
			}
		}

		draw(jobs, true)
	}
}
