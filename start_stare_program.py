import os
from casperfpga import CasperFpga
import numpy as np,struct,time,datetime,sys,socket,os
from astropy.time import Time
import subprocess

os.system("/home/user/destroy_dada_buffer.sh")
os.system("/home/user/create_dada_buffer.sh")
myfpga = CasperFpga(host='192.168.11.20', port=69)
#myfpga.upload_to_ram_and_program('/home/user/casper/stare_v1_mb_dp/top.bin')
myfpga.transport.progdev(addr=0x800000)
#os.system("python /home/user/casper/adc16/adc16_init.py -s -d 2 -g 4 192.168.11.20 test.bof")
calibrated = False
while calibrated == False:
	out = subprocess.Popen(["python", "/home/user/casper/adc16/adc16_init.py", "-s", "-d 2", "-g 4", "192.168.11.20", "test.bof"],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	message = out.communicate()[0]
	print(message)
	if 'ERROR' not in message and 'bitslipping' not in message and 'chip c' in message and 'chip b' in message:
		print "Successfully calibrated the ADCs."
		calibrated = True
	else:
		print "ADC calibration failed, retrying."
started = False
while started == False:
	out2 = subprocess.Popen(["python", "/home/user/stare/stare_config.py"], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	message2 = out2.communicate()[0]
	print message2
	if 'ERROR' not in message2:
		print "Started STARE program"
		started = True
	else:
		print "Failed to start STARE program, retrying"
subprocess.Popen("dsaX_spectrometer_reorder",shell=True)
subprocess.Popen("/home/user/linux_64/heimdall/Applications/heimdall -gpu_id 0 -nsamps_gulp 100000 -k eada -dm 5 2000 -output_dir /home/user/cand_times_sync -v", shell=True)
subprocess.Popen("/home/user/dsa_code/dsaX_dsa5/src/dsaX_spectrometer_udpdb_thread -f /home/user/cand_times_sync/header_2.txt -k dada -p 4010 -n 1 -i 192.168.10.6 ",shell=True)
