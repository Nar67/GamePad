import launchpad_py
import time
import random
import time
import rtmidi



NUM_COLUMNS = 8
HP_COLUMN = 8
PURPLE = 52
CYAN = 37
GREEN = 64
RED = 72
LED_OFF = 0
SPEED = 0.5


class Board(object):

    def __init__(self, lp, hp=8, score=0):
        self.lp = lp
        self.hp = hp
        self.score = score
        
    def decreaseHp(self):
        self.hp -= 1
        self.initBoard()

    def increaseScore(self):
        self.score += 1

    def initBoard(self):
        self.lp.Reset()
        for x in range(NUM_COLUMNS - self.hp + 1, NUM_COLUMNS + 1):
            self.lp.LedCtrlXYByCode(HP_COLUMN, x, PURPLE)
        print("init board. hp: %s, formula: %s" % (self.hp, NUM_COLUMNS - self.hp + 1))

    def isAlive(self):
        return self.hp > 0

    def displayTurnTransition(self):
        self.lp.LedAllOn(CYAN)
        time.sleep(1)
        self.initBoard()

    def displayFailureTransition(self):
        self.lp.LedAllOn(RED)
        time.sleep(1)
        self.initBoard()

    def displaySuccessTransition(self):
        self.lp.LedAllOn(GREEN)
        time.sleep(1)
        self.initBoard()        





class SequenceCoords(object):

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    @staticmethod
    def generateCoord():
        x = random.randint(0, NUM_COLUMNS - 1)
        y = random.randint(1, NUM_COLUMNS)
        color = random.randint(4, 127)
        coord = SequenceCoords(x, y, color)
        return coord

    def matches(self, x, y):
        return self.x == x and self.y == y


class Sequence(object):

    def __init__(self, lp):
        self.lp = lp
        self.ledList = []

    def addCoords(self, coords):
        self.ledList.append(coords)

    def displaySequence(self):
        for coord in self.ledList:
            self.lp.LedCtrlXYByCode(coord.x, coord.y, coord.color)
            time.sleep(SPEED)
            self.lp.LedCtrlXYByCode(coord.x, coord.y, 0)

    def checkUserSequence(self):
        self.lp.ButtonFlush()
        it = 0;
        while 1:
            state = self.lp.ButtonStateXY()
            if state:
                coord = self.ledList[it]
                x, y, pressed = state
                print("pushed coord: (%s, %s, %s), current %sth coord: (%s, %s)" % (x, y, pressed, it, coord.x, coord.y))
                if coord.matches(x, y):
                    if pressed:
                        self.lp.LedCtrlXYByCode(coord.x, coord.y, coord.color)
                        if it == (len(self.ledList)  - 1):
                            return True
                    else:
                        self.lp.LedCtrlXYByCode(coord.x, coord.y, LED_OFF)
                        it += 1
                else:
                    return False



def main():
    lp = launchpad_py.LaunchpadMk2()
    res = lp.Open()
    lp.Reset()

    try:

        board = Board(lp)
        board.initBoard()
        sequence = Sequence(lp)
        rounds = 0
        while board.isAlive():
            coord = SequenceCoords.generateCoord()
            sequence.addCoords(coord)
            sequence.displaySequence()
            board.displayTurnTransition()
            success = sequence.checkUserSequence()
            if success:
                board.displaySuccessTransition()
            else:
                board.decreaseHp()
                board.displayFailureTransition()
            rounds += 1 
            print("*** ROUND %s FINISHED ***" % rounds)



    except KeyboardInterrupt as ki:
        print("Exit game...")
    finally:
        lp.Reset()
        lp.Close()

if __name__ == "__main__":
    main()
