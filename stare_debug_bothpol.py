import numpy as np,struct,time,datetime,sys,socket,os
import matplotlib.pyplot as plt
from casperfpga import CasperFpga

fpga = CasperFpga(host='192.168.11.20')
time.sleep(2)
        
fpga.write_int('adc_snap_ctrl',3)
time.sleep(0.1)
fpga.write_int('adc_snap_ctrl',0)
time.sleep(0.1)

ADC = np.asarray(struct.unpack('<8192b',fpga.read('adc_snap_bram',8192)))

ADC1 = (np.ravel(ADC.reshape((1024,4,2))[:,0,:])).astype('float')
ADC2 = (np.ravel(ADC.reshape((1024,4,2))[:,1,:])).astype('float')
ADC3 = (np.ravel(ADC.reshape((1024,4,2))[:,2,:])).astype('float')
ADC4 = (np.ravel(ADC.reshape((1024,4,2))[:,3,:])).astype('float')

ADC1fft = np.fft.fft(ADC1)
ADC2fft = np.fft.fft(ADC2)
ADC3fft = np.fft.fft(ADC3)

ADC1power = ADC1fft*np.conj(ADC1fft)
ADC2power = ADC2fft*np.conj(ADC2fft)
ADC3power = ADC3fft*np.conj(ADC3fft)

rms1 = np.std(ADC1)
rms2 = np.std(ADC2)
rms3 = np.std(ADC3)
rms4 = np.std(ADC4)
    
print 'RMS of ADC 1 ',rms1
print 'RMS of ADC 2 ',rms2
print 'RMS of ADC 3 ',rms3
print 'RMS of ADC 4 ',rms4

PFB1 = np.asarray(struct.unpack('<2048h',fpga.read('debug1_pfb',4096)))
PFB2 = np.asarray(struct.unpack('<2048b',fpga.read('debug2_pfb',2048)))
PFB3 = np.asarray(struct.unpack('<2048b',fpga.read('debug3_pfb',2048)))
PFB4 = np.asarray(struct.unpack('<2048b',fpga.read('debug4_pfb',2048)))

acc_16 = np.flip(np.asarray(struct.unpack('>2048Q',fpga.read('acc_full',2048*8)))/2.**34,0)
#acc_16 = np.ravel(np.fliplr(acc_16_64.reshape(2048/4,4)))
acc_16_2 = np.flip(np.asarray(struct.unpack('>2048Q',fpga.read('acc_full1',2048*8)))/2.**34,0)

plt.figure(0)

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

"""plt.figure(2)
plt.subplot(221)
plt.title('FFT 1')
plt.plot(PFB1)
plt.subplot(222)
plt.title('FFT 2')
plt.plot(PFB2)
plt.subplot(223)
plt.title('FFT 3')
plt.plot(PFB3)
plt.subplot(224)
plt.title('FFT 4')
plt.plot(PFB4)
"""
plt.figure(3)
plt.title("pol0")
plt.plot(acc_16[2:-1])
#plt.yscale('log')
plt.figure(7)
plt.plot(acc_16_2[2:-1])
plt.title("pol1")

plt.figure(4)
plt.plot(ADC1power[1:])
plt.title("ADC1 power")
plt.figure(5)
plt.plot(ADC2power[1:])
plt.title("ADC2 power")
plt.figure(6)
plt.plot(ADC3power[1:])
plt.title("ADC3 power")
plt.show()



