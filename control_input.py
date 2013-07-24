#!/usr/bin/python
import inmeth
import web
from functions import *
from multiprocessing import Process
from temp_control import BBQpi_control


if __name__ == "__main__":
    # Initialize the control system / plotter
    control_thread = Process(target=BBQpi_control, args=(control, t_plot, temp0, temp1))
    control_thread.start()

    # Initialize web server
    web.internalerror = web.debugerror
    inmeth.app.run()
