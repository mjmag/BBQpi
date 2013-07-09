# import wiringpi
import RPi.GPIO as GPIO
import time

def readTemp(CS_pin, SO_pin, SCK_pin, units):

	value    = 0
	error_tc = 0
	temp     = 0.0

	GPIO.setup(CS_pin, GPIO.OUT)
	GPIO.setup(SO_pin, GPIO.IN)
	GPIO.setup(SCK_pin, GPIO.OUT)
	
# 	GPIO.input(channel)
# 	GPIO.output(channel, state)
	
	GPIO.output(CS_pin,0)
	time.sleep(.002)
	GPIO.output(CS_pin,1)
	time.sleep(.220)
	
	GPIO.output(CS_pin,0)
	
	GPIO.output(SCK_pin,1)
	time.sleep(.001)
	GPIO.output(SCK_pin,0)
	
	for i in range(11, -1, -1):
		GPIO.output(SCK_pin,1)
		value = value + (GPIO.input(SO_pin) << i)
		GPIO.output(SCK_pin,0)

	GPIO.output(SCK_pin,1)
	error_tc = GPIO.input(SO_pin)
	GPIO.output(SCK_pin,0)
	
	for i in range(1, -1, -1):
		GPIO.output(SCK_pin,1)
		time.sleep(.001)
		GPIO.output(SCK_pin,0)
		
	GPIO.output(CS_pin, 1)
	
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
	GPIO.cleanup()