import launchpad_py
import time
import random
import threading
import sys
from threading import Lock, Thread


lp = launchpad_py.LaunchpadMk2()
res = lp.Open()
lp.Reset()

PURPL = 57
fallingSpeed = 0.5
timeBetweenFalls = 1
isEnlightened = [[False for x in range(9)] for y in range(9)]

def fallingLight(column):
	for row in range(1, 9):
		lp.LedCtrlXYByCode(column, row, random.randint(4, 127))
		isEnlightened[column][row] = True
		time.sleep(fallingSpeed)
		lp.LedCtrlXYByCode(column, row, 0)
		isEnlightened[column][row] = False
	return


def fall():
	while 1:
		column = random.randint(0, 7)
		fallingLight(column)
		time.sleep(timeBetweenFalls)	


def buttonPress():
	score = 0
	while 1:
		pressedButtonCoords = lp.ButtonStateXY()
		if(len(pressedButtonCoords) != 0):
			print("test", pressedButtonCoords[0])
			x = pressedButtonCoords[0]
			y = pressedButtonCoords[1]
			if(isEnlightened[x][y]):
				lp.LedCtrlXYByCode(8, score, PURPL)
				score += 1



#if __name__ == '__main__':
t = threading.Thread(target = fall)
t2 = threading.Thread(target = buttonPress)
t.daemon = True
#t2.daemon = True
t.start()
t2.start()

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print("test")
		sys.exit(0)






