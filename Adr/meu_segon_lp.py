import launchpad_py
import time
import objs
import random

def check_if_out_of_bounds(x, y, YMIN, YMAX, XMIN, XMAX):
	return x > XMAX or x < XMIN or y > YMAX or y < YMIN


lp = launchpad_py.LaunchpadMk2()


res = lp.Open()
lp.Reset()

XMIN = 0
YMIN = 0
XMAX = 7
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

dist_marge = 5

matrix = [[]]



while 1:
	ll = []

	matrix = [[]]

	ll = lp.ButtonStateXY()

	for x in range(XMIN - 1 , XMAX + dist_marge*2 + 1):
		submat = []
		for y in range(YMIN - 1, YMAX + dist_marge*2 + 1):
			submat.append("X")
		matrix.append(submat)

	if(len(ll) != 0):
		if ll[0] == 0 and ll[1] == 0 and ycoord < YMAX: # up
			ycoord += 1

		elif ll[0] == 0 and ll[1] == 1 and ycoord > YMIN: #down
			ycoord -= 1

		elif ll[0] == 0 and ll[1] == 2 and xcoord > XMIN: # izquierda
			xcoord -= 1

		elif ll[0] == 0 and ll[1] == 3 and xcoord < XMAX: # derecha
			xcoord += 1

	for x in range(XMIN - 1, XMAX + 1):
		for y in range(YMIN - 1, YMAX + 1):
			matrix[x + dist_marge][y + dist_marge] = "*"
			lp.LedCtrlXYByCode(x, y, colorfons)

	suplist = []
	for i, coord in enumerate(objects):
		matrix[coord[0] + dist_marge][coord[1] + dist_marge] = "."
		lp.LedCtrlXYByCode(coord[0], coord[1], colorobjs)
		coord[0] += desplacx
		coord[1] += desplacy
		if not check_if_out_of_bounds(coord[0], coord[1], YMIN - dist_marge/2, YMAX + dist_marge/2, XMIN - dist_marge/2, XMAX + dist_marge/2):
			suplist.append([coord[0], coord[1]])
	objects = suplist
	matrix[xcoord + dist_marge][ycoord + dist_marge] = "+"
	lp.LedCtrlXYByCode(xcoord, ycoord, colorpers)

	if curr_torn%torns_gen == 0:
		objects = objects + objs.get_obj_1(random.randint(XMIN - dist_marge/2, XMAX + dist_marge/2)*desplacy - desplacx*2, random.randint(YMIN - dist_marge/2, YMAX + dist_marge/2)*desplacx - desplacy*2)

	#lp.ButtonFlush()
	time.sleep(0.1)

	curr_torn += 1

	'''
	print "-------------------------------"

	for x in matrix:
		stringa = ""
		for y in x:
			stringa += y
		print stringa'''


