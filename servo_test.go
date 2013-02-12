package main

import (
	"github.com/tarm/goserial"
	"testing"
	"time"
)

func TestMotors(t *testing.T) {
	c := &serial.Config{Name: "/dev/ttyO2", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
		t.Fatal(err)
	}

	_, err = s.Write([]byte("#16P1700#17P1700\r"))
	if err != nil {
		t.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	_, err = s.Write([]byte("#16P1300#17P1300\r"))
	if err != nil {
		t.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	_, err = s.Write([]byte("#16P1500#17P1500\r"))
	if err != nil {
		t.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	_, err = s.Write([]byte("#16P1300#17P1700\r"))
	if err != nil {
		t.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	_, err = s.Write([]byte("#16P1700#17P1300\r"))
	if err != nil {
		t.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	_, err = s.Write([]byte("#16P1500#17P1500\r"))
	if err != nil {
		t.Fatal(err)
	}

	s.Close()
}
