import launchpad_py
import time
from threading import Thread

parar = False
button = None
lor = None
vides = 4
int1 = 73
int2 = 77


def main():
    lp = launchpad_py.LaunchpadMk2()
    res = lp.Open()
    lp.Reset()
    lp.LedCtrlRawByCode(83, 45)
    lp.LedCtrlRawByCode(84, 45)
    lp.LedCtrlRawByCode(85, 45)
    lp.LedCtrlRawByCode(86, 45)

    def scroll(i,j,temps,vides):
        global parar
        global button
        global lor
        x = i
        #i = 71
        #j = 79
        #time = 0.25
        #vides = 4
        while x in range (i, j) and not parar:
            button = x
            lor = "left"
            time.sleep(temps)
            lp.LedCtrlRawByCode(x, 45)
            lp.LedCtrlRawByCode(x-vides, 0)
            if x == j-1:
                time.sleep(temps)
                lp.LedCtrlRawByCode(x-3, 0)
        
                time.sleep(temps)
                lp.LedCtrlRawByCode(x-2, 0)
        
                time.sleep(temps)
                lp.LedCtrlRawByCode(x-1, 0)
        
                time.sleep(temps)
                lp.LedCtrlRawByCode(x, 0)
                    
                time.sleep(temps)
                lp.LedCtrlRawByCode(x, 45)
                x = x - 1
                while x in range (i, j-1) and not parar:
                    button = x
                    lor = "right"
                    time.sleep(temps)
                    lp.LedCtrlRawByCode(x, 45)
                    lp.LedCtrlRawByCode(x+4, 0)
                    x = x - 1
                if not parar:
                    time.sleep(temps)
                    lp.LedCtrlRawByCode(x+4, 0)
                    time.sleep(temps)
                    lp.LedCtrlRawByCode(x+3, 0)
                    time.sleep(temps)
                    lp.LedCtrlRawByCode(x+2, 0)
                    time.sleep(temps)
                    lp.LedCtrlRawByCode(x+1, 0)
        
            x = x + 1

    def buttonpressed(i,j):
        lp.LedCtrlRawByCode(104, 45)
        global parar
        global button
        global lor
        global vides
        global int1
        global int2
        while not parar:
            ll = lp.ButtonStateXY()
            if len(ll) > 0:
                if ll[0] == 0 and ll[1] == 0 and ll[2] == 127:
                    print "para"
                    parar = True
        print button
        print lor
        lp.LedCtrlRawByCode(int1-2, 0)
        lp.LedCtrlRawByCode(int1-1, 0)
        lp.LedCtrlRawByCode(int2, 0)
        lp.LedCtrlRawByCode(int2+1, 0)
        if lor == "left" and int2 >= int1:
            print "i"
            print i
            print "j"   
            print j
            for z in (0, vides):
                if button-z not in range (i,j):
                    vides = vides -1
                    lp.LedCtrlRawByCode(button-z,0)
                    int1 = int1 + 1

            print "int2"
            print int2
            print "int1"    
            print int1

        if lor == "right" and int2 >= int1:
            print "i"
            print i
            print "j"   
            print j
            for z in (0, vides):
                if button+z not in range (i,j):
                    vides = vides - 1
                    lp.LedCtrlRawByCode(button+z,0)
                    int2 = int2 - 1

            print "int2"
            print int2
            print "int1"    
            print int1
        

        

    i = 71
    j = 79
    temps = 0.25
    vides = 4
    global vides
    global int1
    global int2
    for a in range (0, 7):
        lp.LedCtrlRawByCode(78,0)
        lp.LedCtrlRawByCode(77,0)
        lp.LedCtrlRawByCode(71,0)
        lp.LedCtrlRawByCode(72,0)
        lp.LedCtrlRawByCode(68,0)
        lp.LedCtrlRawByCode(67,0)
        lp.LedCtrlRawByCode(62,0)
        lp.LedCtrlRawByCode(61,0)
        lp.LedCtrlRawByCode(58,0)
        lp.LedCtrlRawByCode(57,0)
        lp.LedCtrlRawByCode(52,0)
        lp.LedCtrlRawByCode(51,0)
        lp.LedCtrlRawByCode(48,0)
        lp.LedCtrlRawByCode(47,0)
        lp.LedCtrlRawByCode(42,0)
        lp.LedCtrlRawByCode(41,0)
        lp.LedCtrlRawByCode(38,0)
        lp.LedCtrlRawByCode(37,0)
        lp.LedCtrlRawByCode(32,0)
        lp.LedCtrlRawByCode(31,0)
        lp.LedCtrlRawByCode(28,0)
        lp.LedCtrlRawByCode(27,0)
        lp.LedCtrlRawByCode(22,0)
        lp.LedCtrlRawByCode(21,0)
        lp.LedCtrlRawByCode(18,0)
        lp.LedCtrlRawByCode(17,0)
        lp.LedCtrlRawByCode(12,0)
        lp.LedCtrlRawByCode(11,0)
        aux1 = int1
        aux2 = int2
        if vides > 0:
            t = Thread(target=scroll, args=(i,j,temps,vides))
            t2 = Thread(target=buttonpressed, args=(aux1, aux2))
            
            t.start()
            t2.start()
            time.sleep(5)
            int1 = int1-10
            int2 = int2-10
            parar = False
            i = i - 10
            j = j - 10
            temps = temps*0.5

if __name__ == "__main__":
    main()
