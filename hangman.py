"""
hangman game

"""

import random

import hangman_gallows as gallows

# -----------------------------------
# global constants
WORDLIST_FILENAME = "words.txt"
ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
VOWELS = 'aeiou'
MAX_GUESSES = 6


# end of global constants
# -----------------------------------

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)


def load_words():
    """
    Reads the words from the words file into a list.

    :return: A list of words that are all lowercase.
    :rtype: list
    """
    print("Loading word list from file...")
    with open(WORDLIST_FILENAME, 'r', encoding="utf8") as word_file:
        line = word_file.readline()
    word_file.close()

    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return tuple(wordlist)


def choose_word(word_list):
    """
    Chooses a word at random from the word_list

    :param word_list: a list of words
    :type word_list: list
    :return: a word chosen at random from the word_list
    :rtype: str
    """
    return random.choice(word_list)


# end of helper code
# -----------------------------------


def is_word_guessed(secret_word, letters_guessed):
    """
    Determines if all the letters in the secret_word have been guessed.
    Iterates over each letter in the secret_word to check if the letter is
    in letters_guessed.

    :param secret_word: the word the user is guessing; assumes all letters are lowercase
    :type secret_word: str
    :param letters_guessed: the lowercase letters that have been guessed
    :type letters_guessed: str
    :return: True if all the letters of secret_word are in letters_guessed; False otherwise
    :rtype: bool
    """
    letters_found = 0
    for letter in secret_word:
        if letter in letters_guessed:
            letters_found += 1

    return letters_found == len(secret_word)


def get_guessed_word(secret_word, letters_guessed):
    """
    This function creates a guessed_word that consists of '_ ' for each letter not
    yet guessed and letters that have been guessed.

    :param secret_word: the word the user is guessing
    :type secret_word: str
    :param letters_guessed: letters that have been guessed so far
    :type letters_guessed: str
    :return: the word comprised of letters, underscores (_),
    and spaces that represents which letters in
    secret_word have and have not been guessed
    :rtype: str
    """
    letters_found = []
    for letter in secret_word:
        if letter in letters_guessed:
            letters_found.append(letter)
    user_answer = ''
    for letter in secret_word:
        if letter in letters_found:
            user_answer += letter
        else:
            user_answer += '_ '
    return user_answer


def get_available_letters(letters_guessed):
    """
    Returns a string of letters that have not yet been guessed.

    :param: letters_guessed: letters that have been guessed so far by the player
    :type letters_guessed: str
    :return: letters that have not been guessed
    :rtype: str
    """
    letters_guessed = letters_guessed.lower()
    letters_remaining_list = []
    for letter in ALL_LETTERS:
        if letter not in letters_guessed:
            letters_remaining_list.append(letter)
    letters_remaining = ''
    for letter in letters_remaining_list:
        letters_remaining += letter
    return letters_remaining


def incorrect_guess(guessed_letter, guesses_remaining):
    """
    Call this function when the user makes a guess that is valid, but it doesn't
    match a letter in the secret word.

    The function supports Game Rules #5 and #6:
        5. Consonants: If the user inputs a consonant that hasn't been guessed
        and the consonant is not in the secret word, the user loses one guess.
        6. Vowels: If the vowel hasn't been guessed and the vowel is not in the
        secret word, the user loses two guesses.

    This function returns a new value for the number of guesses remaining.

    :param guessed_letter: the letter guessed by the player
    :type guessed_letter: str
    :param guesses_remaining: the guesses remaining before the incorrect guess
    :type guesses_remaining: int
    :return: the number of guesses remaining after an incorrect guess
    :rtype: int
    """
    if guessed_letter in VOWELS:
        guesses_remaining -= 2
    else:
        guesses_remaining -= 1

    guesses_remaining = max(guesses_remaining, 0)
    return guesses_remaining


def calculate_score(guesses_remaining, secret_word):
    """
    Calculates the user's score by multiplying the number of guesses_remaining times the
    number of unique letters in secret_word.

    :param guesses_remaining: the guesses remaining
    :type guesses_remaining: int
    :param secret_word: the word the player guessed
    :type secret_word: str
    :return: the calculated score if guesses_remaining is > 0; otherwise, 0
    :rtype: int
    """
    count = 0
    if guesses_remaining > 0:
        for letter in ALL_LETTERS:
            if letter in secret_word:
                count += 1
        user_score = guesses_remaining * count
    else:
        user_score = 0
    return user_score


def prompt_for_letter(guesses_remaining, available_letters):
    """
    Display the number of remaining guesses and the available letters
    Prompt the user to enter an available letter. Converts the letter to lowercase
    before returning it.

    Do not accept non-alphabetic characters or more than one letter.  Prompt until
    an available letter is entered.

    :param guesses_remaining: the guesses remaining before the incorrect guess
    :type guesses_remaining: int
    :param available_letters: available letters for the user to choose from
    :type available_letters: str
    :return: lowercase letter input by the user
    :rtype: str
    """
    print(f"You have {guesses_remaining} guesses left.")
    print(f"Available letters: {available_letters}")
    letter = input("Enter a letter: ")
    while True:
        if letter.isalnum() and len(letter) != 1:
            print("Enter one letter only.")
            letter = input("Enter a letter: ")
        elif letter.isdigit():
            print("Oops! That is not a valid letter.")
            letter = input("Enter a letter: ")
        while letter.lower() not in available_letters:
            print("The letter has already been guessed. Choose again.")
            letter = input("Enter a letter: ")
        return letter.lower()


def display_game_outcome(score, secret_word):
    """
    Displays the outcome of the game.
    If the score is greater than 0, display 'Congratulations, you won!'
    and the player's score. Otherwise, display 'Sorry, you ran out of guesses' and
    the secret word.

    :param score: the player's score
    :type score: int
    :param secret_word: the word the player is attempting to guess
    :type secret_word: str
    :return: None
    :rtype: None
    """
    if score > 0:
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {score}")

    else:
        print("Sorry, you ran out of guesses.")
        print(f"The word was {secret_word}")


def main():
    """
    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.
    * The user should start with 6 guesses
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the secret word.
    * After each guess, you should display to the user the
      partially guessed word so far.
    Follow the other limitations detailed in the problem write-up.
    """
    # load the words into a list
    wordlist = load_words()

    # choose a word from the word list
    secret_word = choose_word(wordlist)
    # you may want to uncomment the following line while testing the game.
    # print(secret_word)

    # used to track number of guesses remaining
    guesses_remaining = MAX_GUESSES

    # used to keep track of letters guessed.
    letters_guessed = ''

    # available letters (not yet guessed) for the player to choose from
    available_letters = get_available_letters(letters_guessed)
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    print("\nLet's play:", guessed_word)
    gallows.draw(0)
    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        user_guess = prompt_for_letter(guesses_remaining, available_letters)
        letters_guessed = letters_guessed + user_guess
        if user_guess not in secret_word:
            # The user's guess is incorrect
            guesses_remaining = incorrect_guess(user_guess, guesses_remaining)
            gallows.draw(MAX_GUESSES - guesses_remaining)
            print("Oops! That letter is not in my word: ", guessed_word)
        else:
            # The user correctly guessed a letter in the word
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print("Good guess: ", guessed_word)
        available_letters = get_available_letters(letters_guessed)
    score = calculate_score(guesses_remaining, secret_word)
    display_game_outcome(score, secret_word)


# -----------------------------------------
# Call the main function to start the game
# -----------------------------------------
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
