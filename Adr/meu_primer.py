import launchpad_py
import time


lp = launchpad_py.LaunchpadMk2()

res = lp.Open()
lp.Reset()
while 1:
	ll = lp.ButtonStateXY()
	lp.LedCtrlXYByCode(ll[0], ll[1], ll[2])
	time.sleep(0.5)
	lp.LedCtrlXYByCode(ll[0], ll[1], 0)
