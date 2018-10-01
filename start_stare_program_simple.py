import os
from casperfpga import CasperFpga
import numpy as np,struct,time,datetime,sys,socket,os
from astropy.time import Time
import subprocess

"""os.system("/home/user/destroy_dada_buffer.sh")
os.system("/home/user/create_dada_buffer.sh")
subprocess.Popen("/home/user/dsa_code/dsaX_dsa5/src/dsaX_spectrometer_reorder",shell=True)
print 0
subprocess.Popen("heimdall -k eada -dm 0 2000", shell=True)
print 1"""
myfpga = CasperFpga(host='192.168.11.20', port=69)
print "Hi"
#os.system("python /home/user/casper/adc16/adc16_init.py -s -d 2 192.168.11.20 test.bof")
#myfpga.upload_to_ram_and_program('/home/user/casper/stare_v2_mb_dp/top.bin')
myfpga.transport.progdev(addr=0x800000)
os.system("python /home/user/casper/adc16/adc16_init.py -s -d 2 -g 4 192.168.11.20 test.bof")
#os.system("python /home/user/stare/stare_config.py")
#os.system("python /home/user/stare/stare_config.py")
"""subprocess.Popen("/home/user/dsa_code/dsaX_dsa5/src/dsaX_spectrometer_udpdb_thread -f /home/user/dada_header/header_2.txt -k dada -p 4010 -n 1 -i 192.168.10.6 -v",shell=True)
print Time(datetime.datetime.now()).mjd"""
