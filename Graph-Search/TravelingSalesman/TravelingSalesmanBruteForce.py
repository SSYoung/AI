#-------------------------------------------------------------------------------
# Name:        Traveling Salesman
# Purpose:
#
# Author:      Stefan
#
# Created:     11/04/2015
# Copyright:   (c) Stefan 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##############################################<START OF PROGRAM>##############################################
def setUpCanvas(root): # These are the REQUIRED magic lines to enter graphics mode.
    root.title("THE TRAVELING SALESMAN PROBLEM by Stefan Y")
    canvas = Canvas(root, width  = root.winfo_screenwidth(), height = root.winfo_screenheight(), bg = 'black')
    canvas.pack(expand = YES, fill = BOTH)
    return canvas
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def script(x, y, msg = '', kolor = 'WHITE'):
    canvas.create_text(x, y, text = msg, fill = kolor,  font = ('Helvetica', 10, 'bold'))
#---------------------------------------------------------------------------------Traveling Salesman Problem-

def plot(city): # Plots 5x5 "points" on video screen
    x = city[1]+5; y = city[2]+5 # The +5 is to push away from the side bars.
    if city[0] == -1:
        kolor = 'WHITE'
    else: kolor = 'YELLOW'
    canvas.create_rectangle(x-2, y-2, x+2, y+2, width = 1, fill = kolor)
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def line(city1, city2, kolor = 'RED'):
    canvas.create_line(city1[1]+5, city1[2]+5, city2[1]+5, city2[2]+5, width = 1, fill = kolor)
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def displayDataInConsole(AlgorithmResults, baseCity, city):
    print('===<Traveling Salesman Path Statistics>===')
    print ('   algorithm         path length ')
    for element in AlgorithmResults:
           print ('---%-20s'%element[0], int(element[2]))
    city.sort()
    baseCity.sort()
    if city == baseCity:
        print("---Data verified as unchanged.")
    else:
        print ('ERROR: City data has been corrupted!')
    print('   Run time =', round(clock()-START_TIME, 2), ' seconds.')
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def printCity(city): # Used for debugging.
    count = 0
    for (id,x,y) in city:
        print( '%3d: id =%2d, (%5d, %5d)'%(count,id, int(x), int(y)))
        count += 1
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def displayPathOnScreen(city, statistics):
#=---Normalize data
    (minX, maxX, minY, maxY, meanX, meanY, medianX, medianY, size, m, b) = statistics
    canvas.delete('all')
    cityNorm, (p,q,r,s) = normalizeCityDataToFitScreen(city[:], statistics)

#---Plot points and lines
    cityNorm.append(cityNorm[0])
    plot(cityNorm[0])
    for n in range(1, len(cityNorm)):
        plot(cityNorm[n])
        line(cityNorm[n], cityNorm[n-1])
    script(650,  20, 'path length = ' + str(pathLength(city)))
    canvas.create_rectangle(530,10, 770, 30, width = 1, outline = 'WHITE')
    canvas.update()
    root.mainloop() # Required for graphics.
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def normalizeCityDataToFitScreen(city, statistics):
    """ Coordinates are all assumed to be non-negative."""
    (minX, maxX, minY, maxY, meanX, meanY, medianX, medianY, size, m, b) = statistics
    newCity = []

#---Step 1a. Shift city points to the x- and y-axes.
    for (id, x,y) in city:
        newCity.append ( (id, x-minX, y-minY))

#---Step 1b. Shift line-of-best-fit to the x- and y-axes.
    (x0,y0) = (maxX-minX, m*maxX+b - minY) # = x-intercept of line-of-best-fit.
    (x1,y1) = (minX-minX, m*minX+b - minY) # = y-intercept of line-of-best-fit.


#---Step 1c. Shift max-values to x- and y-axes.
    maxX = maxX-minX
    maxY = maxY-minY

#---Step 2a. # Re-scale city points to fit the screen.
    cityNorm = []
    for (id, x, y) in newCity:
        cityNorm.append ((id, x*SCREEN_WIDTH/maxX, y*SCREEN_HEIGHT/maxY))

#---Step 2b. # Re-scale the x-axis and y-axis intercepts for the line-of-best-fit.
    (x0,y0) = x0/maxX*SCREEN_WIDTH, y0/maxY*SCREEN_HEIGHT # a point on the x-axis
    (x1,y1) = x1/maxX*SCREEN_WIDTH, y1/maxY*SCREEN_HEIGHT # a point on the y-axis

    return cityNorm, (x1,y1,x0,y0) # = the adjusted city xy-values and 2 points on the line-of-best-fit.
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def readDataFromFileAndAppendId(fileName):
    file1 = open(fileName, 'r')
    fileLength = int(file1.readline()) # removes heading
    city = []
    for elt in range(fileLength):
       x, y = file1.readline().split()
       city.append( [0, float(x), float(y)] ) # A place for an id (0, here) is appended.
    file1.close()
    return city
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def pathLength(city):
    totalPath = 0
    for n in range(1, len(city)):
        totalPath += dist( city[n-1], city[n] )
    totalPath += dist( city[n], city[0] )
    return int(totalPath)
#---------------------------------------------------------------------------------Traveling Salesman Problem--

def dataStatistics(city):
    xValues = []
    yValues = []
    size = len(city)
    for (id, x,y) in city:
        xValues.append(x)
        yValues.append(y)
    minX = min(xValues)
    maxX = max(xValues)
    minY = min(yValues)
    maxY = max(yValues)

    assert (minX >= 0 or maxX >= 0 or minY >= 0 or maxY >= 0)

    meanX = sum(xValues)/size
    meanY = sum(yValues)/size
    medianX = city[len(city)//2][0]
    medianY = city[len(city)//2][1]

#---Derive the line of best fit: y = mx+b
    xyDiff   = 0
    xDiffSqr = 0
    for (id, x,y) in city:
        xyDiff  += (meanX - x)*(meanY - y)
        xDiffSqr+= (meanX - x)**2

    m = xyDiff/xDiffSqr
    b = meanY - m*meanX

    return minX, maxX, minY, maxY, meanX, meanY, medianX, medianY, size, m, b
#---------------------------------------------------------------------------------Traveling Salesman Problem--
def dist(cityA, cityB):
    return hypot(cityA[1]-cityB[1], cityA[2] - cityB[2])
#-------------------------------------------------------------------------------
def nearestCityAlgorithm(originalList):
    cities = originalList
#    start = cities[0]
#    cities.remove(start)
    tour = [[0] for n in range(len(cities))]
    count = 0
    while len(cities) != 0:
        nextCity = cities[0]
        cities.remove(nextCity)
        tour[count] = nextCity
        cities.sort(key = lambda x: hypot(nextCity[1] - x[1], nextCity[2] - x[2]))
        count += 1
    return tour
#-------------------------------------------------------------------------------
def nearestCity(city, cities):
    return min(cities.sort(key = lambda x: hypot(city[1]-x[1],city[2]-x[2])))
#-------------------------------------------------------------------------------
def hillClimbingTSP(cities):
    count = 0
    while count < 100:
        diffCities = []
        L = len(cities)
        for n in range(L-1):
            for x in range(n,L-1):
                if isSwitchBetter(n,x,cities):
                    rand = cities
                    temp = rand[x]
                    rand[x] = rand[n]
                    rand[n] = temp
                    diffCities.append([pathLength(rand),rand])
        diffCities.sort()
        newCities = diffCities[0][1]
        if pathLength(cities) < pathLength(newCities):
            break
        else:
            cities = newCities
        count += 1
    return cities
#-------------------------------------------------------------------------------
def isSwitchBetter(indexA, indexB, cities):
    cityA = cities[indexA]
    cityB = cities[indexB]
    if indexA != 0 and indexB !=(len(cities)-1):
        cityAprev = cities[indexA-1]
        cityAnext = cities[indexA+1]
        cityBprev = cities[indexB-1]
        cityBnext = cities[indexB+1]
        distOld = dist(cityAprev,cityA) + dist(cityAnext,cityA) + dist(cityBprev,cityB) + dist(cityBnext,cityB)
        distNew = dist(cityAprev,cityB) + dist(cityAnext,cityB) + dist(cityBprev,cityA) + dist(cityBnext,cityA)
    elif indexA == 0 and indexB != (len(cities)-1):
        cityAnext = cities[indexA+1]
        cityBprev = cities[indexB-1]
        cityBnext = cities[indexB+1]
        distOld = dist(cityAnext,cityA) + dist(cityBprev,cityB) + dist(cityBnext,cityB)
        distNew = dist(cityAnext,cityB) + dist(cityBprev,cityA) + dist(cityBnext,cityA)
    elif indexA != 0 and indexB ==(len(cities)-1):
        cityAprev = cities[indexA-1]
        cityAnext = cities[indexA+1]
        cityBprev = cities[indexB-1]
        distOld = dist(cityAprev,cityA) + dist(cityAnext,cityA) + dist(cityBprev,cityB)
        distNew = dist(cityAprev,cityB) + dist(cityAnext,cityB) + dist(cityBprev,cityA)
    else:
        cityAnext = cities[indexA+1]
        cityBprev = cities[indexB-1]
        distOld = dist(cityAnext,cityA) + dist(cityBprev,cityB)
        distNew = dist(cityAnext,cityB) + dist(cityBprev,cityA)
#    print('Old: ', distOld, ' New: ', distNew)
    if distNew < distOld:
        return True
    else:
        return False
#====================================<GLOBAL CONSTANTS and GLOBAL IMPORTS>========Traveling Salesman Problem==

from tkinter   import Tk, Canvas, YES, BOTH
from operator  import itemgetter
from itertools import permutations
from copy import deepcopy
from random    import shuffle
from time      import clock
from math      import hypot
root           = Tk()
canvas         = setUpCanvas(root)
START_TIME     = clock()
SCREEN_WIDTH   = root.winfo_screenwidth() //5*5 - 15 # adjusted to exclude task bars on my PC.
SCREEN_HEIGHT  = root.winfo_screenheight()//5*5 - 90 # adjusted to exclude task bars on my PC.
fileName       = "./travelingSalesmanData038.txt"
#==================================================< MAIN >=======================Traveling Salesman Problem==

def main():
#---0. Read in data, append an id to every pair, and store results in a variable called "city".
    city  = readDataFromFileAndAppendId(fileName)

#---1. Extract statistics.
    statistics = (minX, maxX, minY, maxY, meanX, meanY, medianX, medianY, size, m, b) = dataStatistics(city)

#---2. Create a random path.
#    shuffle(city)

#---3. Sort on y-coordinate and connect sequentially by y.
#    city.sort(key = lambda x : x[2])

#---4. Sort on x-coordinate and connect sequentially by x.
#    city.sort(key = lambda x : x[1])

#---5. Your algorithm(s). Can you do better than the sorting algorithms above?
    tour = nearestCityAlgorithm(city)
    city = tour

#---5a. Hillclimbing
#    tour = hillClimbingTSP(city)
#    city = tour

#---6. Display results.
    displayPathOnScreen(city, statistics)
#---------------------------------------------------------------------------------Traveling Salesman Problem--
if __name__ == '__main__': main()
###############################################<END OF PROGRAM>###############################################