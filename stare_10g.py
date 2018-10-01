import numpy as np,struct,time,datetime,sys,socket,os
import matplotlib.pyplot as plt
from casperfpga import CasperFpga

fpga = CasperFpga(host='192.168.11.20')
time.sleep(0.2)
        
# arp table stuff
dest_macff= 255*(2**40) + 255*(2**32) + 255*(2**24) + 255*(2**16) + 255*(2**8) + 255 
arp_table = [dest_macff for i in range(256)]

src_ip_base = 192*(2**24) + 168*(2**16) + 11*(2**8) + 20
src_port = 4002 

gateway=1
device_name='gbe0_gbe0'
subnet_mask=0xffffff00
src_mac = 0*2**40+18*2**32+203*2**24+20*2**16+22*2**8+4
ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac, 0, gateway, src_ip_base, 0, 0, 0, 0, 1, src_port)
subnet_mask_pack=struct.pack('>L',subnet_mask)
arp_pack=struct.pack('>256Q',*arp_table)
fpga.blindwrite(device_name,subnet_mask_pack,offset=0x38)
fpga.write(device_name,arp_pack,offset=0x3000)
fpga.blindwrite(device_name,ctrl_pack,offset=0)

ctrl_read = fpga.read('gbe0_gbe0',0x3b)
#print (ctrl_pack,16)
#print (ctrl_read,16)
print (ctrl_pack,16)
print (ctrl_read,16)


