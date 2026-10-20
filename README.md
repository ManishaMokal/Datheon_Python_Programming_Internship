# Datheon Python Programming Internship

This repository contains Python projects completed as part of the Datheon Python Programming Internship.

## Task 1: Hangman Game

A word-guessing game where the player guesses letters to find a hidden word within a limited number of attempts.

**Features**
- Random word selection
- Letter-by-letter guessing
- Tracks incorrect guesses
- Displays the game result

**Run the program**
```bash
python hangman.py
```

## Task 2: Stock Portfolio Performance Tracker

A Python program that tracks stock investments and calculates portfolio performance using the latest available stock closing prices from Yahoo Finance.

**Features**
- Validates stock symbols using `constituents.csv`
- Accepts purchase prices and share quantities
- Fetches the latest available stock closing prices using `yfinance`
- Calculates investment value, market value, gain/loss, and return percentage
- Saves portfolio results to `portfolio_summary.csv`

**Requirements**
- Python 3
- Internet connection
- `yfinance` library

**Install the required library**
```bash
python -m pip install yfinance
```

**Run the program**

python portfolio.py


Enter a valid ticker symbol, purchase price, and share quantity. Type `done` when you have finished entering stocks.

The program generates `portfolio_summary.csv` containing the calculated portfolio results.

## Project Files

- `hangman.py` — Hangman game source code
- `words.txt` — Words used by the Hangman game
- `portfolio.py` — Stock portfolio tracker source code
- `constituents.csv` — Stock symbols used for validation
- `portfolio_summary.csv` — Generated portfolio report