import random as rand
import numpy as np

data = open("words.txt", "r")

#6 chances to guess secret 5 letter word

# mark 0 if letter not in word
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
    solArray = [('', 0), ('', 0), ('', 0), ('', 0), ('', 0)]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabetCount = np.zeros(26)
    greenTrack = []
    for letter in sol:
        alphabetCount[alphabet.index(letter)] += 1

    # green check
    for ele in guess:
        if ele == sol[i]:
            solArray[i]=(ele, 2)
            alphabetCount[alphabet.index(ele)] -= 1
            greenTrack.append(i)
        i += 1

    # yellow/gray check
    i = 0
    for ele in guess:
        if i in greenTrack:
            i += 1
            continue
        if ele in sol and alphabetCount[alphabet.index(ele)] > 0:
            solArray[i]=(ele, 1)
            alphabetCount[alphabet.index(ele)] -= 1
        else:
            solArray[i]=(ele, 0)
        i += 1

    return solArray

def indexConvert(wordIn, ans):
    convertThis = compare(wordIn, ans)
    sum = 0
    for i in range(5):
        sum += 3**i * int(convertThis[i][1])
    return sum

def entropyCalc(dictIn, ans):
    values = np.zeros(3**5)
    for word in dictIn:
        values[indexConvert(word, ans)] += 1
    for i in range(len(values)):
        values[i] = values[i] / len(dictIn)
    sum = 0
    for prob in values:
        if prob == 0:
            continue
        sum += -prob*np.log2(prob)
    return sum


def newDictionary(tup, d, guess):
    green = []
    greenLetters = []
    yellow = []
    gray = []

    for m in range(len(tup)):
        if tup[m][1] == 2:
            green.append((tup[m][0], m))
            greenLetters.append(tup[m][0])
        if tup[m][1] == 1:
            yellow.append(tup[m][0])
        if tup[m][1] == 0:
            gray.append(tup[m][0])

    newDict = []
    zeroDict = []
    noZerosDict = []
    
    for w in d:
        for ele in gray:
            if ele in w:
                if greenLetters.count(ele) > 0: 
                    if w.count(ele) == greenLetters.count(ele) + 1:
                        zeroDict.append(w)
                    else:
                        continue
                if yellow.count(ele) > 0:
                    if w.count(ele) == yellow.count(ele) + 1:
                        zeroDict.append(w)
                    else:
                        continue
                else:
                    zeroDict.append(w)
                
    noZerosDict = list(set(d).difference(zeroDict))

    if len(green) == 0 and len(yellow) == 0:
        return noZerosDict

    for w in noZerosDict:
        t = w
        if len(green) == 0:
            for ele in yellow:
                if ele not in t:
                    break
                elif yellow.index(ele) == len(yellow) - 1:
                    newDict.append(w)
        for ele in green:
            if w[ele[1]] == ele[0]:
                t = t.replace(ele[0], "", 1)
                if green.index(ele) == len(green) - 1 and checkYellows(yellow, t) == True:
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
goalWord = "plant"
attempt = 1

# guess = "floss"
while attempt < 7:
    print(len(words))
    r = rand.randint(0, len(words) -1)
    guess = words[r]
    # if attempt == 1:
    #     guess = "flail"
    print(guess)
    if isValidWord(guess, words) == False:
        print("Invalid word")
        break

    #compare
    tup = compare(goalWord, guess)

    # return dictionary with remaining valid words
    new = newDictionary(tup, words, guess)

    entropies = np.zeros(len(new))
    # for i in range(len(new)):
    #     entropies[i] = entropyCalc(newDictionary(tup, new, new[i]), goalWord)

    print(new)
    words = new
    # print(entropies)
    # guess = new(np.argmax(entropies))

    # use knn to determine closest word, rinse and repeat
    
    attempt += 1

