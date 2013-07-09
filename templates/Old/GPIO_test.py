# import other necessary libraries.
import RPi.GPIO as GPIO
import MAX6675_GPIO as MAX6675
import functions

# GPIO BCM Pin Convention.
CS0      = 27            # chip select pin for 1st thermocouple
CS1      = 22            # chip select pin for 2nd thermocouple
SO       = 18            # output pin
SCK      = 17            # clock pin
RelayPin = 23            # relay switch pin

units    = 2            # degree Fahrenheit
size     = 5            # number of temp readings to be averaged

# initialize variables.
t     = []          # time
temp0 = []          # 1st temperature
temp1 = []          # 2nd temperature

# # initialize 'wiringpi'.
# wiringpi.wiringPiSetup()

# initialize 'GPIO'.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# read data from RaspPi, plot the data, and save the data.                              # current time round to 1 decimal
temp0.append( round( functions.readTemp(CS0,SO,SCK,units,size), 1 ) )   # current temperatures round to 1 decimal.
temp1.append( round( functions.readTemp(CS1,SO,SCK,units,size), 1 ) )

print temp0[-1], temp1[-1]
