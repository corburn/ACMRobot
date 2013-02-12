package main

// Servo pin layout
const (
	BASE     = "0"
	SHOULDER = "1"
	ELBOW    = "2"
	FOREARM  = "3"
	WRIST    = "4"
	CLAW     = "5"
	LEFT     = "16"
	RIGHT    = "17"
)

// Claw positions
const (
	NEUTRAL  = "#" + BASE + "P1500#" + SHOULDER + "P1800#" + ELBOW + "P2200#" + FOREARM + "P1500#" + WRIST + "P600#" + CLAW + "P1500T5000\r"
)
