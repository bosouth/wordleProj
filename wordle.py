import random as rand

data = open("valid.txt", "r")

#6 chances to guess secret 5 letter word

#mark 0 if letter not in word 
# mark 1 if letter in word but not in right place
# mark 2 if letter in word at the right place

def isValidWord(guess, words):
    isValid = False
    if guess in words:
        isValid = True
    return isValid

def checkYellows(yellow, guess):
    result = True
    for ele in yellow:
        if ele not in guess:
            result = False

    return result


def compare(sol, guess):
    # ensure that double letter guess are counted for
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

def newDictionary(tup, d, guess):
    green = []
    yellow = []
    for m in range(len(tup)):
        if tup[m][1] == 2:
            green.append((tup[m][0], m))
        if tup[m][1] == 1:
            yellow.append(tup[m][0])

    newDict = []
    tempDict = []


    for w in d:
        for ele in green:
            if w[ele[1]] == ele[0]:
                if green.index(ele) == len(green) - 1 and checkYellows(yellow, w) == True:
                    if w[ele[1]] == ele[0]:
                        newDict.append(w)
                        break
                    continue
            else:
                break
    return newDict  

#modify data
words = data.readlines()
words = words[0].split(",")
words = [w.strip("\"") for w in words]

goalWord = "beaux"
attempt = 1


while attempt < 7:
    r = rand.randint(0, len(words) -1)

    guess = "betas"

    if isValidWord(guess, words) == False:
        print("Invalid word")
        break

    #compare
    tup = compare(goalWord, guess)

    # return dictionary with remaining valid words
    new = newDictionary(tup, words, guess)

    print(new)

    # use knn to determine closest word, rinse and repeat
    
    attempt += 1

