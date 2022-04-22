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
                if greenLetters.count(ele) > 0 and yellow.count(ele) > 0:
                    continue
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
            for idx, ele in enumerate(yellow):
                if ele not in t:
                    break
                elif idx == len(yellow) - 1:
                    newDict.append(w)
        for idx, ele in enumerate(green):
            if w[ele[1]] == ele[0]:
                t = t.replace(ele[0], "", 1)
                if idx == len(green) - 1 and checkYellows(yellow, t) == True:
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

r = rand.randint(0, len(words) - 1)
goalWord = words[r]
guesses_arr = []
attempt = 1


# baseline
def baseline():
    global words
    global goalWord
    attempt = 1
    while attempt < 10:
        q = rand.randint(0, len(words) - 1)
        guess = words[q]
        if guess == goalWord:
            print("the baseline guessed the word in " + str(attempt) + " tries.\n")
            break
        
        print("Guess is: " + guess)
        # if isValidWord(guess, allWords) == False:
        #     print("Invalid word")
        #     break
    
        #compare
        tup = compare(goalWord, guess)
    
        # return dictionary with remaining valid words
        new = newDictionary(tup, words, guess)
    
        # print(new)
        words = new
        
        
        attempt += 1

# data = open("words.txt", "r")
# words = data.readlines()
# words = words[0].split(",")
# words = [w.strip("\"") for w in words]

#oracle
def oracle():
    global words
    global goalWord
    attempt = 1
    while attempt < 10:
        if attempt == 1:
            for word in words:
                i = compare(goalWord, word)
                if i[0][1] == 2:
                    guess = word
        else:
            q = rand.randint(0, len(words) - 1)
            guess = words[q]
    
    
        if guess == goalWord:
            print("the oracle guessed the word in " + str(attempt) + " tries.\n")
            break
        
        print("Guess is: " + guess)
        # if isValidWord(guess, allWords) == False:
        #     print("Invalid word")
        #     break
    
        #compare
        tup = compare(goalWord, guess)
    
        # return dictionary with remaining valid words
        new = newDictionary(tup, words, guess)
    
        # entropies = np.zeros(len(new))
        # for i in range(len(new)):
        #     tup = compare(goalWord, new[i])
        #     entropies[i] = entropyCalc(newDictionary(tup, new, new[i]), goalWord)
    
        # print(new)
        
        words = new
        attempt += 1
    
# Using entropy to guess
def entropy_guess():
    global words
    global goalWord
    attempt = 1
    while attempt < 7:
        #print(len(words))
    
        if attempt == 1:
            entropies = np.zeros(len(words))
            for i in range(len(words)):
                tup = compare(goalWord, words[i])
                entropies[i] = entropyCalc(newDictionary(tup, words, words[i]), goalWord)
    
            #guess = words[np.argmax(entropies)]   
            # For using min entropy
            guess = words[np.argmin(entropies)]
    
        if attempt != 1:
            entropies = np.zeros(len(new))
            for i in range(len(new)):
                tup = compare(goalWord, new[i])
                entropies[i] = entropyCalc(newDictionary(tup, new, new[i]), goalWord)
    
            #guess = new[np.argmax(entropies)]
            # For using min entropy
            guess = new[np.argmin(entropies)]
    
        if isValidWord(guess, words) == False:
            print("Invalid word")
            break
        
        if guess == goalWord:
            print("Guess is: " + guess)
            print("entropy guessed the word in " + str(attempt) + " tries.\n")
            break
    
        print("Guess is: " + guess)
        #print(entropies)
    
        #compare
        tup = compare(goalWord, guess)
    
        # return dictionary with remaining valid words
        new = newDictionary(tup, words, guess)
    
        #print(new)
        words = new
    
        attempt += 1

def best_guess():
    global words
    global goalWord
    attempt = 1
    guess = "stale"
    while attempt < 20:
            
        #compare
        tup = compare(goalWord, guess)
    
        # return dictionary with remaining valid words
        new = newDictionary(tup, words, guess)
        if guess == "stale":
            print("First guess: " + guess)
       
        
        entropies2 = np.zeros(len(new))
        
        for j in range(len(new)):
            entropies = np.zeros(len(new))
            for i in range(len(new)):
                tup = compare(new[j], words[i])
                entropies[i] += entropyCalc(newDictionary(tup, new, new[i]), new[j])
               
            entropies2[j] = np.argmin(entropies)

        #guess = new[np.argmax(entropies)]
        # For using min entropy
        guess = new[np.argmin(entropies)]
    
        if isValidWord(guess, words) == False:
            print("Invalid word")
            break
        
        if guess == goalWord:
            print("Guess is: " + guess)
            print("entropy guessed the word in " + str(attempt) + " tries.\n")
            guesses_arr.append(attempt)
            #print(guesses_arr)
            break
    
        print("Guess is: " + guess)

        words = new
    
        attempt += 1       

# Loop for 100 times
tries = 1
words_permanent = words
attempt = 1
while tries < 101:
    words = words_permanent
    r = rand.randint(0, len(words) -1)
    goalWord = words[r]
   
    print("Try #" + str(attempt))
    print("Goal word is: " + goalWord)

    # Using baseline to guess
    #baseline()
    
    # Using oracle to guess
    #oracle()
    
    # Using entropy to guess
    #entropy_guess()
    
    # Best guess
    best_guess()
    
    attempt += 1    
    tries += 1

