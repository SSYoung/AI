"""
Stefan Young
Word Ladder Search

Steps:
1. Using a list of 6 letter words from the dictionary.txt file,
    implement a greedy search algorithm to find the word ladder
    from a starting word to ending word
2.
"""
#----------------------------------------------------------------
from pickle import load, dump, HIGHEST_PROTOCOL
from collections import deque
#----------------------------------------------------------------
def create_dictionary():
    words = []
    with open('dictionary.txt', 'r') as f:
        words = f.read().splitlines()
    dictionary = {}
    for word in words:
        dictionary[word] = findNeighbors(word, words);
    return dictionary
#----------------------------------------------------------------
def findNeighbors(word, words):
    neighbors = []
    bounds = range(len(word))
    for other in words:
        if (other !=  word):
            diff = 0
            for i in bounds:
                if word[i] != other[i]:
                    diff += 1
            if diff == 1:
                neighbors.append(other)
    return neighbors
#----------------------------------------------------------------
def save(dictionary):
    with open('dictionary.pkl', 'wb') as f:
        dump(dictionary, f, HIGHEST_PROTOCOL)
#----------------------------------------------------------------
def read_database():
    with open('dictionary.pkl', 'rb') as f:
        database = load(f)
    return database
#----------------------------------------------------------------
def bfs(database, start_word, ending_word):
    popCount = 0;
    queue = []
    queue.append((start_word, [start_word]))
    popped = start_word
    visited = set([start_word])
    while (queue) and (popped != ending_word):
        popCount += 1
        popped, path = queue.pop(0)
        visited.add(popped)
        if popped == ending_word:
            print('Pop Count: ', popCount)
            return path
        for neighbor in database[popped]:
            if neighbor not in visited:
                copy = path + [neighbor]
                queue.append((neighbor, path + [neighbor]))
    return -1
#----------------------------------------------------------------
def main():
    #dictionary = create_dictionary()
    #save(dictionary)
    dictionary = read_database()
    start_word = input("What is the starting word? ")
    end_word = input("What is the ending word? ")
    print(bfs(dictionary, start_word, end_word))
#----------------------------------------------------------------
main()