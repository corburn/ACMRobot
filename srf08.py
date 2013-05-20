import smbus
from time import sleep

# http://www.robot-electronics.co.uk/htm/srf08tech.shtml

#SRF08 REQUIRES 5V

# Enable Ranging Mode
# 0x50 - Result in inches
# 0x51 - Result in centimeters
# 0x52 - Result in micro-seconds
# Enable Artificial Neural Network Mode
# 0x53 - Result in inches
# 0x54 - Result in centimeters
# 0x55 - Result in micro-seconds

class SRF08(object):

	def __init__(self, bus=1, address=0x70, mode=0x51):
		self.bus = smbus.SMBus(bus)
		self.address = address
		self.mode = mode
		if mode == 0x50 or mode == 0x53:
			self.units = 'in'
		if mode == 0x51 or mode == 0x54:
			self.units = 'cm'
		if mode == 0x52 or mode == 0x55:
			self.units = 'ms'

	def __str__(self):
		try:
			self.bus.write_byte_data(self.address, 0, self.mode)
			#self.bus.write_byte_data(self.address, 2, 0x00)
			#while self.bus.read_byte_data(self.address, 0) == 0xFF:
				# TODO threading
				# SRF08 will not respond while ranging. The I2C data line is pulled high
				# if nothing is driving it. Read from the software version register until
				# it stops returning 0xFF.
				#pass
			#sleep(.07)
			sleep(.5)
			#return str(self.bus.read_byte_data(self.address, 0))
			return 'Range: ' + str(self.range()) + self.units + '\n' + 'Light: ' + str(self.light())
		except IOError:
			# An IOError likely means the device is not connected or a read was attempted before
			# the ranging was complete.
			return 'IOError'

	# Returns the light level from 0 (dark) to 255 (bright)
	def light(self):
		try:
			light = self.bus.read_byte_data(self.address, 1)
			return light
		except IOError:
			return -1

	# Returns the distance to the nearest object. This can be changed
	# from 43mm to 11m by writing to the range register at location 2,
	# however, the SRF08 has a maximum range of about 6m.
	def range(self):
		try:
			high_byte = self.bus.read_byte_data(self.address, 2)
			low_byte = self.bus.read_byte_data(self.address, 3)
			distance = (high_byte << 8) + low_byte
			return distance
		except IOError:
			return -1

