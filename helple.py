allChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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
    
    def getBestStartingWords(self, option):
        # Calculate the best starting words

        if option == "recommended":
            # Some starting words that are known to be good openers
            return ["CRANE", "SAUCY", "SLATE"]
        else:
            # Calculate the most common characters, so opening words can be given which provide the most information possible
            chars = {}

            for c in allChars:
                # char : {index: num_times}
                chars[c] = 0

            # get character frequencies
            for word in self.possibleWords:
                unique = set()
                for i in range(0, len(word)):
                    unique.add(word[i])

                for item in unique:
                    chars[item] += 1

            # Characters with the highest frequency are first in the dict
            sorted_amounts = sorted(chars.items(), key = lambda item : item[1], reverse=True)

            amounts = {}

            for i in range(len(sorted_amounts)):
                char, amount = sorted_amounts[i]

                amounts[char] = [amount, i]

            print()
            # This dict is the same as before, but includes the index; The lower the index, the more frequent the character (ranking)
            print("Characters with the highest frequency: ", amounts)
            print()

            # Now we're gonna check the words again. We will add up the ranks of the characters included, 
            # and the words with the lowest combined ranking will have the most common characters.
            
            words = {}

            for word in self.possibleWords:
                rankings = 0
                unique = set()
                for i in range(len(word)):
                    rankings += amounts[word[i]][1]

                    unique.add(word[i])
                    
                words[word] = rankings

                if len(unique) != 5:
                    # Not eligible because repeat characters, so let's toss it out
                    words[word] += 1000

            # Finally return the 5 best starting words in terms of:
            # 1) Unique characters
            # 2) The most common characters are included
            return list(dict(sorted(words.items(), key = lambda item : item[1])).keys())[:5]
        
    def updatePossibleWords(self):
        pass


class CharState:
    UNAVAILABLE = 0
    DIFFERENT_SPOT = 1
    CORRECT = 2
    AVAILABLE = 3
    
class possibleChars:
    # This is a dict of characters corresponding to a position in the input. 
    # Many characters can get eliminated from a spot based on provided information.
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
def main():
    possWords = possibleWords()

    possChars = []
    for i in range(0, 5):
        possChars.append(possibleChars())

    print("Welcome to Helple, the Wordle helper. Solve your daily Wordle with this application and get the words with the highest possibility of being the correct word.")
    print("Some good starting words are: ", possWords.getBestStartingWords("other"))

    num_guesses = 1
    while num_guesses <= 6:
        print("Enter chosen Wordle word: ", end="")
        word = input().lower()

        print("Enter results of Wordle guess (0 = unavailable/grey, 1 = yellow, 2 = green) with format 22222 if word is correct, for example: ", end="")
        new_info = input()

        if new_info == '22222':
            print("Congrats on solving the Wordle! This was done in " + num_guesses + " attempts. See ya tomorrow!")

        # Narrow down which characters are and are not in which positions
        for i in range(0, len(word)):
            print(new_info[i])
            # update accordingly
            if new_info[i] == '0':
                # The character is NOT in any spot. So we can add this info to our possChars list.
                for u in range(0, 5):
                    possChars[u].updateChar(word[i], new_info[i])
            elif new_info[i] == '1':
                # The character is available, just in a different spot. So not this one.
                possChars[i].updateChar(word[i], new_info[i])
            elif new_info[i] == '2':
                # The character IS in this spot. So, every other character here is impossible.
                # We can only update this spot because the same character can be repeated in other spots.
                for char, _ in allChars.items():
                    if char == word[i]:
                        possChars[i].updateChar(word[i], new_info[i])
                    else:
                        possChars[i].updateChar(char, 0)
            else:
                print("Uh oh! This input is invalid!")
                exit(0)


        possWords.updatePossibleWords()

        possible_words = possWords.getPossibleWords()
        #print(possChars[3].getPossibleChars())
        print()
        print(len(possible_words))


        num_guesses += 1
    
    print("Uh oh! Too many guesses on this Wordle! The word was: " + possWords.getPossibleWords() + ". Try again tomorrow!")



if __name__ == "__main__":
    main()


