#-------------------------------------------------------------------------------
# Author:      Stefan
#-------------------------------------------------------------------------------
class Node(object):
#-------------------------------------------------------------------------------
    def __init__(self,value):
        self.value = value
        self.children = {}
#-------------------------------------------------------------------------------
    def __repr__(self):
        self.print()
        return
#-------------------------------------------------------------------------------
    def print(self,stng):
        if self.value == '$':
            print(stng[1:])
        stng = stng + self.value
        for char in self.children.keys():
            p = self.children[char]
            p.print(stng)

#-------------------------------------------------------------------------------
    def display(self):
        if self.value == '$': return
        print('======== NODE =======')
        print('--> self.value    =', self.value)
        print('--> self.children:[', end = "")
        for key in self.children:
            if key != '$':
                print(key,sep="",end =", ")
        print("]")
        print('---------------------')

        for char in self.children:
            (self.children[char]).display()
#-------------------------------------------------------------------------------
    def insert(self,stng):
        if stng == '':
            self.children['$'] = Node('$')
            return
        if stng[0] not in self.children.keys():
            p = Node(stng[0])
            self.children[stng[0]] = p
            p.insert(stng[1:])
            return
        self.children[stng[0]].insert(stng[1:])
#-------------------------------------------------------------------------------
    def search(self,stng):
        for char in self.children.keys():
            p = self.children[char]
            if char == '$' and stng == '':
                return True
            elif stng != '' and char == stng[0]:
                return p.search(stng[1:])
        return False
#-------------------------------------------------------------------------------
    def randomChild(self):
        from random import choice
        letterOptions = [key for key in self.children.keys()]
        if '$' in letterOptions and len(letterOptions) == 1:
            print('End of Word')
            return '$'
        else:
            if '$' in letterOptions:
                letterOptions.remove('$')
            childChar = choice(letterOptions)
            print(childChar)
            assert type(childChar) == str
            return self.children[childChar]
#-------------------------------------------------------------------------------
    def searchForNextLetter(self,stng):
        for char in self.children.keys():
            p = self.children[char]
            if char == stng:
                return p.randomChild()
            elif stng[0] == char:
                return p.searchForNextLetter(stng[1:])
#-------------------------------------------------------------------------------
    def fragmentInDictionary(self,stng):
        for char in self.children.keys():
            p = self.children[char]
            if char == stng:
                return True
            elif stng[0] == char:
                return p.fragmentInDictionary(stng[1:])
        return False
#-------------------------------------------------------------------------------
def spellWordFromString(root,stng):
    from random import choice
    p = root
    finalStng = stng
    while(len(stng) != 0):
        p = p.children[stng[0]]
        stng = stng[1:]
    while '$' not in list(p.children.keys()):
        lst = list(p.children.keys())
        char = choice(lst)
        finalStng = finalStng + char
        p = p.children[char]
    return finalStng
#-------------------------------------------------------------------------------
def printGhostDirections():
    print('+--------------------------------+')
    print('| Welcome to the game of Ghost.  |')
    print('| The human goes first. Enter    |')
    print('| your letters in the pop-up     |')
    print('| dialog boxes. Good luck.       |')
    print('+--------------------------------+')
#-------------------------------------------------------------------------------
def requestAndCheckHumanMove(root,stng):
    stng += input('HUMAN, enter your character: ').lower()[0]
    print('Cumulative word: ',stng)
    if len(stng) > 3 and root.search(stng) == True:
        print('------------------------------------------------')
        print('HUMAN LOSES because "',stng,'"is a word.',sep = '')
        print('------------------<GAME OVER>-------------------')
        exit()
    if root.fragmentInDictionary(stng) == False:
        print('------------------------------------------------')
        print('HUMAN LOSES because "',stng, \
              '"\n does not begin any word.', sep = '')
        print("[The computers word was",'""', \
             spellWordFromString(root,stng[0:-1]),'".]',sep = '')
        exit()
    return stng
#-------------------------------------------------------------------------------
def requestAndCheckComputerMove(root,stng):
    stng = stng + root.searchForNextLetter(stng).value
    print(' ',stng)
    if len(stng) > 3 and root.search(stng) == True:
        print('---------------------------------------------------')
        print('COMPUTER LOSES because"',stng,'"is a word.',sep = '')
        print('------------------<GAME OVER>----------------------')
        exit()
    return stng
#-------------------------------------------------------------------------------
def createTrieFromDictionaryFile():
    file = open('GhostDictionary.txt')
    oodle = file.read().split('\n')
    root = Node('*')
    for word in oodle:
        root.insert(word)
    return root
#-------------------------------------------------------------------------------
def main():
    root = createTrieFromDictionaryFile()
    printGhostDirections()
    stng = ''
    while True:
        stng = requestAndCheckHumanMove(root,stng)
        stng = requestAndCheckComputerMove(root,stng)





if __name__ == '__main__':
    main()
