import threading, launchpad_py, time, random

#GLOBALS
mapa = [[False for x in range(9)] for y in range(9)] #MAPA
mapa[8] = 9*[True]
for x in range(0, 9):
    mapa[x][0] = True

sleep = 0.5

BLUE = 37       #color de la moto 1
D_plr1 = [0,0]
U_plr1 = [1,0]
R_plr1 = [2,0]
L_plr1 = [3,0]
pos_b1 = [4,1] #posicio actual de la moto 1

d_vect1 = [0,1] #direccio i sentit que segueix la moto 1
B1_Alive = True #marca si la moto 1 segueix viva

PURPL = 57      #color de la moto 2
R_plr2 = [8,5]
L_plr2 = [8,6]
U_plr2 = [8,7]
D_plr2 = [8,8]
pos_b2 = [3,8]  #posicio actual de la moto 2

d_vect2 = [0,-1] #direccio i sentit que segueix la moto 2
B2_Alive = True #marca si la moto 2 segueix viva

#AUXILIARS
def Winner():
    global B1_Alive, B2_Alive

    COLOR = BLUE
    if not B1_Alive and B2_Alive:
        COLOR = PURPL
    elif not B1_Alive and not B2_Alive:
        auto = random.randint(0, 3)
        if auto:
            COLOR = PURPL

    lp.LedAllOn(COLOR)

def buttCtrl():
    global B1_Alive, B2_Alive
    while B1_Alive and B2_Alive:
        lbutt = lp.ButtonStateXY()
        if(len(lbutt) and lbutt[2]):
            if(lbutt[0] == D_plr1[0] and lbutt[1] == D_plr1[1]):
                printer(False,U_plr1,D_plr1)
                turnDown(d_vect1)
            elif(lbutt[0] == D_plr2[0] and lbutt[1] == D_plr2[1]):
                printer(True,U_plr2,D_plr2)
                turnDown(d_vect2)
            elif(lbutt[0] == U_plr1[0] and lbutt[1] == U_plr1[1]):
                printer(False,U_plr1,D_plr1)
                turnUp(d_vect1)
            elif(lbutt[0] == U_plr2[0] and lbutt[1] == U_plr2[1]):
                printer(True,U_plr2,D_plr2)
                turnUp(d_vect2)
            elif(lbutt[0] == R_plr1[0] and lbutt[1] == R_plr1[1]):
                printer(False,R_plr1,L_plr1)
                turnRight(d_vect1)
            elif(lbutt[0] == R_plr2[0] and lbutt[1] == R_plr2[1]):
                printer(True,R_plr2,L_plr2)
                turnRight(d_vect2)
            elif(lbutt[0] == L_plr1[0] and lbutt[1] == L_plr1[1]):
                printer(False,R_plr1,L_plr1)
                turnLeft(d_vect1)
            elif(lbutt[0] == L_plr2[0] and lbutt[1] == L_plr2[1]):
                printer(True,R_plr2,L_plr2)
                turnLeft(d_vect2)

def turnDown(list):
    if list != [0,1]:
        list[0] = 0
        list[1] = -1

def turnUp(list):
    if list != [0,-1]:
        list[0] = 0
        list[1] = 1

def turnLeft(list):
    if list != [-1,0]:
        list[0] = 1
        list[1] = 0

def turnRight(list):
    if list != [1,0]:
        list[0] = -1
        list[1] = 0

def steep():
    pos_b1[0] += d_vect1[0]
    pos_b1[1] += d_vect1[1]

    pos_b2[0] += d_vect2[0]
    pos_b2[1] += d_vect2[1]

def death():
    global B1_Alive, B2_Alive
    if pos_b1 == pos_b2:
        B2_Alive = B1_Alive = False
    if (pos_b1[0] < 0 or pos_b1[1] > 8) or (mapa[pos_b1[0]][pos_b1[1]]):
        B1_Alive = False
    if (pos_b2[0] < 0 or pos_b2[1] > 8) or (mapa[pos_b2[0]][pos_b2[1]]):
        B2_Alive = False

def maparize():
    mapa[pos_b1[0]] [pos_b1[1]] = True
    mapa[pos_b2[0]][pos_b2[1]] = True

def Reset():
    global mapa, pos_b1, pos_b2, d_vect1, d_vect2, B1_Alive, B2_Alive

    mapa = [[False for x in range(9)] for y in range(9)] #MAPA
    mapa[8] = 9*[True]
    for x in range(0, 9):
        mapa[x][0] = True

    pos_b1 = [4,1]
    d_vect1 = [0,1]
    B1_Alive = True
    pos_b2 = [3,8]
    d_vect2 = [0,-1]
    B2_Alive = True

def printer(b,listA,listB):
    if not b:
        lp.LedCtrlXYByCode(D_plr1[0], D_plr1[1], BLUE)
        lp.LedCtrlXYByCode(U_plr1[0], U_plr1[1], BLUE)
        lp.LedCtrlXYByCode(R_plr1[0], R_plr1[1], BLUE)
        lp.LedCtrlXYByCode(L_plr1[0], L_plr1[1], BLUE)
    else:
        lp.LedCtrlXYByCode(D_plr2[0], D_plr2[1], PURPL)
        lp.LedCtrlXYByCode(U_plr2[0], U_plr2[1], PURPL)
        lp.LedCtrlXYByCode(R_plr2[0], R_plr2[1], PURPL)
        lp.LedCtrlXYByCode(L_plr2[0], L_plr2[1], PURPL)

    lp.LedCtrlXYByCode(listA[0], listA[1], 0)
    lp.LedCtrlXYByCode(listB[0], listB[1], 0)


#MAIN
lp = launchpad_py.LaunchpadMk2()
res = lp.Open()

while True:
    lp.Reset()

    printer(False,U_plr1,D_plr1)
    printer(True,U_plr2,D_plr2)

    pr = threading.Thread(target=buttCtrl)
    pr.start()

    while B1_Alive and B2_Alive:
        lp.LedCtrlXYByCode(pos_b1[0], pos_b1[1], BLUE)
        lp.LedCtrlXYByCode(pos_b2[0], pos_b2[1], PURPL)
        maparize()

        time.sleep(sleep)
        steep()
        death()

    Winner()

    while not len(lp.ButtonStateXY()):
        lp.ButtonStateXY()

    Reset()

#END MAIN