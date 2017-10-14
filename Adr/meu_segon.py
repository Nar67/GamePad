import launchpad_py
import time
import objs
import random
#import button_thread
from threading import Lock, Thread

def check_if_out_of_bounds(x, y, YMIN, YMAX, XMIN, XMAX):
	return x > XMAX or x < XMIN or y > YMAX or y < YMIN

class button_thread(Thread):

	def __init__(self, execute_lock):
		super(button_thread, self).__init__()
		self.el = execute_lock
		self.flag = 0

	def stopt(self):
		self.flag = 1

	def run(self):
		while not self.flag:
			ll = []

			self.el.acquire()
			#ll = self.lh.ButtonStateXY()
			self.el.release()

			global ycoord
			ycoord = ycoord + 1

			if(len(ll) != 0):
				if ll[0] == 0 and ll[1] == 0 and ycoord < YMAX: # up
					ycoord += 1

				elif ll[0] == 1 and ll[1] == 0 and ycoord > YMIN: #down
					ycoord -= 1

				elif ll[0] == 2 and ll[1] == 0 and xcoord > XMIN: # izquierda
					xcoord -= 1

				elif ll[0] == 3 and ll[1] == 0 and xcoord < XMAX: # derecha
					xcoord += 1


#lp = launchpad_py.LaunchpadMk2()


#res = lp.Open()
#lp.Reset()

XMIN = 0
YMIN = 1
XMAX = 7
YMAX = 8

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


el = Lock()
thr1 = button_thread(el)
thr1.start()

#thr1.stopt()

while 1:
	#ll = []

	matrix = [[]]

	#ll = lp.ButtonStateXY()

	for x in range(XMIN - 1 , XMAX + dist_marge*2 + 1):
		submat = []
		for y in range(YMIN - 1, YMAX + dist_marge*2 + 1):
			submat.append("X")
		matrix.append(submat)

	

	for x in range(XMIN - 1, XMAX + 1):
		for y in range(YMIN - 1, YMAX + 1):
			if x != 8 and y != 0:
				matrix[x + dist_marge][y + dist_marge] = "*"
				el.acquire()
				#lp.LedCtrlXYByCode(x, y, colorfons)
				el.release()

	el.acquire()
	#lp.LedCtrlXYByCode(0, 0, 67)
	#lp.LedCtrlXYByCode(0, 1, 67)
	#lp.LedCtrlXYByCode(0, 2, 67)
	#lp.LedCtrlXYByCode(0, 3, 67)
	el.release()

	suplist = []
	for i, coord in enumerate(objects):
		matrix[coord[0] + dist_marge][coord[1] + dist_marge] = "."
		if coord[0] != 8 and coord[1] != 0:
			el.acquire()
			#lp.LedCtrlXYByCode(coord[0], coord[1], colorobjs)
			el.release()
		coord[0] += desplacx
		coord[1] += desplacy
		if not check_if_out_of_bounds(coord[0], coord[1], YMIN - dist_marge/2, YMAX + dist_marge/2, XMIN - dist_marge/2, XMAX + dist_marge/2):
			suplist.append([coord[0], coord[1]])
	objects = suplist
	#matrix[xcoord + dist_marge][ycoord + dist_marge] = "+"
	el.acquire()
	#lp.LedCtrlXYByCode(xcoord, ycoord, colorpers)
	el.release()

	if curr_torn%torns_gen == 0:
		objects = objects + objs.get_obj_1(random.randint(XMIN - dist_marge/2, XMAX + dist_marge/2)*desplacy - desplacx*2, random.randint(YMIN - dist_marge/2, YMAX + dist_marge/2)*desplacx - desplacy*2)

	#lp.ButtonFlush()
	time.sleep(0.1)

	curr_torn += 1

	
	print "-------------------------------"

	for x in matrix:
		stringa = ""
		for y in x:
			stringa += y
		print stringa
	print "Valor xcoord {} , valor ycoord {}".format(xcoord, ycoord)

