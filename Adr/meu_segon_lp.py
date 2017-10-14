import launchpad_py
import time
import objs
import random
import signal
import sys
#import button_thread
from threading import Lock, Thread

#----------- CONSTANTS ------------
CONS_XMIN = 0
CONS_YMIN = 1
CONS_XMAX = 7
CONS_YMAX = 8

CONS_xcoord = 6
CONS_ycoord = 6

CONS_colorpers = 64
CONS_colorobjs = 120
CONS_colorfons = 71

#CONS_objects = []

CONS_desplacx = 1
CONS_desplacy = 0

CONS_torns_gen = 6
CONS_curr_torn = 0

CONS_dist_marge = 5

#CONS_matrix = [[]]

# ---------------------------------




def check_if_out_of_bounds(x, y, YMIN, YMAX, XMIN, XMAX):
	return x > XMAX or x < XMIN or y > YMAX or y < YMIN

class button_thread(Thread):

	#def __init__(self, execute_lock, xcoord, ycoord, YMIN, YMAX, XMIN, XMAX, check, stop):
	def __init__(self, launchpad, execute_lock, get_xcoord, get_ycoord, incrementa_x_y, YMIN, YMAX, XMIN, XMAX, check, stop):
		super(button_thread, self).__init__()
		self.el = execute_lock
		self.YMIN = YMIN
		self.YMAX = YMAX
		self.XMIN = XMIN
		self.XMAX = XMAX
		self.lh = launchpad
		self.flag = 0
		self.check_if_collide = check
		self.stop = stop
		self.getx = get_xcoord
		self.gety = get_ycoord
		self.incxy = incrementa_x_y


	def stopt(self, signum, frame):
		self.flag = 1
		sys.exit()

	def run(self):
		#signal.signal(signal.SIGINT, self.stop)
		#signal.signal(signal.SIGTERM, self.stop)

		while not self.flag:

			ll = []

			self.el.acquire()
			ll = self.lh.ButtonStateXY()
			self.el.release()
			#print "hola"

			self.el.acquire()
			#if self.check_if_collide():
			#	flag_principal = 1
			self.el.release()

			if(len(ll) != 0):
				if ll[0] == 0 and ll[1] == 0 and self.gety() > self.YMIN: # up
					self.el.acquire()
					self.incxy(0, -1)
					self.el.release()

				elif ll[0] == 1 and ll[1] == 0 and self.gety() < self.YMAX: #down
					self.el.acquire()
					self.incxy(0, 1)
					self.el.release()

				elif ll[0] == 2 and ll[1] == 0 and self.getx() > self.XMIN: # izquierda
					self.el.acquire()
					self.incxy(-1, 0)
					self.el.release()

				elif ll[0] == 3 and ll[1] == 0 and self.getx() < self.XMAX: # derecha
					self.el.acquire()
					self.incxy(1, 0)
					self.el.release()

			#self.incxy(1, 0)
			#time.sleep(0.5)


class game:
	def __init__(self):
		self.lp = launchpad_py.LaunchpadMk2()
		self.res = self.lp.Open()
		self.lp.Reset()
		#self.lp = None
		hol = 1


	def reset_variables(self):
		self.XMIN = CONS_XMIN
		self.YMIN = CONS_YMIN
		self.XMAX = CONS_XMAX
		self.YMAX = CONS_YMAX

		self.xcoord = CONS_xcoord
		self.ycoord = CONS_ycoord

		self.colorpers = CONS_colorpers
		self.colorobjs = CONS_colorobjs
		self.colorfons = CONS_colorfons

		self.objects = []

		self.desplacx = CONS_desplacx
		self.desplacy = CONS_desplacy

		self.torns_gen = CONS_torns_gen
		self.curr_torn = CONS_curr_torn

		self.dist_marge = CONS_dist_marge

		self.flag_principal = 0

		self.el = Lock()
		
	def check_if_collide(self):
		for x in self.objects:
			if x[0] == self.xcoord and x[1] == self.ycoord:
				return True

	def stop_thread(self, signum, frame):
		self.flag_principal = 1
		sys.exit()

	def incrementa_x_y(self, inc_x, inc_y):
		self.ycoord += inc_y
		self.xcoord += inc_x

	def get_xcoord(self):
		return self.xcoord

	def get_ycoord(self):
		return self.ycoord

	def start_game(self):
		
		thr1 = button_thread(self.lp, self.el, self.get_xcoord, self.get_ycoord, self.incrementa_x_y, self.YMIN, self.YMAX, self.XMIN, self.XMAX, self.check_if_collide, self.stop_thread)
		thr1.start()
		signal.signal(signal.SIGINT, thr1.stopt)
		signal.signal(signal.SIGTERM, thr1.stopt)

		while not self.flag_principal:
			ll = []

			matrix = [[]]

			ll = self.lp.ButtonStateXY()

			for x in range(self.XMIN - 1 , self.XMAX + self.dist_marge*2 + 1):
				submat = []
				for y in range(self.YMIN - 1, self.YMAX + self.dist_marge*2 + 1):
					submat.append("X")
				matrix.append(submat)

			

			for x in range(self.XMIN, self.XMAX + 1):
				for y in range(self.YMIN, self.YMAX + 1):
					if x != 8 and y != 0:
						matrix[x + self.dist_marge][y + self.dist_marge] = "*"
						self.el.acquire()
						self.lp.LedCtrlXYByCode(x, y, self.colorfons)
						self.el.release()

			self.el.acquire()
			self.lp.LedCtrlXYByCode(0, 0, 67)
			self.lp.LedCtrlXYByCode(1, 0, 67)
			self.lp.LedCtrlXYByCode(2, 0, 67)
			self.lp.LedCtrlXYByCode(3, 0, 67)
			self.el.release()

			suplist = []
			for coord in self.objects:

				matrix[coord[0] + self.dist_marge][coord[1] + self.dist_marge] = "."

				if coord[0] != 8 and coord[1] != 0:

					self.el.acquire()
					self.lp.LedCtrlXYByCode(coord[0], coord[1], self.colorobjs)
					self.el.release()

				coord[0] += self.desplacx
				coord[1] += self.desplacy
				if not check_if_out_of_bounds(coord[0], coord[1], self.YMIN - self.dist_marge, self.YMAX + self.dist_marge, self.XMIN - self.dist_marge, self.XMAX + self.dist_marge):
					suplist.append([coord[0], coord[1]])

			self.objects = suplist

			matrix[self.xcoord + self.dist_marge][self.ycoord + self.dist_marge] = "+"

			self.el.acquire()
			self.lp.LedCtrlXYByCode(self.xcoord, self.ycoord, self.colorpers)
			self.el.release()

			

			if self.curr_torn%self.torns_gen == self.torns_gen/3:
				self.objects = self.objects + objs.get_obj_1(random.randint(self.XMIN - self.dist_marge/2, self.XMAX + self.dist_marge/2)*self.desplacy - self.desplacx*2, random.randint(self.YMIN - self.dist_marge/2, self.YMAX + self.dist_marge/2)*self.desplacx - self.desplacy*2)
			elif self.curr_torn%self.torns_gen == self.torns_gen/3*2:
				self.objects = self.objects + objs.get_obj_2(random.randint(self.XMIN - self.dist_marge/2, self.XMAX + self.dist_marge/2)*self.desplacy - self.desplacx*2, random.randint(self.YMIN - self.dist_marge/2, self.YMAX + self.dist_marge/2)*self.desplacx - self.desplacy*2)
			elif self.curr_torn%self.torns_gen == 0:
				self.objects = self.objects + objs.get_obj_3(random.randint(self.XMIN - self.dist_marge/2, self.XMAX + self.dist_marge/2)*self.desplacy - self.desplacx*2, random.randint(self.YMIN - self.dist_marge/2, self.YMAX + self.dist_marge/2)*self.desplacx - self.desplacy*2)

			#lp.ButtonFlush()
			time.sleep(0.1)

			self.curr_torn += 1

			
			print "-------------------------------"

			for x in matrix:
				stringa = ""
				for y in x:
					stringa += y
				print stringa

			print("Variable x {}".format(self.xcoord))









#signal.signal(signal.CTRL_C_EVENT, thr1.stopt)

g = game()
while 1:
	g.reset_variables()
	g.start_game()
