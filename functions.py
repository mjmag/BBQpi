# =========================================
#           FUNCTION DEFINITIONS
# =========================================

import RPi.GPIO as GPIO
import csv
from numpy import median
import time
import os
from subprocess import *
from Adafruit_CharLCD import Adafruit_CharLCD
from multiprocessing import Manager
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialize variables / controller
manager = Manager()
control = manager.list([0, 0, 0, 0, 0])  # [control_switch, t_desired, alert_switch, t_high, t_done]
t_plot = manager.list([])        # time (min)
temp0 = manager.list([])         # 1st temperature
temp1 = manager.list([])         # 2nd temperature

# Initialize the large figure for the latest 500 data points.
fig, ax = plt.subplots(figsize=(6, 5))
plt.clf()
plt.axes([0.11, 0.35, 0.85, 0.6])
plt.title('BBQ Temperatures')
plt.xlabel('Time (min)')
plt.ylabel('Temperature ($^\circ$F)')

# Initialize the small figure for all the data points.
plt.axes([0.6, 0.05, 0.35, 0.20])
ax2 = plt.gca()
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)

# Plot the large figure.
large_axes = plt.axes([0.11, 0.35, 0.85, 0.6])
large_plot0, = plt.plot([0], [0], color='red', linewidth=2.0, linestyle='-', label='$T_0$')
large_plot1, = plt.plot([0], [0], color='black', linewidth=2.0, linestyle='-', label='$T_1$')
large_plot2, = plt.plot([0, 1], [control[1], control[1]], color='magenta', linewidth=2.0, linestyle='-', label='Control')
large_plot3, = plt.plot([0, 1], [control[4], control[4]], color='blue', linewidth=2.0, linestyle='-', label='Target')
plt.legend(bbox_to_anchor=(-.5, -1.15, 1, 1), ncol=2)

# Plot the small figure.
small_axes = plt.axes([0.6, 0.05, 0.35, 0.20])
small_plot0, = plt.plot([0], [0], color='red', linewidth=0.5, linestyle='-', label='$T_0$')
small_plot1, = plt.plot([0], [0], color='black', linewidth=0.5, linestyle='-', label='$T_1$')


def set_control(cmd):
    control[:] = cmd


def get_temp():
    return [temp0[-1], temp1[-1]]


def update_figure():
    # Plot limits
    tlen = len(temp1) - 1
    tlen_short = min(50, tlen) - 1
    tmin = min(temp0[1:] + temp1[1:])
    tmax = max(temp0[1:] + temp1[1:])
    tmin_short = min(temp0[-tlen_short:] + temp1[-tlen_short:])
    tmax_short = max(temp0[-tlen_short:] + temp1[-tlen_short:])

    # Update line data
    small_plot0.set_data(t_plot[-tlen_short:], temp0[-tlen_short:])
    small_plot1.set_data(t_plot[-tlen_short:], temp1[-tlen_short:])
    large_plot0.set_data(t_plot[-tlen:], temp0[-tlen:])
    large_plot1.set_data(t_plot[-tlen:], temp1[-tlen:])
    large_plot2.set_data([t_plot[-tlen], t_plot[-1]], [control[1], control[1]])
    large_plot2.set_visible(control[0])
    large_plot3.set_data([t_plot[-tlen], t_plot[-1]], [control[4], control[4]])
    large_plot3.set_visible(control[2])

    # Update the limits
    small_axes.axis([t_plot[-tlen_short], t_plot[-1], tmin_short - 5, tmax_short + 5])
    large_axes.axis([t_plot[0], t_plot[-1], tmin - 5, tmax + 5])
    plt.draw()

    # save the latest figure to a file 'plot.png'.
    fig.savefig('./static/plot.png')


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


class BBQpi_Config():
    def __init__(self):
        # Configuration
        self.pins_T0 = 3             # chip select pin for 1st thermocouple
        self.pins_T1 = 5             # chip select pin for 2nd thermocouple
        self.pins_out = 11           # output pin
        self.pins_clock = 7          # clock pin
        self.pins_relay = 24         # relay switch pin

        self.plot_avg = 5            # number of temp readings to be averaged

        self.control_time = 0        # initialize control time
        self.control_delay = 35      # control delay in second
        self.control_tolerance = 2   # tolerance

        self.alert_delay = 60       # alert delay in seconds
        self.alert_time = 0         # initialize alert time
        self.alert_email = '5107177937@smtext.com'   # Send message to email/smtp

        self.out_temp = 'temp.csv'          # output file name for temperature data
        self.out_control = 'control.csv'    # input file name for control parameters

        self.network_cmd0 = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        self.network_cmd1 = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
        self.network_smtp = ['rp.smartbbq@gmail.com', '030206raspberrypi']
        self.network_tweet = "/usr/local/bin/twitter -erp.smartbbq@gmail.com set "

        #Initialize components:
        self.LCD = Adafruit_CharLCD()
        self.LCD.begin(16, 1)
        self.RELAY = BBQpi_relay(self.pins_relay)
        self.T0 = BBQpi_thermocouple(self.pins_T0, self.pins_out, self.pins_clock)
        self.T1 = BBQpi_thermocouple(self.pins_T1, self.pins_out, self.pins_clock)

        # Initialize output files
        if os.path.isfile(self.out_temp):
            os.remove(self.out_temp)
        self.f = open(self.out_temp, 'wb')
        self.CSV = csv.writer(self.f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # Find the devices IP Address
        self.ipaddr = ''
        try:
            self.ipaddr = run_cmd(self.network_cmd0)
        except:
            pass
        if (self.ipaddr == ''):
            self.ipaddr = run_cmd(self.network_cmd1)

    def sendmail(self, header, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.network_smtp[0], self.network_smtp[1])
        server.sendmail(header, self.alert_email, message)

    def sendtweet(self, message):
        print "trying to send a tweet!"
        tweetcommand = self.network_tweet + message
        subprocess.call(tweetcommand, shell=True)


class BBQpi_relay():
    def __init__(self, pin):
        self.pin = pin
        self.relay = GPIO
        self.relay.setmode(GPIO.BOARD)
        self.relay.setwarnings(False)
        self.relay.setup(self.pin, GPIO.OUT)

    def off(self):
        self.relay.output(self.pin, 0)

    def on(self):
        self.relay.output(self.pin, 1)


class BBQpi_thermocouple():
    def __init__(self, pin_tc, pin_out, pin_clock):
        self.tc = pin_tc
        self.out = pin_out
        self.clock = pin_clock
        self.thermocouple = GPIO
        self.thermocouple.setmode(GPIO.BOARD)
        self.thermocouple.setup(pin_tc, GPIO.OUT)
        self.thermocouple.setup(pin_out, GPIO.IN)
        self.thermocouple.setup(pin_clock, GPIO.OUT)

    def read(self, length=1):
        tmp = []
        for ii in range(0, length):
            self.thermocouple.output(self.tc, 0)
            time.sleep(.002)
            self.thermocouple.output(self.tc, 1)
            time.sleep(.220)

            self.thermocouple.output(self.tc, 0)
            self.thermocouple.output(self.clock, 1)
            time.sleep(.001)
            self.thermocouple.output(self.clock, 0)

            value = 0
            for jj in range(11, -1, -1):
                self.thermocouple.output(self.clock, 1)
                value += (self.thermocouple.input(self.out) << jj)
                self.thermocouple.output(self.clock, 0)

            self.thermocouple.output(self.clock, 1)
            error_tc = self.thermocouple.input(self.out)
            self.thermocouple.output(self.clock, 0)

            for jj in range(0, 2):
                self.thermocouple.output(self.clock, 1)
                time.sleep(.001)
                self.thermocouple.output(self.clock, 0)
            self.thermocouple.output(self.tc, 1)

            if (error_tc == 0):
                tmp.append((value * 0.25) * 9.0 / 5.0 + 32.0)

        return round(median(tmp), 1)