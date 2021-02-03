# STARE_config

This repo contains code used to control STARE2. The following programs are the most frequently used:

start_stare_program.py - Creates the ring buffers for data, calibrates the ADCs on the FPGA, starts the program on the FPGA, starts the packet capture code from the FPGA, the real-time data reduction pipeline, the burst searching code, and modifies the header file to keep track of the time the observation was started.

start_stare_program_simple.py - Contains all the functions of start_stare_program.py but is used with only a few of the steps at once to facilitate debugging. Which steps are run are determined by which lines are commented.

stare_config.py - Starts the FPGA code.

kill_stare_program.py - Stops the real-time pipeline.

moderate_stare_program.py - Starts and stops the real-time anaysis pipeline every 5 hours.

stare_debug.py - Makes diagnostic plots of the system to check its health.
