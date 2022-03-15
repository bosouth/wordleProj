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
    newDict = []
    tempDict = []
    for word in d:
        for l in range(len(word)):
            if tup[l][1] == 0:
                continue
            elif tup[l][1] == 1:
                if tup[l][0] in word:
                    tempDict.append(word)
                break
            else:
                if tup[l][0] == word[l]:
                    tempDict.append(word)
                break
    if tempDict == []:
        return d

    # find indexes of each letter whose value is 2
    # only return words that have ALL green words
    green = []
    yellow = []
    for m in range(len(tup)):
        if tup[m][1] == 2:
            green.append((tup[m][0], m))
        if tup[m][1] == 1:
            yellow.append(tup[m][0])

    if len(green) == 0:
        return tempDict

    for w in tempDict:
        for ele in green:
            
            if green.index(ele) == len(green) - 1:
                if w[ele[1]] == ele[0]:
                    newDict.append(w)
                    break

            if w[ele[1]] == ele[0]:
                continue
            
            else:
                break
    return newDict  
    # return None

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

