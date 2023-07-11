// Wrapper around youtube-dl to implement concurrent and _fault-tolerant_
// download of music from an Youtube playlist.

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

type Status uint8

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

type View struct {
	Status  Status
	Message string
}

func draw(views []*View, completed int, clear bool) {
	if clear {
		for i := 0; i < len(views)+1; i++ {
			fmt.Print("\x1b[A\x1b[K") // up one, clear line
		}
	}

	fmt.Printf("Completed: %v/%v\n", completed, len(views))

	for _, job := range views {
		msg := []rune(job.Message)
		if len(msg) > 78 {
			msg = append(msg[:77], '…')
		}

		fmt.Printf("%v %v\n", job.Status, string(msg))
	}
}

type Update struct {
	Id string
	View
}

func worker(queue <-chan string, updates chan<- Update) {
	for id := range queue {
		cmd := exec.Command("yt-dlp", "--no-progress", "-x", "--audio-format", "flac", "--add-metadata", "--", id)

		r, err := cmd.StdoutPipe()
		if err != nil {
			updates <- Update{id, View{StatusFailed, err.Error()}}
			continue
		}
		cmd.Stderr = cmd.Stdout

		err = cmd.Start()
		if err != nil {
			updates <- Update{id, View{StatusFailed, err.Error()}}
			continue
		}

		updates <- Update{id, View{StatusRunning, ""}}

		scanner := bufio.NewScanner(r)
		for scanner.Scan() {
			updates <- Update{id, View{StatusRunning, scanner.Text()}}
		}

		err = cmd.Wait()
		if err != nil {
			updates <- Update{id, View{StatusFailed, err.Error()}}
			continue
		}

		updates <- Update{id, View{StatusSucceeded, ""}}
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
	raw, err := exec.Command("yt-dlp", "--get-id", playlist).Output()
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
	updates := make(chan Update)
	for i := 0; i < *nJobs; i++ {
		go worker(queue, updates)
	}

	// launch jobs and start status tracking
	jobs := make(map[string]*View, len(tracks))
	failures := make(map[string]int, len(tracks))
	views := make([]*View, len(tracks))
	for i, t := range tracks {
		queue <- t
		jobs[t] = &View{StatusQueued, "…"}
		failures[t] = 0
		views[i] = jobs[t]
	}
	draw(views, 0, false)

	// control loop
	for completed := 0; completed < len(tracks); {
		update := <-updates
		id := update.Id

		job := jobs[id]
		job.Status = update.Status
		if update.Message != "" {
			job.Message = update.Message
		}

		switch update.Status {
		case StatusSucceeded:
			completed++

		case StatusFailed:
			failures[id]++
			if failures[id] > *nRetries {
				completed++
				break
			}

			job.Status = StatusPending
			time.AfterFunc(
				time.Duration(*retryInterval)*time.Second,
				func() {
					queue <- id
					updates <- Update{id, View{StatusQueued, ""}}
				},
			)
		}

		draw(views, completed, true)
	}
}
