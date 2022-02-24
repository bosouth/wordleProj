data = open("valid.txt", "r")

#mark 0 if letter not in word 
# mark 1 if letter in word but not in right place
# mark 2 if letter in word at the right place

#modify data
words = data.readlines()
words = words[0].split(",")
words = [w.strip("\"") for w in words]

goalWord = words[0]
attempt = 1

print(goalWord)

