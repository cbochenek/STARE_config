import numpy as np,struct,time,datetime,sys,socket,os
import matplotlib.pyplot as plt
from casperfpga import CasperFpga
from astropy.time import Time

#os.system("python ~/snap/adc16/adc16_init.py 192.168.1.151 stare_v1.bof -d 2 -g 5")
fpga = CasperFpga(host='192.168.11.20')
time.sleep(0.2)
        
#print 'connected to FPGA ',fpga,', with est clock',fpga.estimate_fpga_clock()

# snap defaults

# arp table stuff
mac_base0 = (2<<40) + (2<<32)
dest_macff= 255*(2**40) + 255*(2**32) + 255*(2**24) + 255*(2**16) + 255*(2**8) + 255 
arp_table = [dest_macff for i in range(256)]
arp_table1 = [0 for i in range(256)]

# defaults for snap-side
src_ip_base = 192*(2**24) + 168*(2**16) + 10*(2**8) + 20
src_port = 4001
#src_ip_base2 = 192*(2**24) + 168*(2**16) + 11*(2**8) + 20
#src_port2 = 4002 

dest_ip = 192*(2**24) + 168*(2**16) + 10*(2**8) + 6 
#dest_ip2 = 192*(2**24) + 168*(2**16) + 11*(2**8) + 6
#dest_mac_a = 40175247655024 # 24:8a:07:5d:80:70 // ens6 on dsamaster
#dest_mac_a = 40175247654496 # 24:8a:07:5d:7e:60 // ens6 on dsa1
#dest_mac_b = 137432781157264 # ens6 on dsa2
#dest_mac_c = 137432781157248 # ens6 on dsa3
#dest_mac_d = 137432781168272 # ens6 on dsa4
#dest_mac_e = 40175247654464 # ens6 on dsa5

#dest_mac1 = 40175247654465 # ens6d1 on dsa5

dest_port = 4010
#dest_port2=4011
src_mac = mac_base0+src_ip_base
#src_mac2 = mac_base0+src_ip_base2

#arp_table[6] = src_mac
#arp_table[1] = dest_mac_a
#arp_table[2] = dest_mac_b
#arp_table[3] = dest_mac_c
#arp_table[4] = dest_mac_d
#arp_table[5] = dest_mac_e
#arp_table1[2] = src_mac1
#arp_table1[1] = dest_mac1


# raw data flow
#fpga.config_10gbe_core('eth1_gbe1',src_mac, src_ip_base, src_port, arp_table)
gateway=1
device_name='gbe1_gbe1'
subnet_mask=0xffffff00
ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac, 0, gateway, src_ip_base, 0, 0, 0, 0, 1, src_port)
subnet_mask_pack=struct.pack('>L',subnet_mask)
arp_pack=struct.pack('>256Q',*arp_table)
fpga.blindwrite(device_name,ctrl_pack,offset=0)
fpga.blindwrite(device_name,subnet_mask_pack,offset=0x38)
fpga.write(device_name,arp_pack,offset=0x3000)
#fpga.write(device_name,arp_pack,offset=0x90)
"""
gateway1=1
device_name1='gbe0_gbe0'
subnet_mask1=0xffffff00
src_mac2 = 0*2**40+18*2**32+203*2**24+20*2**16+22*2**8+4
ctrl_pack1=struct.pack('>QLLLLLLBBH',src_mac2, 0, gateway1, src_ip_base2, 0, 0, 0, 0, 1, src_port2)
subnet_mask_pack1=struct.pack('>L',subnet_mask1)
arp_pack1=struct.pack('>256Q',*arp_table)
fpga.blindwrite(device_name1,subnet_mask_pack1,offset=0x38)
fpga.write(device_name1,arp_pack1,offset=0x3000)
fpga.blindwrite(device_name1,ctrl_pack1,offset=0)
"""
time.sleep(3)
#print fpga.print_10gbe_core_details('gbe1_gbe1')


# write stuff to registers
fpga.write_int('acc_len',15);
#fpga.write_int('acc_len',8191)
fpga.write_int('fft_shift',1023);
fpga.write_int('port1',dest_port);
#fpga.write_int('port2',dest_port2);
fpga.write_int('ip1',dest_ip);
#fpga.write_int('ip2',dest_ip2);

# set reset for 10g
fpga.write_int('gbe1_ctrl',1);
time.sleep(0.1)
fpga.write_int('gbe1_ctrl',0);
time.sleep(0.1)
#fpga.write_int('gbe0_ctrl',1);
#time.sleep(0.1)
#fpga.write_int('gbe0_ctrl',0);
#time.sleep(0.1)

print 'All ready to go!'

#print 'connected to FPGA ',fpga,', with est clock',fpga.est_brd_clk()
    
#fpga.write_int('adc_snap_ctrl',3)
#time.sleep(0.1)
#fpga.write_int('adc_snap_ctrl',0)
#time.sleep(0.1)
#
"""ADC = np.asarray(struct.unpack('<8192b',fpga.read('adc_snap_bram',8192)))
#
ADC1 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,0,:]))).astype('float')
ADC2 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,1,:]))).astype('float')
ADC3 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,2,:]))).astype('float')
ADC4 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,3,:]))).astype('float')
#
rms1 = np.std(ADC1)
rms2 = np.std(ADC2)
rms3 = np.std(ADC3)
rms4 = np.std(ADC4)
#    
print 'RMS of ADC 1 ',rms1
print 'RMS of ADC 2 ',rms2
print 'RMS of ADC 3 ',rms3
print 'RMS of ADC 4 ',rms4
print ADC.shape 
#
#
plt.figure()
#
plt.subplot(251)
plt.title('ADC 1')
plt.hist(ADC1,bins=13)
plt.subplot(256)
plt.plot(ADC1)
plt.subplot(252)
plt.title('ADC 2')
plt.hist(ADC2,bins=13)
plt.subplot(257)
plt.plot(ADC2)
plt.subplot(253)
plt.title('ADC 3')
plt.hist(ADC3,bins=13)
plt.subplot(258)
plt.plot(ADC3)
plt.subplot(254)
plt.title('ADC 4')
plt.hist(ADC4,bins=13)
plt.subplot(259)
plt.plot(ADC4)
plt.subplot(155)
plt.title('All')
plt.hist(np.ravel(ADC),bins=20)
plt.show()"""
#
#
#
# 2^12-1 is the largest shift

fpga.write_int('sel1',2)
time.sleep(0.1)
fpga.write_int('coeff1',32768)
time.sleep(0.1)


fpga.write_int('reg_arm',0)
time.sleep(0.1)
now = datetime.datetime.now()
t_to_next_sec = (1000000-now.microsecond)/1.e6
time.sleep(0.1+t_to_next_sec)
start_time = Time((datetime.datetime.now()+datetime.timedelta(seconds=1)).replace(microsecond=0)).mjd
print start_time
with open("/home/user/cand_times_sync/header_2.txt","r+") as f:
    old = f.readlines()
new = "MJD_START %0.11f" %start_time
old[-1] = new
with open("/home/user/cand_times_sync/header_2.txt","w") as f:
    f.writelines(old)
f.close()
fpga.write_int('reg_arm',1)
time.sleep(0.1)
# jonathon edit force_sync
"""fpga.write_int('force_sync',2)
time.sleep(0.1)
fpga.write_int('force_sync',0)
time.sleep(0.1)
fpga.write_int('force_sync',1)
time.sleep(0.1)
fpga.write_int('force_sync',0)
"""
fpga.write_int('gbe1_ctrl',1);
time.sleep(0.1)
fpga.write_int('gbe1_ctrl',0);
fpga.write_int('gbe1_ctrl',2);
time.sleep(0.1)
#fpga.write_int('gbe0_ctrl',1);
#time.sleep(0.1)
#fpga.write_int('gbe0_ctrl',0);
#fpga.write_int('gbe0_ctrl',2);
#time.sleep(0.1)

ADC = np.asarray(struct.unpack('<8192b',fpga.read('adc_snap_bram',8192)))
#
ADC1 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,0,:]))).astype('float')
ADC2 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,1,:]))).astype('float')
ADC3 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,2,:]))).astype('float')
ADC4 = (np.ravel(np.fliplr(ADC.reshape((1024,4,2))[:,3,:]))).astype('float')
#
rms1 = np.std(ADC1)
rms2 = np.std(ADC2)
rms3 = np.std(ADC3)
rms4 = np.std(ADC4)
#    
print 'RMS of ADC 1 ',rms1
print 'RMS of ADC 2 ',rms2
print 'RMS of ADC 3 ',rms3
print 'RMS of ADC 4 ',rms4
print ADC.shape
#
#
"""plt.figure()
#
plt.subplot(251)
plt.title('ADC 1')
plt.hist(ADC1,bins=13)
plt.subplot(256)
plt.plot(ADC1)
plt.subplot(252)
plt.title('ADC 2')
plt.hist(ADC2,bins=13)
plt.subplot(257)
plt.plot(ADC2)
plt.subplot(253)
plt.title('ADC 3')
plt.hist(ADC3,bins=13)
plt.subplot(258)
plt.plot(ADC3)
plt.subplot(254)
plt.title('ADC 4')
plt.hist(ADC4,bins=13)
plt.subplot(259)
plt.plot(ADC4)
plt.subplot(155)
plt.title('All')
plt.hist(np.ravel(ADC),bins=20)
plt.show()"""
