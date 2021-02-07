from picoscope import ps5000a
import pylab as pl
import numpy as np
from time import sleep

ps=ps5000a.PS5000a()
ps.setChannel("A",enabled=True, coupling="DC", VRange=2)
ps.setChannel("B",enabled=True, coupling="DC", VRange=2)
ps.setNoOfCaptures(1)
ps.memorySegments(1)
sampleRate=3e6
acquisitionTime=0.1 # Not entirely sure what this does in streaming case, but it affects the available sampling intervals
actSampleRate, maxN=ps.setSamplingFrequency(sampleRate, sampleRate*acquisitionTime)
ps.setSimpleTrigger('External', enabled=False)
#ps.quickSetup(chanAParams=dict(coupling="DC", VRange=2),
#        chanBParams=dict(coupling="DC", VRange=5),
#            nCaps=1,
#            sampleRate=10e6, acqTime=0.60,resolution=15,
#            triggerParams=dict(trigSrc="External", threshold_V=1.0, 
#                    direction="Rising", delay=0,enabled=False)
#              )

saveFileName='savestream.bin'
saveFile=open(saveFileName,'wb')
lastStartIndex=0
totPts=0;
import pdb
def streamingReadySimple(handle, nSamples, startIndex, overflow, triggerAt, triggered, autoStop, parameter):
    global totPts
    totPts+=nSamples
    endInd=startIndex+nSamples
    valid=data[:,startIndex:endInd]
    if valid.size<nSamples: #This is never run, as the picoscope handles the overruns itself (i.e. next call will tell us about the extra data)
        nStart=nSamples-valid.size
        print('circling back')
        valid=np.hstack([valid, data[:,:nStart]])
    valid.T.tofile(saveFile)

DSmode=0 #or 4 for downsampling
DSratio=1 # Or the downsample factor
data=ps.allocateDataBuffers(channels=["A", "B"],numSamples=int(1e6), downSampleMode=DSmode)
data=data.squeeze()

try:
    ps.runStreaming(bAutoStop=False, downSampleMode=DSmode, downSampleRatio=DSratio)
    from time import sleep, time
    t0=time()
    tElapsed=0
    while tElapsed<2:
        try:
            ps.getStreamingLatestValues(callback=streamingReadySimple)
        except OSError as e:
            if e.args[0].find('PICO_BUSY')>=0:
                print('PICO_BUSY exception, try again shortly')
            else:
                raise e
        tElapsed=time()-t0

finally:
    ps.stop()
    ps.close()
    print('saved {} pts, at approx {} per second'.format(totPts, float(totPts)/tElapsed))

saveFile.close()
dat2=np.fromfile(saveFileName, dtype='i2').reshape(-1,2).T
pl.plot(data.T)
pl.title('current buffer')
pl.figure()
pl.plot(dat2.T)
pl.title('From file')
pl.show()


