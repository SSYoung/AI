#-------------------------------------------------------------------------------
# Author:      Stefan Young
#-------------------------------------------------------------------------------
from pickle import load
#-------------------------------------------------------------------------------
def loadFile(fileName):
    file = open(fileName, 'rb')
    loadedDictionary = load(file)
    assert type(loadedDictionary) == dict
    file.close()
    return loadedDictionary
#-------------------------------------------------------------------------------
def g(path):
    return len(path)
#-------------------------------------------------------------------------------
def h(word,target):
    assert type(word) == str
    count = 0
    for n in range (len(word) if len(word) < len(target) else len(target)):
        if(word[n] != target[n]):
            count += 1
    return count
#-------------------------------------------------------------------------------
def f(path,word,target):
    return g(path) + h(word,target)
#-------------------------------------------------------------------------------
def AStarSearch(startingWord,endingWord,dictionary):
    queue = []
    closed = {}
    queue.append((0,startingWord,[],0))
    popCount = 0
    dictList =[]
    max = 0

    while queue:
        #---Sort
        queue.sort()
        popCount+=1
        #---Extract Parent Node
        (fValue, node, path, gValue) = queue.pop(0)

        #---Check popped-off Node
        if(node == endingWord):
            print(path + [node])
            print("Max Queue Length " + str(max))
            return popCount

        #---Place parent on closed list, it shouldnt be there
        if(node in closed):
            continue

        assert node not in closed
        closed[node] = gValue

        #---Generate Children
        dictList = dictionary[node][0]
        for child in dictList:
            #---Create new Child, Just in Case
            cPath = path + [node]
            cG = gValue + 1
            cF = f(cPath,child,endingWord)
            childx = (cF,child,cPath,cG)

            #closed list cases
            if(child in closed):
                if(closed[child] < cG):
                    continue
                else:
                    del closed[child]
                    queue.append(childx)

            #open list cases
##            elif(child not in queue):
##                queue.append(childx)
            else:
                found = False
                for nodex in queue:
                    title = nodex[1]
                    if(title == child):
                        found = True
                        if(nodex[3] > cG):
                            queue.remove(nodex)
                            queue.append(childx)
                if(not found):
                    queue.append(childx)


        if(len(queue) > max):
            max = len(queue)

#-------------------------------------------------------------------------------
def testDictionary(retrieved):
    assert type(retrieved) == dict
    count = 0
    for word in retrieved:
        print(word, " ")
        print(retrieved[word])
        count+=1
        if(count==10):
            break
#-------------------------------------------------------------------------------
def main():
    dictionary = loadFile("dictionary.txt")
    startingWord = input("Starting Word? ")
    endingWord = input("Final Word? ")

    print("pop count: " + str(AStarSearch(startingWord,endingWord,dictionary)))
    print("and in reverse:")
    print(" ")
    print("pop count: " + str(AStarSearch(endingWord,startingWord,dictionary)))

#-------------------------------------------------------------------------------
main()

