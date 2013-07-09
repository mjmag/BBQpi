import wiringpi
import time

def readTemp(CS_pin, SO_pin, SCK_pin, units):

	value    = 0
	error_tc = 0
	temp     = 0.0

	wiringpi.digitalWrite(CS_pin,0)
	time.sleep(.002)
	wiringpi.digitalWrite(CS_pin,1)
	time.sleep(.220)
	
	wiringpi.digitalWrite(CS_pin,0)
	
	wiringpi.digitalWrite(SCK_pin,1)
	time.sleep(.001)
	wiringpi.digitalWrite(SCK_pin,0)
	
	for i in range(11, -1, -1):
		wiringpi.digitalWrite(SCK_pin,1)
		value = value + (wiringpi.digitalRead(SO_pin) << i)
		wiringpi.digitalWrite(SCK_pin,0)

	wiringpi.digitalWrite(SCK_pin,1)
	error_tc = wiringpi.digitalRead(SO_pin)
	wiringpi.digitalWrite(SCK_pin,0)
	
	for i in range(1, -1, -1):
		wiringpi.digitalWrite(SCK_pin,1)
		time.sleep(.001)
		wiringpi.digitalWrite(SCK_pin,0)
		
	wiringpi.digitalWrite(CS_pin, 1)
	
	if units == 2:
		temp = (value*0.25) * 9.0/5.0 + 32.0
	elif units == 1:
		temp = (value*0.25)
	else:
		temp = value
	
	if error_tc != 0:
		return -CS_pin
	else:
		return temp
	
# wiringpi.wiringPiSetup()

# CS0 = 2
# CS1 = 3
# SO = 1
# SCK = 0
# units = 2

# tempdata = readdata(CS0,SO,SCK,units)

# print 'T = ', tempdata, 'degree F'