import fcntl
import socket
import struct
import os
import socket

class Lan(object):

	def __init__(self):
		#self.lan = 1
		self.lan = self.get_lan()

	def __str__(self):
		return str(self.lan)

	def __repr__(self):
		return self.str()

	#def getExternalIP(self):
	#    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#    sock.connect(('google.com', 80))
	#    ip = sock.getsockname()[0]
	#    sock.close()
	#    return ip

	def getHost(self):
		return socket.gethostname()

	def get_interface(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
			ifname[:15]))[20:24])

	#def get_lan():
	#	return ([ip for ip in socket.gethostbyname_ex(socket.gethostname()) if not ip.startswith("127.")][:1])

	def wan(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("google.com",80))
		return s.getsockname()

	def get_lan(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			eth0 = socket.inet_ntoa(fcntl.ioctl(
				s.fileno(),
				0x8915,  # SIOCGIFADDR
				struct.pack('256s', 'eth0')
			)[20:24])
		except IOError:
			eth0 = 'eth0 null'
		try:
			wlan0 = socket.inet_ntoa(fcntl.ioctl(
				s.fileno(),
				0x8915,  # SIOCGIFADDR
				struct.pack('256s', 'wlan0')
			)[20:24])
		except IOError:
			wlan0 = 'wlan0 null'
		return eth0 + '\n' + wlan0

	def refresh(self):
		#self.lan = self.lan + 1#self.lan()
		self.lan = self.get_lan()

