import launchpad_py
import time
import objs
import random

def check_if_out_of_bounds(x, y, YMIN, YMAX, XMIN, XMAX):
	return x > XMAX or x < XMIN or y > YMAX or y < YMIN


lp = launchpad_py.LaunchpadMk2()


res = lp.Open()
lp.Reset()

XMIN = 1
YMIN = 0
XMAX = 8
YMAX = 7

xcoord = 6
ycoord = 6

colorpers = 64
colorobjs = 120
colorfons = 71

objects = []

desplacx = 1
desplacy = 0

torns_gen = 6
curr_torn = 0

dist_marge = 20

while 1:
	ll = []
	ll = lp.ButtonStateXY()

	if(len(ll) != 0):
		if ll[0] == 0 and ll[1] == 0 and ycoord < YMAX: # up
			ycoord += 1

		elif ll[0] == 0 and ll[1] == 1 and ycoord > YMIN: #down
			ycoord -= 1

		elif ll[0] == 0 and ll[1] == 2 and xcoord > XMIN: # izquierda
			xcoord -= 1

		elif ll[0] == 0 and ll[1] == 3 and xcoord < XMAX: # derecha
			xcoord += 1

	for x in range(XMIN, XMAX):
		for y in range(YMIN, YMAX):
			lp.LedCtrlXYByCode(x, y, colorfons)

	suplist = []
	for i, coord in enumerate(objects):
		lp.LedCtrlXYByCode(coord[0], coord[1], colorobjs)
		coord[0] += desplacx
		coord[1] += desplacy
		if not check_if_out_of_bounds(coord[0], coord[1], YMIN - dist_marge, YMAX + dist_marge, XMIN - dist_marge, XMAX + dist_marge):
			suplist.append([coord[0], coord[1]])
	objects = suplist
	lp.LedCtrlXYByCode(xcoord, ycoord, colorpers)

	if curr_torn%torns_gen == 0:
		objects = objects + objs.get_obj_1(random.randint(XMIN, XMAX)*desplacx, random.randint(YMIN, YMAX)*desplacy)

	lp.ButtonFlush()
	time.sleep(0.3)

	curr_torn += 1


