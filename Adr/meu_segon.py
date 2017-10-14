import launchpad_py
import time


lp = launchpad_py.LaunchpadMk2()


res = lp.Open()
lp.Reset()

xcoord = 4
ycoord = 4

colorpers = 64
colorobs = 120

while 1:
	ll = lp.ButtonStateXY()
	if(len(ll) != 0):
		if ll[0] == 0 and ll[1] == 0: # up
		

