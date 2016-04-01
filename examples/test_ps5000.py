"""Test acquiring bulk data on a ps5000a
"""
from picoscope import ps5000a
import pylab as pl
import pdb

#Open the scope
ps=ps5000a.PS5000a()

# Capture 10 traces from channel A at sample rate of 1MS/s , each 100 ms long
# The scope triggers by default at 1V off a rising edge on the External connector.
ps.quickSetup(chanAParams=dict(coupling="DC", VRange=5.0),
                chanBParams=dict(coupling="DC", VRange=5.),
            nCaps=10,
        sampleRate=1e6, acqTime=300e-3,resolution=15,
        triggerParams=dict(trigSrc="External", threshold_V=1.0, 
                direction="Rising", delay=0)
          )


ps.runBlock()
ps.waitReady()
#pdb.set_trace()
(data,nSamps,ovf)=ps.getDataVBulk(['A', 'B'])
ps.close()


for dat in data:
    t=pl.arange(nSamps)*ps.sampleInterval
    pl.figure()
    pl.plot(t, dat[::3].T)
    pl.xlabel("s")
    pl.ylabel("V")
    pl.show()


