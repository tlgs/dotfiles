package main

import (
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
		return "✔️"
	case StatusFailed:
		return "❌"
	default:
		return ""
	}
}

type Result struct {
	id     string
	status Status
}

type Job struct {
	id     string
	status Status
	fails  int
}

func draw(jobs []*Job, clear bool) {
	if clear {
		for range jobs {
			fmt.Print("\x1b[A\x1b[K")
		}
	}

	for i, job := range jobs {
		fmt.Printf("%2d %v:", i+1, job.id)
		for j := 0; j < job.fails; j++ {
			fmt.Printf(" %v", StatusFailed)
		}
		fmt.Printf(" %v\n", job.status)
	}
}

func worker(queue <-chan string, feedback chan<- Result) {
	for id := range queue {
		feedback <- Result{id, StatusRunning}

		cmd := exec.Command("youtube-dl", "--no-progress", "-x", "--audio-format", "flac", "--add-metadata", id)
		err := cmd.Run()
		if err != nil {
			feedback <- Result{id, StatusFailed}
			continue
		}

		feedback <- Result{id, StatusSucceeded}
	}
}

var (
	nJobs         = flag.Int("jobs", 5, "number of concurrent downloads")
	nRetries      = flag.Int("retries", 3, "number of retries on a failed webpage")
	retryInterval = flag.Int("interval", 60, "number of seconds between retries")
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
	feedback := make(chan Result)
	for i := 0; i < *nJobs; i++ {
		go worker(queue, feedback)
	}

	// launch jobs and start status tracking
	jobs := make([]*Job, len(tracks))
	for i, t := range tracks {
		queue <- t
		jobs[i] = &Job{t, StatusQueued, 0}
	}
	draw(jobs, false)

	// control loop
	for completed := 0; completed < len(tracks); {
		result := <-feedback

		var job *Job
		for i := 0; job == nil; i++ {
			if result.id == jobs[i].id {
				job = jobs[i]
				break
			}
		}

		job.status = result.status

		switch result.status {
		case StatusSucceeded:
			completed++

		case StatusFailed:
			job.fails++

			if job.fails >= *nRetries {
				completed++
				break
			}

			job.status = StatusPending
			go func() {
				time.Sleep(time.Duration(*retryInterval) * time.Second)

				feedback <- Result{result.id, StatusQueued}
				queue <- result.id
			}()

		}

		draw(jobs, true)
	}
}
