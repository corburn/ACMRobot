package main

import (
	"fmt"
	"github.com/tarm/goserial"
	"io"
	"log"
	"os"
	"os/signal"
	"strconv"
)

// Use a keyboard number pad to drive the robot. If you press a movement
// key more than once, up to five times, the robot will move faster.
//  8  Forward
// 456 Left/Stop/Right
//  2  Reverse
// 0   Reset
//
// Reset is similar to stop, except that it also moves the claw to
// it's neutral position.
//
// Example usage
//  Forward max speed: 88888<enter>
//  Reverse mid speed: 222<enter>
//  Stop:              5<enter>
func main() {
	// Beagleboard builtin leds
	log.Println("Accessing leds")
	usr0, _ := os.Open("/sys/class/leds/beagleboard::user0/brightness")
	defer usr0.Close()
	usr1, _ := os.Open("/sys/class/leds/beagleboard::user1/brightness")
	defer usr1.Close()

	usr1.Write([]byte("1"))

	// capture ctrl+c, turn off led, and exit
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		<-c
		log.Println("Captured interrupt: turnoff usr1 and exit.")
		defer usr1.Close()
		usr1.Write([]byte("0"))
		os.Exit(1)
	}()
	log.Print("Accessing controller")
	conf := &serial.Config{Name: "/dev/ttyO2", Baud: 9600}
	s, err := serial.OpenPort(conf)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Initializing")
	if err = reset(s); err != nil {
		log.Fatal(err)
	}

	// Listen for input in a separate goroutine
	log.Println("Listening for input")
	ch := make(chan string)
	go func(ch chan string) {
		var s string
		for {
			fmt.Scanf("%s", &s)
			ch <- s
		}
	}(ch)

	// Execute move commands
	left, right := 1500, 1500
	for v := range ch {
		offset := len(v) * 100
		switch v[0] {
		case '5':
			// stop
			left, right = 1500, 1500
		case '8':
			// forward
			left, right = left+offset, right+offset
		case '2':
			// reverse
			left, right = left-offset, right-offset
		case '4':
			// left
			left -= offset
			right += offset
		case '6':
			// right
			left += offset
			right -= offset
		case '0':
			reset(s)
			// skip the call to nove
			continue
		}

		// enforce limits
		if left < 1000 {
			left = 1000
		}
		if left > 2000 {
			left = 2000
		}
		if right < 1000 {
			right = 1000
		}
		if right > 2000 {
			right = 2000
		}

		log.Printf("%d %d", left, right)
		// move
		if err := move(s, left, right); err != nil {
			log.Fatal(err)
		}
	}
}

// move sends the pulse widths pw_l and pw_r to the left and right motor pairs.
// Pulse width is equivalent to speed where 1000 is full reverse, 1500 is stop,
// and 2000 is full forward.
func move(s io.ReadWriteCloser, pw_l, pw_r int) (err error) {
	log.Printf("#%sP%d#%sP%d\n", LEFT, pw_l, RIGHT, pw_r)
	_, err = s.Write([]byte("#" + LEFT + "P" + strconv.Itoa(pw_l) + "#" + RIGHT + "P" + strconv.Itoa(pw_r) + "\r"))
	return
}

// reset moves all servos to their starting position
func reset(s io.ReadWriteCloser) (err error) {
	if err = move(s, 1500, 1500); err != nil {
		return
	}
	log.Printf("#%sP1500#%sP1800#%sP2200#%sP1500#%sP600#%sP1500T5000\r", BASE, SHOULDER, ELBOW, FOREARM, WRIST, CLAW)
	if _, err = s.Write([]byte(NEUTRAL)); err != nil {
		return
	}
	return
}
