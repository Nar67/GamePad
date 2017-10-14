import launchpad_py
import time
lp = launchpad_py.LaunchpadMk2()

res = lp.Open()
lp.Reset()
while 1:
	ll = lp.ButtonStateXY()
	if(len(ll) != 0):
		if(ll[0] == 0 and ll[1] == 8):
			for x in range(11, 98):
				lp.LedCtrlRawByCode(x, 23)
				time.sleep(0.05)
				lp.LedCtrlRawByCode(x, 0)
	lp.ButtonFlush()

	
print(res)