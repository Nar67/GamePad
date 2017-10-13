import launchpad_py
import time
lp = launchpad_py.LaunchpadMk2()

res = lp.Open()
lp.Reset()
for x in range(11, 98):
	lp.LedCtrlRawByCode(x, 72)
	time.sleep(0.05)
	lp.LedCtrlRawByCode(x, 0)
print(res)