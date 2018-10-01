#!/bin/env ipython

import casperfpga, time, struct, sys, logging, socket, datetime

#Decide where we're going to send the data, and from which addresses:
dest_ip  =192*(2**24) + 168*(2**16) + 10*(2**8) +6 
dest_port = 4011
fabric_port=60000         
source_ip= 192*(2**24) + 168*(2**16) + 10*(2**8) + 42
mac_base=(2<<40) + (2<<32)
src_mac = mac_base+source_ip
tx_core_name = 'gbe1'

pkt_period = 2**12 #how often to send another packet in FPGA clocks (200MHz)
payload_len = 1026 #how big to make each packet in 64bit words


dest_macff= 255*(2**40) + 255*(2**32) + 255*(2**24) + 255*(2**16) + 255*(2**8) + 255
arp_table = [dest_macff for i in range(256)]
arp_table1 = [0 for i in range(256)]

roach = '192.168.11.20'

print('Connecting to server %s... '%(roach)),
fpga = casperfpga.CasperFpga(host=roach,port=69)
time.sleep(1)

if fpga.is_connected():
    print 'ok\n'
else:
    print 'ERROR connecting to server %s.\n'%(roach)
    exit()
    
fpga.write_int('pkt_sim_enable', 0)
print 'done'
#fpga.write_int('pkt_sim_rid',1)
print '---------------------------'
print 'Configuring transmitter core...',
sys.stdout.flush()

device_name = tx_core_name
src_port = fabric_port
gateway=1
subnet_mask=0xffffff00
ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac, 0, gateway, source_ip, 0, 0, 0, 0, 1, src_port)
subnet_mask_pack=struct.pack('>L',subnet_mask)
arp_pack=struct.pack('>256Q',*arp_table)
fpga.blindwrite(device_name,ctrl_pack,offset=0)
fpga.blindwrite(device_name,subnet_mask_pack,offset=0x38)

print 'done'

print '---------------------------'
print 'Setting-up packet source...',
sys.stdout.flush()
fpga.write_int('pkt_sim_period',pkt_period)
fpga.write_int('pkt_sim_payload_len',payload_len)
print 'done'

print 'Setting-up destination addresses...',
sys.stdout.flush()
fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',dest_port)
print 'done'

print 'Resetting cores and counters...',
sys.stdout.flush()
fpga.write_int('rst', 3)
time.sleep(0.1)
fpga.write_int('rst', 0)
print 'done'

time.sleep(0.1)
print 'Enabling output...',
sys.stdout.flush()
fpga.write_int('pkt_sim_enable', 1)
print 'done'

