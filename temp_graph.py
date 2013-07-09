#!/usr/bin/python
# =========================================
#                 BEGIN
# =========================================

# =========================================
#             INITIALIZATIONS
# =========================================

# import other necessary libraries.
import functions
import matplotlib
import csv


# declare variables.
OUTPUT_NAME = 'temp.csv'

# initialize 'matplotlib'.
matplotlib.use('Agg')
matplotlib.rcParams['timezone'] = 'US/Pacific'  # Replace with your favorite time zone
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# initialize the large figure for the latest 500 data points.
fig, ax = plt.subplots(figsize=(6,5))
plt.clf()
plt.axes([0.11, 0.10, 0.85, 0.85])
plt.title('BARBEQUE TEMPERATURES')
plt.xlabel('Time (min)')
plt.ylabel('Temperature ($^\circ$F)')

# initialize the small figure for all the data points.
plt.axes([0.65, 0.15, 0.25, 0.20])
ax2 = plt.gca()
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)

# =========================================
#        PLOT TEMPERATURE HISTORIES
# =========================================

# read data from 'temp.csv' and plot the data.
while 1 == 1 :

    # initialize variables.
    t     = []
    temp0 = []
    temp1 = []

    # read the data file.
    f = open(OUTPUT_NAME,'rb')
    input = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    temp_data = [[item for number, item in enumerate(row) if item and (0 <= number <= 2)] for row in input]
    for i in range(len(temp_data)):
        if i == 0:
            t.append(0);
            temp0.append(temp_data[i][0]);
            temp1.append(temp_data[i][1]);
        else:
            t.append(temp_data[i][0]);
            temp0.append(temp_data[i][1]);
            temp1.append(temp_data[i][2]);
    f.close()

    # print data
   # print t[-1], temp0[-1], temp1[-1]

    # data for the large figure.
    t_p1 = [ x / 60 for x in t[max(-len(t[:]), -50):] ] 
    temp0_p1 = temp0[max(-len(temp0[:]), -50):]
    temp1_p1 = temp1[max(-len(temp1[:]), -50):]
    
    # plot the large figure.
    plt.axes([0.11, 0.10, 0.85, 0.85])
    if len(t_p1) > 1:
        plt.plot(t_p1, temp0_p1, color='red', linewidth=2.0, linestyle='-', label='$T_0$') 
        plt.plot(t_p1, temp1_p1, color='black', linewidth=2.0, linestyle='-', label='$T_1$')
        plt.axis([min(t_p1), max(t_p1), min(functions.merge([temp0_p1, temp1_p1])) - 10, max(functions.merge([temp0_p1, temp1_p1])) + 10])
        if len(t_p1) == 2:
            plt.legend(loc='upper right')
    
    # data for the small figure.
    t_p2 = [ x / 60 for x in t[:] ]
    
    # plot the small figure.
    plt.axes([0.65, 0.15, 0.25, 0.20])
    if len(t_p2) > 1:
        plt.plot(t_p2, temp0, color='red', linewidth=0.5, linestyle='-', label='$T_0$') 
        plt.plot(t_p2, temp1, color='black', linewidth=0.5, linestyle='-', label='$T_1$')
        plt.axis([min(t_p2), max(t_p2), min(functions.merge([temp0, temp1])) - 10, max(functions.merge([temp0, temp1])) + 10])
    
    # save the latest figure to a file 'plot.png'.
    fig.savefig('./static/plot.png')

    # delete temporary variables.
    del t, temp0, temp1

    # uncomment to enable extra delay
    # time.sleep()
