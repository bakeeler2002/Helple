class possibleWords:
    def __init__(self):
        self.possibleWords = []
        self.getAllPossibleWords()
    
    def getAllPossibleWords(self):
        file = open("words.txt", "r")
        for line in file:
            line = line[:len(line)-3]
            words = line.split('\t')
            for word in words:
                if word != '' and word != ' ':
                    self.possibleWords.append(word)

    def getPossibleWords(self):
        return self.possibleWords
    
    def getBestStartingWord(self):
        # Calculate best starting word

        return "dont know yet"

class CharState:
    UNAVAILABLE = 0
    DIFFERENT_SPOT = 1
    CORRECT = 2
    AVAILABLE = 3
    
class possibleChars:
    def __init__(self):
        self.possibleChars = {}
        self.setPossibleChars()

    def setPossibleChars(self):
        allChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for c in allChars:
            self.possibleChars[c] = CharState.AVAILABLE

    def getPossibleChars(self):
        return self.possibleChars
    
    def updateChar(self, char, state):
        self.possibleChars[char] = state
    

# main
possWords = possibleWords()

possChars = []
for i in range(0, 5):
    possChars.append(possibleChars())
#print(possibleWords.getPossibleWords())

print("Welcome to Helple, the Wordle helper. Solve your daily Wordle with this application and get the words with the highest possibility of being the correct word.")
print("The best possible starting word is: ", possWords.getBestStartingWord())

while True:
    print("Enter chosen Wordle word: ", end="")
    word = input()

    print("Enter results of Wordle guess (0 = unavailable, 1 = yellow, 2 = green) with format 22222 if word is correct, for example: ", end="")
    new_info = input()


    if new_info == '22222':
        print("YAY")


    for i in range(0, len(word)):
        # update accordingly
        print(word[i], "   r  ", new_info[i])
        if new_info[i] == 0:
            for u in range(0, 5):
                possChars[u].updateChar(word[i], new_info[i])
        else: 
            possChars[i].updateChar(word[i], new_info[i])

    #print(word, " ", new_info)
    possible_words = possWords.getPossibleWords()
    #possible_chars = possChars.getPossibleChars()
    #print(possible_chars)
    print(possChars[3].getPossibleChars())
    print()
    print(len(possible_words))



