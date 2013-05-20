#!/usr/bin/python

import network
import os
import srf08
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate


class LcdPlate(Adafruit_CharLCDPlate):
	SELECT = 1
	RIGHT = 2
	DOWN = 4
	UP = 8
	LEFT = 16

	def __init__(self):
		# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
		# pass '0' for early 256 MB Model B boards or '1' for all later versions
		super(LcdPlate, self).__init__(busnum=1)

		# TODO Turnoff the display when the computer shutsdown
		# Turn off the display when the program exits
		import atexit
		atexit.register(self.stop)

		self.lan = network.Lan()
		self.srf08 = srf08.SRF08()

	def listen(self):
		# TODO: Compass action
		# Menu items and the functions they trigger when selected
		menu = [[[self.lan, self.lan.refresh], ['Reboot', self.reboot],['Shutdown', self.shutdown]],
				[['Range Finder', self.range_finder],['Compass', None]]]
		main = 0
		sub = 0

		# Debounce buttons by comparing the current value to the previous value.
		prev = -1
		while True:
			button = self.buttons()
			if button is not prev:
				# Select menu item
				if button is self.LEFT:
					sub -= 1
				if button is self.RIGHT:
					sub += 1
				if button is self.UP:
					main -= 1
				if button is self.DOWN:
					main += 1
				# Call menu item function
				if button is self.SELECT:
					menu[main][sub][1]()

				# TODO: Find index out of bounds error
				# Index wrapping
				if main < 0:
					main = len(menu)-1
				if main >= len(menu):
					main = 0
				if sub < 0:
					sub = len(menu[main])-1
				if sub >= len(menu[main]):
					sub = 0

				# Display menu item
				self.clear()
				self.message(menu[main][sub][0])
				prev = button

	def range_finder(self):
		# Display light and range value until an arrow key is pressed.
		# The interface is unresponsive while ranging so the button may need to be held.
		while self.buttons() not in [self.LEFT, self.RIGHT, self.UP, self.DOWN]:
			# Range before the screen is cleared so that the old value will be displayed while
			# waiting for the new value. If placed after, the screen will be cleared as soon as
			# it's displayed.
			r = str(self.srf08)
			self.clear()
			self.message(r)

	def reboot(self):
		os.system('reboot')

	def shutdown(self):
		os.system('shutdown -h now')

plate = LcdPlate()
try:
	plate.listen()
except KeyboardInterrupt:
	raise KeyboardInterrupt
