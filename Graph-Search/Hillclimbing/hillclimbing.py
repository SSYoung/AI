#------------------------------GLOBAL IMPORTS-----------------------------------
from math import sin, cos, pi
from random import random
HILLS = 100
FLOP_MAX = 1000
#-------------------------------------------------------------------------------
def f(x,y):
    if x<=0 or x >= 10 or y<= 0 or y >= 10:
        return float('inf')
    return (x*sin(4*x) + 1.1*y*sin(2*y))
#-------------------------------------------------------------------------------
def createLookUpTables(r):
    sinLookup = []
    cosLookup = []
    for t in frange(0, 2 * pi, pi / 64):
        sinLookup.append(r * sin(t))
        cosLookup.append(r * cos(t))
    return sinLookup, cosLookup
#-------------------------------------------------------------------------------
def frange(start,stop,step):
    i = start
    while i < stop:
        yield i
        i += step
#-------------------------------------------------------------------------------
def gridGenerator(MAX):
    from math import sqrt
    side = int(sqrt(MAX))
    for x in range(side):
        for y in range(side):
            yield (x,y)
#-------------------------------------------------------------------------------
def randomPoints(trials):
    bestF = float('inf')
    bestX = 0
    bestY = 0
    for n in range(trials):
        x = random() * 10
        y = random() * 10
        fVal = f(x,y)
        if (fVal < bestF):
            bestF = fVal
            bestX = x
            bestY = y
    return 'best X: ', round(bestX,3), ' best Y:', round(bestY,3), ' best F:', round(bestF,3)
#-------------------------------------------------------------------------------
def randomHillClimbing():
    bestVals = [float('inf'), 0, 0]
    radius = 0.001
    for n in range(HILLS):
        x = random() * 10
        y = random() * 10
        bestF = float('inf')
        bestX = 0
        bestY = 0
        better = True
        while better:
            better = False
            for t in frange(0, 2 * pi, pi / 64):
                trialX = x + radius * cos(t);
                trialY = y + radius * sin(t);
                trialF = f(trialX, trialY)
                if (trialF < bestF):
                    bestF = trialF
                    bestX = trialX
                    bestY = trialY
                    better = True
        if bestF < bestVals[0]:
            bestVals[0] = bestF
            bestVals[1] = bestX
            bestVals[2] = bestY
    return 'best X: ', round(bestVals[1],3), ' best Y:', round(bestVals[2],3), ' best F:', round(bestVals[0],3)
#-------------------------------------------------------------------------------
def gridHillClimbing():
    bestVals = []
    radius = 0.001
##    for n in range(HILLS):
    for (x,y) in gridGenerator(HILLS):
        better = True
        bestF = float('inf')
        bestX = 0
        bestY = 0
        while better:
            improvement = False
            for t in frange(0,2*pi, 2*pi/64):
                trialX = x + radius*cos(t)
                trialY = y + radius*sin(t)
                trialF = f(trialX,trialY)
                if trialF < bestF:
                    bestX = trialX
                    bestY = trialY
                    x = trialX
                    y = trialY
                    bestF = trialF
                    improvement = True
            if not improvement:
                better = False
        vals = [bestF, bestX, bestY]
        bestVals.append(vals)
    bestVal = min(bestVals)
    bestF = bestVal[0]
    bestX = bestVal[1]
    bestY = bestVal[2]
    return 'best X: ', round(bestX,3), ' best Y:', round(bestY,3), ' best F:', round(bestF,3)
#-------------------------------------------------------------------------------
def randomHillClimbingLookUp():
    radius = 0.001
    RADIUS_TIMES_SINE, RADIUS_TIMES_COSINE = createLookUpTables(radius)
    bestVals = [float('inf'), 0, 0]
    for n in range(HILLS):
        x = random() * 10
        y = random() * 10
        bestF = float('inf')
        bestX = 0
        bestY = 0
        better = True
        while better:
            better = False
            for n in range(64):
                trialX = x + RADIUS_TIMES_COSINE[n];
                trialY = y + RADIUS_TIMES_SINE[n];
                trialF = f(trialX, trialY)
                if (trialF < bestF):
                    bestF = trialF
                    bestX = trialX
                    bestY = trialY
                    better = True
        if bestF < bestVals[0]:
            bestVals[0] = bestF
            bestVals[1] = bestX
            bestVals[2] = bestY
    return 'best X: ', round(bestVals[1],3), ' best Y:', round(bestVals[2],3), ' best F:', round(bestVals[0],3)
#-------------------------------------------------------------------------------
    #Helper method to sort nelder mead points
def sortHelper(a, b, c):
    valsF = [[f(a[0],a[1]),a[0],a[1]], [f(b[0],b[1]),b[0],b[1]], [f(c[0],c[1]), c[0],c[1]]]
    valsF.sort()
    a = [ valsF[0][1], valsF[0][2] ]
    b = [ valsF[1][1], valsF[1][2] ]
    c = [ valsF[2][1], valsF[2][2] ]
    return a,b,c
#-------------------------------------------------------------------------------
def nelderMead():
    bestVals = [float('inf'), 0, 0]
    for n in range(HILLS):
        #Best, Good, Worst
        B, G, W = [random() * 10, random()*10], [random() * 10, random() * 10], [random() * 10, random() * 10]
        B, G, W = sortHelper(B, G, W)
        flopCount = 0
        # Avoid flopping back and forth around same value
        while flopCount < FLOP_MAX:
            #Midpoint of BG
            M = [(B[0] + G[0]) / 2, (B[1] + G[1]) / 2]
            #Reflection of W over BG through M
            R = [2 * M[0] - W[0], 2 * M[1] - W[1]]

            # Either reflect or extend
            if f(R[0], R[1]) < f(G[0], G[1]):
                if f(B[0], B[1]) < f(R[0], R[1]):
                    W = R
                else:
                    #Expansion over E
                    E = [2 * R[0] - M[0], 2 * R[1] - M[1]]
                    if f(E[0], E[1]) < f(B[0], B[1]):
                        W = E
                    else:
                        W = R
            #contract or shrink
            else:
                if f(R[0], R[1]) < f(W[0], W[1]):
                    W = R
                C = [(W[0] + M[0]) / 2, (W[1] + M[1]) / 2]
                if f(C[0], C[1]) < f(W[0], W[1]):
                    W = C
                else:
                    S = [(W[0] + B[0]) / 2, (W[1] + B[1]) / 2]
                    W = S
                    G = M
            B, G, W = sortHelper(B, G, W)
            flopCount += 1
        if (f(B[0], B[1]) < bestVals[0]):
            bestVals[0] = f(B[0], B[1])
            bestVals[1] = B[0]
            bestVals[2] = B[1]
    return 'best X: ', round(bestVals[1],3), ' best Y:', round(bestVals[2],3), ' best F:', round(bestVals[0],3)
#-------------------------------------------------------------------------------
def main():

    from time import clock
    trials = 10000
    START_TIME = clock()
    print('------ Random Hill Climbing:             ', randomHillClimbing())
    print('| %5.2f'%(clock()-START_TIME), 'seconds without LookUp')
    START_TIME = clock()
    print('------ Random Hill Climbing with LookUp: ', randomHillClimbingLookUp())
    print('| %5.2f'%(clock()-START_TIME), 'seconds with LookUp')
    START_TIME = clock()
    print('------ Grid Based Hill Climbing:         ', gridHillClimbing())
    print('| %5.2f'%(clock()-START_TIME), 'seconds with Grids')
    START_TIME = clock()
    print('------ 10,000 Random Points:             ', randomPoints(trials))
    print('| %5.2f'%(clock()-START_TIME), 'seconds with 10000 random points')
    START_TIME = clock()
    print('------ Nelder Mead Method:               ', nelderMead() )
    print('| %5.2f'%(clock()-START_TIME), 'seconds with 10000 random points')

if __name__ == '__main__':
    main()
