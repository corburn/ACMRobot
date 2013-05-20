#!/usr/bin/env python3                                                                          

from quick2wire.i2c import I2CMaster, writing_bytes, reading                  
import time                                                                   

address = 0x21  # found using `sudo i2cdetect -y 0`                                                         
cmd = 0x41  # 'A' means read                                                     

with I2CMaster() as master:                                                   

	while True:                                                               
		try:
			master.transaction(writing_bytes(address, cmd))                       
			raw_bytes = master.transaction(reading(address, 2))[0]                
			#Shift the first byte up by 8 bits and add it to the second
			#The result is in 10ths of degrees, so divide by 10 to get
			#degrees.
			heading = (raw_bytes[0] * 2**8 + raw_bytes[1]) / 10                   
			print(heading)                                                        
		except IOError:
			print(-1)

		time.sleep(.2)
