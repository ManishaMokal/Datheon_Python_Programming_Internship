# Hangman Word Guessing Game

## Project Overview
This project is a console-based Hangman Word Guessing Game developed using Python as part of the Datheon Python Programming Internship.

The player tries to guess a randomly selected English word, one letter at a time, with a maximum of six incorrect attempts.

## Features
- Random word selection from a provided English word list.
- Displays hidden letters using underscores.
- Reveals correctly guessed letters.
- Allows up to six incorrect guesses.
- Displays ASCII hangman drawings.
- Prevents repeated guesses from reducing attempts.
- Validates user input.
- Displays victory and defeat messages.

## Technologies Used
- Python 3
- Python Standard Library (`random`)
- Text file handling
- Git and GitHub

## Project Files
- `hangman.py` — Main Python program containing the game logic.
- `words.txt` — English word list used to select the secret word.
- `README.md` — Project documentation.

## How to Run
1. Install Python 3.
2. Download or clone this repository.
3. Ensure `hangman.py` and `words.txt` are in the same folder.
4. Open a terminal in that folder.
5. Run the following command:

python hangman.py


## How to Play
1. Run the program.
2. Read the underscores displayed for the hidden word.
3. Enter one alphabet letter at a time.
4. Correct guesses reveal letters in the word.
5. Incorrect guesses reduce the remaining attempts and update the hangman drawing.
6. Guess the complete word before your attempts run out to win.
