import launchpad_py
import time
import random

lp = launchpad_py.LaunchpadMk2()
res = lp.Open()
lp.Reset()

PURPLE = 52

speed = 0.5
guesses = 0
score = 1


class Player(object):

	def __init__(self, hp=8, score=0):
		self.hp = hp
		self.score = score
		
	def decreaseHp(self):
		self.hp -= 1

	def increaseScore(self):
		self.score += 1

class GuessCoords(object):

	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		

guessCoords = (x, y, color)

guessList = [guessCoords]

for x in range(1, 9):
	lp.LedCtrlXYByCode(8, x, PURPLE)
while guesses < score:
	guessList.append([[random.randint(0, 8)][random.randint(1, 9)] [random.randint(4, 127)]])
	print("test", guessList)
	#guessCoords[guesses][0] = random.randint(0, 8) 
	#guessCoords[guesses][1] = random.randint(1, 9)
	#guessCoords[guesses][2] = random.randint(4, 127)
	lp.LedCtrlXYByCode(guessList[guesses][0], guessList[guesses][1], guessList[guesses][2])
	time.sleep(0.5)
	guesses += 1

#while len(guessCoords) > 0:




