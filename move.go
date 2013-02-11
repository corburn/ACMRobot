package main

import (
	"github.com/tarm/goserial"
	"log"
	"time"
)

func main() {
	c := &serial.Config{Name: "/dev/ttyO2", Baud: 9600}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}

	n, err := s.Write([]byte("#16P1700#17P1700\r"))
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	n, err = s.Write([]byte("#16P1300#17P1300\r"))
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	n, err = s.Write([]byte("#16P1500#17P1500\r"))
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	n, err = s.Write([]byte("#16P1300#17P1700\r"))
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	n, err = s.Write([]byte("#16P1700#17P1300\r"))
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(2 * time.Second)

	n, err = s.Write([]byte("#16P1500#17P1500\r"))
	if err != nil {
		log.Fatal(err)
	}

	/*
	   buf := make([]byte, 128)
	   n, err = s.Read(buf)
	   if err != nil {
	           log.Fatal(err)
	   }
	   log.Print("%q", buf[:n])
	*/
	log.Print("%d", n)
}
