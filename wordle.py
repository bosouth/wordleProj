import random as rand

data = open("valid.txt", "r")

#6 chances to guess secret 5 letter word

#mark 0 if letter not in word 
# mark 1 if letter in word but not in right place
# mark 2 if letter in word at the right place

def compare(sol, guess):
    for i in len(guess):
        if guess[i] == sol[i]:
            #green
        elif guess[i] in sol:
            # yellow
        else:
            #gray
            #cannot use letter again

#modify data
words = data.readlines()
words = words[0].split(",")
words = [w.strip("\"") for w in words]

goalWord = words[1111]
attempt = 1

print(goalWord)

while attempt < 7:
    r = rand.randint(0, len(words) -1)

    guess = words[r]

    #compare

    print(guess)
    
    attempt += 1

