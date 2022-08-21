import config
import random


print('Welcome to Wheel of Fortune')


wheel_list = ['Bankrupt','Lose a Turn', 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]
vowels = {"a", "e", "i", "o", "u"}

#initializing variables
word_archive = []
game_total = [0,0,0]

# getting the dictionary
def get_dictionary():
    global dictionary
    dictionary_loc = getattr(config,'dictionary_loc', 'not_found')
    dictionary_file = open(dictionary_loc).read()
    dictionary = dictionary_file.replace('\n',',').split(',')


#user can input names
def get_names():
    global players
    players = []
    for i in range(3):
        name = str(input(f'Enter the name of player {1+i}: '))
        players.append(name)


#printing text with a underline
def print_with_underline(string):
    print(string)
    underline = '='*len(string)
    print(underline)

def print_rules():
    rules_loc = getattr(config,'rules_loc', 'not_found')
    rules = open(rules_loc).read()
    print_with_underline('Rules')
    print(rules)

#printing the choices the player has at the begining of each turn
def print_choices():
    print_with_underline('Choices')
    print('1. Spin the wheel')
    print('2. Buy a vowel')
    print('3. Solve the puzzle')


#making sure the player only puts in a single letter whn guessing a letter
def valid_letter():
    guess = str(input('Guess a letter: '))
    while (not guess.isalpha()) or (len(guess)>1):
        print('You must guess a single letter. Try again')
        guess = str(input('Guess a letter: '))
    return guess


#making sure the guess is a consonant
def get_consonant():
    guess = valid_letter()
    while guess in vowels:
        print('That is a vowel. Please guess a consanant')
        guess = valid_letter()
    return guess


#making sure the guess is a vowel
def get_vowel():
    guess = valid_letter()
    while guess not in vowels:
        print('That is not a vowel. Try again.')
        guess = valid_letter()
    return guess


#getting a valid integer
def get_int(string):
    is_valid = False
    while not is_valid:
        try:
            num = int(input(string))
            is_valid = True
        except:
            print('That is not a number')
    return num


#getting a valid choice (number 1-3)
def get_choice():
    choice = get_int('What would you like to do?')
    while (choice < 1) or (choice > 3):
        print('Please pick a valid number (1, 2, or 3)')
        choice = get_int('What would you like to do? ')
    return choice


#gets a word form the dictionary that hasn't been used
def get_word():
    global word_archive #list of words used in the game
    round_word = random.choice(dictionary)
    while round_word in word_archive:
        round_word = random.choice(dictionary)
    
    word_archive.append(round_word)
    return round_word

#displaying the word as a string
def display_word():
    blank_string = ''
    for space in blank_word:
        blank_string += space
    print_with_underline(blank_string) 

#checking if letters in a list are in a word (used in final round)
def check_list(list_of_letters):
    for i in list_of_letters:
        for j in range(len(round_word)):
            if round_word[j] == i:
                blank_word[j] = i
    display_word()


#checking to see if a letter is in a word
def check_guess(guess):
    global success
    if guess in round_word:
        for i in range(len(round_word)):
            if round_word[i] == guess:
                blank_word[i] = guess
                display_word()
        success = True
    else:
        print('That letter is not in the word')
        success = False


#guessing a letter (consonant)
def guess_letter():
    guess = get_consonant()
    while guess in guessed_letters:
        print('That letter has already been guessed')
        guess = get_consonant()
    guessed_letters.append(guess)
    check_guess(guess)


#spinning the wheel and guessing a letter
def spin_wheel(player):
    global success
    spin = random.choice(wheel_list)
    if spin == 'Bankrupt':
        print('You went Bankrupt.')#remove money from round total
        round_total[player] = 0
        success = False

    elif spin == 'Lose a Turn':
        print('You lost a turn')#go to the next player
        success = False

    else:
        print(f'You spun ${spin}')#give the player the choice to guess a letter or word
        guess_letter() #guessing a letter
        if success:
            round_total[player] = round_total[player] + spin #adding money to players bank
 

#buying a vowel
def buy_vowel(player):
    if round_total[player] >= 250: #if the player has enough money
        guess = get_vowel()
        while guess in guessed_letters:
            print('That letter has already been guessed')
            guess = get_vowel()
        guessed_letters.append(guess) #add to list of already guessed letters
        round_total[player] = round_total[player]-250 #removing money from the bank
        check_guess(guess)
    else:
        print('You do not have enough money to buy a vowel.')


#making sure the guess is a word (not numeric)
def valid_word():
    guess = str(input('Guess a word: '))
    while not guess.isalpha():
        print('Please guess a single word with no numbers or spaces: ')
        guess = str(input('Guess a word: '))
    return guess


#guessing a word
def guess_word():
    global success
    global blank_word
    guess = valid_word()
    if guess == round_word:
        print('Thats the word!')
        for i in range(len(round_word)):
            blank_word[i] = round_word[i] #breaks the while loop in game play
        success = False
        guessed = True #allows prize money to be added in the final round
    else:
        print('That is not the word')
        success = False
    return guessed #allows prize money to be added in the final round

#one turn
def turn(player):
    global success
    success = True
    while success: #keep going while the player is successful
        print_choices()
        choice = get_choice()
        print_with_underline('Here is your hint')
        display_word()
        if choice == 1: #spin the wheel and guess a letter
            spin_wheel(player)
        elif choice == 2: #buy a vowel
            buy_vowel(player)
        elif choice == 3: #guess a word
            guess_word()
        else:
            print('That is not a valid choice.')
            continue
        print_with_underline(f'Your round total is ${round_total[player]}')
    print_with_underline('End of turn')

#one round
def round():

    global round_word
    global blank_word
    global round_total
    global game_total
    global guessed_letters 

    #getting the word and filling a list with blank spaces
    round_word = get_word()
    blank_word = ['_ ']* len(round_word)

    #resetting the round total and guessed letters
    round_total = [0,0,0]
    guessed_letters = []

    #getting the player
    player = random.choice(range(3))

    while '_ ' in blank_word:
        player += 1
        player = player%3
        print_with_underline(f"It's {players[player]}'s turn")
        print_with_underline(f'HINT: the word is {round_word} (kept in for testing/grading ease!)')
        print_with_underline('Here is your hint')
        display_word()
        turn(player)
        
    print_with_underline('End of round')

    #show round totals
    print(f'Player\t\tRound Total')
    for i in range(len(round_total)):
        print(f'{players[i]}\t\t{round_total[i]}')


    #The player who guessed wins the round
    print(f'{players[player]} won this round. Their round total will be added to their total winnings for the game')
    game_total[player] = game_total[player]+round_total[player]

    #show the game totals to this point
    print_with_underline('Game totals so far')
    print(f'Player\t\tGame Total')
    for i in range(len(round_total)):
        print(f'{players[i]}\t\t{game_total[i]}')
    
#playing the final round
def final_round():

    global round_word
    global blank_word
    prize = 1000

    #selecting the player
    player = game_total.index(max(game_total))
    print(f'{players[player]} is going on to the final round!')
    print(f'The cash prize for this round is ${prize}!')

    #get the word and fill out the blanks in a list
    round_word = get_word()
    blank_word = ['_ ']*len(round_word)

    #list of player guesses
    extra_guesses = []

    #list of given letters
    given_letters = ['r','s','t','l','n','e']

    #checking the list for letters that are in the word
    check_list(given_letters)

    print(f'HINT: the word is {round_word} (left in for testing/grading ease!)')

    #get input for letters
    print('You can now pick 3 consanents and 1 vowel')
    print_with_underline('Pick your consonants')
    for i in range(3):
        consonant = get_consonant()
        while consonant in given_letters:
            print('That letter was already given. Pick again.')
            consonant = get_consonant()
        extra_guesses.append(consonant)

    print_with_underline('You can now pick your vowel')
    for i in range(1):
        vowel = get_vowel()
        while vowel in given_letters:
            print('That letter was already given Pick again')
            vowel = get_vowel()
        extra_guesses.append(vowel)


    check_list(extra_guesses)
    win = guess_word()
    
    if win:
        print(f'You won! ${prize} will be added to your total winnings!')
        game_total[player] = game_total[player] + prize
        print(f'Congratulations {players[player]}!')
    else:
        print(f'Sorry. The word was {round_word}.')

    #printing the final results
    print_with_underline('Here are the final results!')
    print(f'Player\t\tGame Total')
    for i in range(len(round_total)):
        print(f'{players[i]}\t\t{game_total[i]}')


#main game play function
def play_game():
    num_rounds = 1
    get_dictionary()
    get_names()
    print_rules()
    while num_rounds < 3:
        round()
        num_rounds +=1
    final_round()
    print('Thanks for playing!')

play_game()
