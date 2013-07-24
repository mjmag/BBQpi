#!/usr/bin/python
import time
from functions import *
from multiprocessing import Process, Manager


def BBQpi_control(control, t_plot, temp0, temp1):
    # Initialize variables.
    t = []                          # time (seconds)
    t_0 = time.time()               # initial time
    config = BBQpi_Config()

    # Read data from RaspPi, plot the data, and save the data.
    while (1):
        # Collect temperature data
        t.append(round(time.time() - t_0, 1))
        t_plot.append(t[-1] / 60)
        temp0.append(config.T0.read(config.plot_avg))
        temp1.append(config.T1.read(config.plot_avg))

        # Write results to file
        config.CSV.writerow([t[-1], temp0[-1], temp1[-1]])

        # Write message to LCD
        config.LCD.clear()
        config.LCD.message('B=%s M=%s\n' % (temp0[-1], temp1[-1]))
        config.LCD.message('IP %s' % (config.ipaddr))

        # Control switch
        if (control[0]) & (t[-1] - config.control_time >= config.control_delay):
            config.control_time = t[-1]
            if (temp1[-1] > (control[1] + config.control_tolerance)):
                config.RELAY.off()
            elif (temp1[-1] < (control[1] - config.control_tolerance)):
                config.RELAY.on()

        # Alert switch
        if (control[2]):
            # High temperature alert
            if (temp0[-1] >= control[3]) & (t[-1] - config.alert_time >= config.alert_delay):
                config.alert_time = t[-1]
                config.sendmail('Smart BBQ', 'Your meat has the desired temperature. Enjoy!')
                config.sendtweet("Your meat meat needs care! %s" % (int(t[-1])))

            # Desired temperature alert
            if (temp1[-1] >= (control[4] - config.control_tolerance)) & (t[-1] - config.alert_time >= config.alert_delay):
                config.alert_time = t[-1]
                config.sendmail('Smart BBQ', 'Your meat has the desired temperature. Enjoy!')
                config.sendtweet("Your meat is almost done %s" % (int(t[-1])))