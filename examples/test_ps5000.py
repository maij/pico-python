"""Test acquiring bulk data on a ps5000a
"""
from picoscope import ps5000a
ps=ps5000a.PS5000a()

ps.quickSetup(
		chanParams=dict(coupling="AC", VRange=10.0, VOffset=0),
		resolution="15",
		nCaps=1, nMemorySegments=-1, sampleRate=5e6, acqTime=1e-3,
		triggerParams=dict(trigSrc="External", threshold_V=1.0, direction="Rising", delay=0, enabled=True, timeout_ms=100),
ps.runBlock(pretrig=0,segmentIndex=0)
ps.waitReady()
(data,nSamps,ovf)=ps.getDataRawBulk()
t=arange(nSamps)*ps.sampleInterval

# Now do something with it...


