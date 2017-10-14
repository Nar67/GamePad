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

# coordenades inicials
CONS_xcoord = 6
CONS_ycoord = 6

CONS_colorpers = 64
CONS_colorobjs = 120
CONS_colorfons = 71

#CONS_objects = []

CONS_desplacx = 1
CONS_desplacy = 0


CONS_torns_changedir_easy = 30
CONS_torns_changedir_mig = 25
CONS_torns_changedir_hard = 18
CONS_torns_changedir_veryhard = 12


#for very hard
CONS_multiply_veryhard = 2
CONS_multiply_other = 1

CONS_torns_gen_easy = 18
CONS_torns_gen_mig = 15
CONS_torns_gen_hard = 12
CONS_torns_gen_veryhard = 9

CONS_curr_torn = 0

CONS_dist_marge = 5

CONS_colorveryhard = 5
CONS_colorhard = 4
CONS_colormig = 13
CONS_coloreasy = 21

CONS_colorchooser = 79
#CONS_matrix = [[]]

# ---------------------------------




def check_if_out_of_bounds(x, y, YMIN, YMAX, XMIN, XMAX):
	return x > XMAX or x < XMIN or y > YMAX or y < YMIN

class button_thread(Thread):

	#def __init__(self, execute_lock, xcoord, ycoord, YMIN, YMAX, XMIN, XMAX, check, stop):
	def __init__(self, launchpad, execute_lock, get_xcoord, get_ycoord, 
			incrementa_x_y, YMIN, YMAX, XMIN, XMAX, check, finish_game):
		super(button_thread, self).__init__()
		self.el = execute_lock
		self.YMIN = YMIN
		self.YMAX = YMAX
		self.XMIN = XMIN
		self.XMAX = XMAX
		self.lh = launchpad
		self.flag = 0
		self.check_if_collide = check
		#self.stop = stop
		self.getx = get_xcoord
		self.gety = get_ycoord
		self.incxy = incrementa_x_y
		self.finish = finish_game

	def stoptmanual(self):
		self.flag = 1


	def stopt(self, signum, frame):
		self.flag = 1
		sys.exit()

	def run(self):
		#signal.signal(signal.SIGINT, self.stop)  l
		#signal.signal(signal.SIGTERM, self.stop)

		while not self.flag:

			ll = []

			self.el.acquire()
			ll = self.lh.ButtonStateXY()
			self.el.release()
			#print "hola"

			self.el.acquire()
			if self.check_if_collide():
				self.finish()
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
				ll = self.lh.ButtonStateXY()
			#self.incxy(1, 0)
			#time.sleep(0.5)


class game:
	def __init__(self):
		self.lp = launchpad_py.LaunchpadMk2()
		self.res = self.lp.Open()
		self.lp.Reset()
		#self.lp = None
		hol = 1


	def reset_variables(self, difficult):
		self.multiply_despl = CONS_multiply_other
		if difficult == 0: #easy
			self.torns_gen = CONS_torns_gen_easy
			self.torns_changedir = CONS_torns_changedir_easy

		elif difficult == 1: #mitjana
			self.torns_gen = CONS_torns_gen_mig
			self.torns_changedir = CONS_torns_changedir_mig

		elif difficult == 2: #hard
			self.torns_gen = CONS_torns_gen_hard
			self.torns_changedir = CONS_torns_changedir_hard

		elif difficult == 3: # veryhard
			self.torns_gen = CONS_torns_gen_veryhard
			self.multiply_despl = CONS_multiply_veryhard
			self.torns_changedir = CONS_torns_changedir_veryhard


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

		
		self.curr_torn = CONS_curr_torn

		self.dist_marge = CONS_dist_marge

		self.flag_principal = 0

		self.el = Lock()
		
	def check_if_collide(self):
		for x in self.objects:
			if x[0] == self.xcoord and x[1] == self.ycoord:
				return True

	def incrementa_x_y(self, inc_x, inc_y):
		self.ycoord += inc_y
		self.xcoord += inc_x

	def get_xcoord(self):
		return self.xcoord

	def get_ycoord(self):
		return self.ycoord

	def finish_game(self):
		self.flag_principal = 1
		self.thr1.stoptmanual()

	def get_position(self):
		mitjax = (self.XMAX + self.XMIN)/2
		xpos = (self.dist_marge + mitjax + random.randint(-mitjax, mitjax))

		mitjay = (self.YMAX + self.YMIN)/2
		ypos = (self.dist_marge + mitjay + random.randint(-mitjay, mitjay))

		restax = self.dist_marge
		restay = self.dist_marge

		#print("----> (x, y) = ({}, {})".format(xpos - restax, ypos - restay))

		return [xpos, ypos, restax, restay]

	def generate_object(self):
		if self.curr_torn%self.torns_gen == self.torns_gen/3:
			p = self.get_position()
			self.objects = self.objects + objs.get_obj_1(p[0], p[1], p[2], p[3])
				
				
		elif self.curr_torn%self.torns_gen == self.torns_gen/3*2:
			'''self.objects = self.objects + objs.get_obj_2(
				random.randint(self.XMIN - self.dist_marge/2, self.XMAX + self.dist_marge/2)*self.desplacy, 
				random.randint(self.YMIN - self.dist_marge/2, self.YMAX + self.dist_marge/2)*self.desplacx)'''
			p = self.get_position()
			self.objects = self.objects + objs.get_obj_2(p[0], p[1], p[2], p[3])
		elif self.curr_torn%self.torns_gen == 0:
			'''self.objects = self.objects + objs.get_obj_3(
				random.randint(self.XMIN - self.dist_marge/2, self.XMAX + self.dist_marge/2)*self.desplacy, 
				random.randint(self.YMIN - self.dist_marge/2, self.YMAX + self.dist_marge/2)*self.desplacx)'''
			p = self.get_position()
			self.objects = self.objects + objs.get_obj_3(p[0], p[1], p[2], p[3])

	def change_dirs(self):
		if random.randint(0, 1) == 0:
			self.desplacx = random.randint(-1, 1)
			if self.desplacx == 0:
				self.desplacy = random.randint(-1, 1)
				if self.desplacy == 0:
					self.desplacy = 1
		else:
			self.desplacy = random.randint(-1, 1)
			if self.desplacy == 0:
				self.desplacx = random.randint(-1, 1)
				if self.desplacx == 0:
					self.desplacx = 1
		self.desplacx *= random.randint(0, 1)*self.multiply_despl
		self.desplacy *= random.randint(0, 1)*self.multiply_despl

	def menu_principal(self):
		for fila in reversed(range(1, 8)):
			self.lp.LedCtrlXYByCode(0, fila, CONS_colorveryhard)
		for fila in reversed(range(3, 8)):
			self.lp.LedCtrlXYByCode(2, fila, CONS_colorhard)
		for fila in reversed(range(5, 8)):
			self.lp.LedCtrlXYByCode(4, fila, CONS_colormig)
		for fila in reversed(range(7, 8)):
			self.lp.LedCtrlXYByCode(6, fila, CONS_colorhard)

		self.lp.LedCtrlXYByCode(0, 0, CONS_colorchooser)
		self.lp.LedCtrlXYByCode(0, 2, CONS_colorchooser)
		self.lp.LedCtrlXYByCode(0, 4, CONS_colorchooser)
		self.lp.LedCtrlXYByCode(0, 8, CONS_colorchooser)
		dificultat = -1
		while dificultat == -1:
			ll = self.lp.ButtonStateXY()
			if(len(ll) != 0):
				if ll[0] == 0 and ll[1] == 0: # up
					dificultat = 3

				elif ll[0] == 2 and ll[1] == 0: #down
					dificultat = 2

				elif ll[0] == 4 and ll[1] == 0: # izquierda
					dificultat = 1

				elif ll[0] == 6 and ll[1] == 0: # derecha
					dificultat = 0

				ll = self.lp.ButtonStateXY()

	def start_game(self):
		
		self.thr1 = button_thread(self.lp, self.el, self.get_xcoord, self.get_ycoord, 
			self.incrementa_x_y, self.YMIN, self.YMAX, self.XMIN, self.XMAX, 
			self.check_if_collide, self.finish_game)
		self.thr1.start()
		signal.signal(signal.SIGINT, self.thr1.stopt)
		signal.signal(signal.SIGTERM, self.thr1.stopt)

		while not self.flag_principal:
			ll = []

			matrix = [[]]

			ll = self.lp.ButtonStateXY()

			for x in range(self.XMIN , self.XMAX + self.dist_marge*2):
				submat = []
				for y in range(self.YMIN, self.YMAX + self.dist_marge*2):
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


				x = coord[0] + self.dist_marge
				y = coord[1] + self.dist_marge

				#print ("(x, y) = ({}, {}), mult = {}, lenMat: {} , lenMat[{}]: ".format(x, y, self.multiply_despl, len(matrix), x))


				#if len(matrix) > x and 0 <= x and 0 <= y and len(matrix[x]) > y:
				matrix[x][y] = "."

				if coord[0] != 8 and coord[1] != 0:

					self.el.acquire()
					self.lp.LedCtrlXYByCode(coord[0], coord[1], self.colorobjs)
					self.el.release()

				coord[0] += self.desplacx
				coord[1] += self.desplacy

				mitjax = (self.XMAX + self.XMIN)/2
				xpos = (self.dist_marge + mitjax + random.randint(-mitjax, mitjax))

				mitjay = (self.YMAX + self.YMIN)/2
				ypos = (self.dist_marge + mitjay + random.randint(-mitjay, mitjay))

				restax = self.dist_marge
				restay = self.dist_marge
				if not check_if_out_of_bounds(coord[0] + self.dist_marge, coord[1] + self.dist_marge, 
						self.YMIN + self.dist_marge/2, 
						self.YMAX + self.dist_marge/2, 
						self.XMIN + self.dist_marge/2, 
						self.XMAX + self.dist_marge/2):
					suplist.append([coord[0], coord[1]])

			self.objects = suplist

			matrix[self.xcoord + self.dist_marge][self.ycoord + self.dist_marge] = "+"

			self.el.acquire()
			self.lp.LedCtrlXYByCode(self.xcoord, self.ycoord, self.colorpers)
			self.el.release()

			self.generate_object()
			self.change_dirs()

			#lp.ButtonFlush()
			#time.sleep(0.3)

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
	dif = 2
	dif = g.menu_principal()
	g.reset_variables(dif)
	g.start_game()

