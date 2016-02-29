#!/usr/bin/python
# coding: utf-8

import sys,math,struct,numpy,matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pylab
from scipy import signal
#from signal import signal, SIGPIPE, SIG_DFL


#signal(SIGPIPE,SIG_DFL)

class modulation:
    def __init__(self):
        self.samplerate = 2e5
        self.frequency = 200
        self.length = self.frequency*10
        self.fftsample = 512
        #self.timeshift = 128
        self.blackman = numpy.blackman(self.fftsample)
        self.signal = [math.sin(2*math.pi*self.frequency*i/self.samplerate) for i in xrange(self.length)]

    def run(self):
        out = 0
        z1 = 0
        z2 = 0
        outputlist = []
        for line in self.signal:
            z1 = line + z1 - z2
            out = self.quantization(z1)
            z2 = out
            outputlist.append(out)
        spectrum = numpy.fft.fft(outputlist[0:0+self.fftsample])
        spplot = (numpy.sqrt(numpy.power(spectrum.real,2)+numpy.power(spectrum.imag,2)))
        freqlist = numpy.fft.fftfreq(self.fftsample,d=1/self.samplerate)
        b, a = signal.iirfilter(4, 1000 / (self.samplerate / 2), btype = 'lowpass', analog = False, ftype = 'butter', output = 'ba')
        w,h = signal.freqz(b,a,self.fftsample)
        bpltlist = spplot
        #bpltlist *= abs(h)
        print len(spplot)
        print spplot
        plt.plot(freqlist[0:self.fftsample/2],spplot[0:self.fftsample/2])
        plt.axis([0, self.samplerate/2.0, 0, 500])
        plt.xlim()

        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude spectrum")
        plt.show()

    def quantization(self,sig):
        if sig > 0:
            return 1
        else:
            return -1



        #self.obj =
        #for line in self.reader:
        #    self.writelist = []
        #    for idx in list:
        #        self.writelist.append(10*math.log10(float(line[idx]))+c_cal)
        #    self.writelist.append(self.zround(float(line[24])))
        #    self.writer.writerow(self.writelist)

if __name__ == "__main__":
    m = modulation()
    m.run()
