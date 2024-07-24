# Helple : Blake Keeler
# This is a Wordle helper which, given the information you provide from Wordle,
# will let you know the remaining number of solutions along with giving you
# those words. Based on narrowing down the possible solutions, it is very unlikely
# to be unable to solve the daily Wordle now.
# This project also gives you a good list of starting words which cover the most
# common character among the possible solutions.


# Each position (0-4) of a word can be a letter from A-Z
allChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class possibleWords:
    def __init__(self):
        self.possibleWords = []
        self.getAllPossibleWords()
    
    def getAllPossibleWords(self):
        # .txt file of all available Wordle words
        file = open("words.txt", "r")
        for line in file:
            # remove \n
            line = line[:len(line)-1]
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
            print("Characters with the highest frequency: ", sorted_amounts)
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
        
    def updatePossibleWords(self, unavailable, available_diff_spot, correct):
        updated_words = []

        for word in self.possibleWords:
            add_flag = True

            # grey characters : not in word
            for u in unavailable:
                if u in word:
                    add_flag = False
                
            # yellow characters : in word but different positions
            for char, position in available_diff_spot.items():
                if word[position] == char:
                    add_flag = False
                
                # must still be in the word
                if char not in word:
                    add_flag = False

            # green characters : in word AT same position
            for char, position in correct.items():
                if word[position] != char:
                    add_flag = False

            if add_flag:
                updated_words.append(word)
            
        self.possibleWords = updated_words
        return updated_words

# main
def main():
    possWords = possibleWords()

    print("Welcome to Helple, the Wordle helper. Solve your daily Wordle with this application and get the words with the highest possibility of being the correct word.")
    print("Some good starting words are: ", possWords.getBestStartingWords("other"))

    num_guesses = 1

    while num_guesses <= 6:
        print("Enter chosen Wordle word: ", end="")
        word = input().lower()

        print("Enter results of Wordle guess (0 = unavailable/grey, 1 = yellow, 2 = green) with format 22222 if word is correct, for example: ", end="")
        new_info = input()

        if new_info == '22222':
            print("Congrats on solving the Wordle! This was done in ", num_guesses, " attempts. See ya tomorrow!")
            exit(0)


        # Our constraints data structures to limit the number of possible words remaining
        unavailable = []
        # {char : spot not in}
        available_diff_spot = {}
        correct = {}

        # Narrow down which characters are and are not in which positions
        for i in range(0, len(word)):
            # update accordingly
            if new_info[i] == '0':
                # The character is NOT in any spot. 
                if word[i] not in correct.keys():
                    unavailable.append(word[i])
            elif new_info[i] == '1':
                # The character is available, just in a different spot. So not this one.
                available_diff_spot[word[i]] = int(i)
            elif new_info[i] == '2':
                # The character IS in this spot. So, every other character here is impossible.
                # We can only update this spot because the same character can be repeated in other spots.
                correct[word[i]] = int(i)
            else:
                print("Uh oh! This input is invalid!")
                exit(0)

        possible_words = possWords.updatePossibleWords(unavailable, available_diff_spot, correct)
        print()
        print("Number of possible words remaining: " + str(len(possible_words)) + ". Next word suggestions: ", possible_words[:15])

        num_guesses += 1
    
    print("Uh oh! Too many guesses on this Wordle! The word was: ", possible_words, ". Try again tomorrow!")


if __name__ == "__main__":
    main()

