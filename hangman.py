
import random

print("================================")
print("     HANGMAN WORD GUESSING GAME")
print("================================")


with open("words.txt", "r") as file:
    words = [
        line.strip().lower()
        for line in file
        if len(line.strip()) >= 2 and line.strip().isalpha()
    ]

secret_word = random.choice(words)


guessed_letters = []
attempts_left = 6

hangman_art = [
    """
     +---+
     |   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =========
    """
]

while attempts_left > 0:
    print(hangman_art[6 - attempts_left])

    print("\nWord: ", end="")
    for letter in secret_word:
        if letter in guessed_letters:
            print(letter, end=" ")
        else:
            print("_", end=" ")

    print("\nAttempts left:", attempts_left)

    guess = input("Guess a letter: ").lower().strip()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter one alphabet letter.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter!")
        continue

    guessed_letters.append(guess)

    if guess in secret_word:
        print("Correct guess!")
    else:
        attempts_left -= 1
        print("Wrong guess!")

    if all(letter in guessed_letters for letter in secret_word):
        print("\nCongratulations! You guessed the word!")
        print("The word was:", secret_word)
        break

if attempts_left == 0:
    print(hangman_art[6])
    print("\nGame over! You ran out of attempts.")
    print("The word was:", secret_word)