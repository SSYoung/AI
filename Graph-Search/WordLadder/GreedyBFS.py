#-------------------------------------------------------------------------------#
# Author:      Stefan Young
#-------------------------------------------------------------------------------
def loadFile(fileName):
    file = open(fileName, 'rb')
    import pickle
    loadedDictionary = pickle.load(file)
    assert type(loadedDictionary) == dict
    file.close()
    return loadedDictionary
#-------------------------------------------------------------------------------
def h(word,endingWord):
    return sum([endingWord[n] != word[n] for n in range (0,len(word))])
#-------------------------------------------------------------------------------
def establishPath(startingWord,endingWord,dictionary):
    print("Establish Path is Reached")
    popCount = 0
    queue = []
    neighbors = []
    check = 0
    dictionary.get(startingWord)[1] = 0
    while(queue):
        popCount += 1
        queue.sort(key = h(popped,endingWord))
        popped = queue.pop(0)
        if (popped == endingWord):
            print("Pop Count: ", popCount)

        neighbors = dictionary.get(popped)[0]
        for neighbor in neighbors:
            if(dictionary.get(neighbor)[1] == -1):
                queue.append(neighbor)
                dictionary.get(neighbor)[2] = popped
                dictionary.get(neighbor)[1] = dictionary.get(popped)[1] + 1
    print('No paths exist')
#-------------------------------------------------------------------------------
def writePath(startingWord,endingWord,dictionary):
    print("WRITE PATH IS REACHED")
    pathStack = [endingWord]
    currentWord = endingWord
    parent = dictionary.get(endingWord)[2]
    while(parent!=startingWord):
        currentWord = parent
        pathStack.append(parent)
        parent = dictionary.get(currentWord)[2]
    pathStack.append(startingWord)
    pathStack.reverse()
    for word in pathStack:
        print(word , end = "  ")
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
    dictionary = loadFile("dictionary.pkl")
    #dictionary = loadFile('dictionaryTest.txt')
    startingWord = input("Starting Word? ")
    endingWord = input("Final Word? ")
    testDictionary(dictionary)
    print("pop count: " + str(establishPath(startingWord,endingWord,dictionary)))
    writePath(startingWord,endingWord,dictionary)

#-------------------------------------------------------------------------------
main()