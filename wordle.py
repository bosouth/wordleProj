import random as rand

data = open("valid.txt", "r")

#6 chances to guess secret 5 letter word

#mark 0 if letter not in word 
# mark 1 if letter in word but not in right place
# mark 2 if letter in word at the right place

def compare(sol, guess):
    i = 0
    solArray = []
    for ele in guess:
        if ele == sol[i]:
            solArray.append((ele, 2))
        elif ele in sol:
            solArray.append((ele, 1))
        else:
            solArray.append((ele, 0))
        i += 1
    return solArray

def newDictionary(tup, d):
    newDict = []
    for word in d:
        for l in range(len(word)):
            if tup[l][1] == 0:
                break
            elif tup[l][1] == 1:
                if tup[l][0] in word:
                    newDict.append(word)
            else:
                if tup[l][0] == word[l]:
                    newDict.append(word)
            
    return newDict  
    # return None

#modify data
words = data.readlines()
words = words[0].split(",")
words = [w.strip("\"") for w in words]

goalWord = "lawns"
attempt = 1

print(goalWord)

while attempt < 7:
    r = rand.randint(0, len(words) -1)

    guess = "loans"

    #compare
    tup = compare(goalWord, guess)

    # return dictionary with remaining valid words
    new = newDictionary(tup, words)

    print(guess)
    
    attempt += 1

