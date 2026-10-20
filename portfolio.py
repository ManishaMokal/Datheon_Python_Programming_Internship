
import csv
import os
from datetime import datetime

import yfinance as yf


# File names
CONSTITUENTS_FILE = "constituents.csv"
OUTPUT_FILE = "portfolio_summary.csv"


def load_valid_symbols():
    """Load valid stock symbols from the constituents CSV file."""
    symbols = set()

    try:
        with open(CONSTITUENTS_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                symbol = row.get("Symbol", "").strip().upper()
                if symbol:
                    symbols.add(symbol)

    except FileNotFoundError:
        print(f"Error: {CONSTITUENTS_FILE} was not found.")
        print("Keep constituents.csv in the same folder as portfolio.py.")
        return None

    return symbols


def get_current_price(symbol):
    """Fetch the latest available closing price from Yahoo Finance."""
    # Yahoo Finance uses hyphens for symbols such as BRK.B.
    yahoo_symbol = symbol.replace(".", "-")

    try:
        stock = yf.Ticker(yahoo_symbol)
        history = stock.history(period="5d", auto_adjust=False)

        if history.empty or "Close" not in history.columns:
            return None

        closing_prices = history["Close"].dropna()

        if closing_prices.empty:
            return None

        price = float(closing_prices.iloc[-1])

        if price <= 0:
            return None

        return price

    except Exception as error:
        print(f"Could not fetch the price for {symbol}: {error}")
        return None


def get_positive_number(prompt):
    """Ask for a number greater than zero."""
    while True:
        try:
            number = float(input(prompt))

            if number <= 0:
                print("Please enter a number greater than zero.")
                continue

            return number

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def collect_portfolio(valid_symbols):
    """Collect stock purchases and combine repeated purchases."""
    portfolio = {}

    print("\n=== STOCK PORTFOLIO TRACKER ===")
    print("Enter a stock symbol, or type 'done' to finish.\n")

    while True:
        symbol = input("Enter stock ticker symbol: ").strip().upper()

        if symbol.lower() == "done":
            break

        if not symbol:
            print("Please enter a ticker symbol.")
            continue

        if symbol not in valid_symbols:
            print("Symbol not found in constituents.csv. Try another symbol.")
            continue

        purchase_price = get_positive_number("Enter purchase price per share: ")
        quantity = get_positive_number("Enter number of shares: ")

        print(f"Fetching the latest available price for {symbol}...")
        current_price = get_current_price(symbol)

        if current_price is None:
            print("Price lookup failed. Check your internet connection and ticker.")
            print("This stock was not added. You can try entering it again.\n")
            continue

        print(f"Latest available closing price: ${current_price:,.2f}")

        if symbol in portfolio:
            old = portfolio[symbol]
            old_quantity = old["quantity"]
            new_quantity = old_quantity + quantity

            # Calculate the weighted average purchase price.
            average_price = (
                old["purchase_price"] * old_quantity
                + purchase_price * quantity
            ) / new_quantity

            portfolio[symbol] = {
                "purchase_price": average_price,
                "quantity": new_quantity,
                "current_price": current_price,
            }
        else:
            portfolio[symbol] = {
                "purchase_price": purchase_price,
                "quantity": quantity,
                "current_price": current_price,
            }

        print(f"{symbol} added successfully!\n")

    return portfolio


def calculate_results(portfolio):
    """Calculate investment, market value, and profit or loss."""
    results = []
    total_invested = 0
    total_market_value = 0

    for symbol, details in portfolio.items():
        purchase_price = details["purchase_price"]
        quantity = details["quantity"]
        current_price = details["current_price"]

        invested = purchase_price * quantity
        market_value = current_price * quantity
        gain_loss = market_value - invested
        return_percentage = (gain_loss / invested) * 100

        total_invested += invested
        total_market_value += market_value

        results.append({
            "Symbol": symbol,
            "Purchase Price": round(purchase_price, 2),
            "Quantity": quantity,
            "Current Price": round(current_price, 2),
            "Total Invested": round(invested, 2),
            "Market Value": round(market_value, 2),
            "Gain/Loss": round(gain_loss, 2),
            "Return Percentage": round(return_percentage, 2),
        })

    total_gain_loss = total_market_value - total_invested

    if total_invested:
        total_return = (total_gain_loss / total_invested) * 100
    else:
        total_return = 0

    return results, total_invested, total_market_value, total_gain_loss, total_return


def display_results(results, invested, market_value, gain_loss, return_percentage):
    """Display a readable portfolio summary in the terminal."""
    print("\n" + "=" * 90)
    print("PORTFOLIO PERFORMANCE SUMMARY")
    print("=" * 90)

    if not results:
        print("No stocks were added to the portfolio.")
        return

    print(
        f"{'Symbol':<10}"
        f"{'Buy Price':>12}"
        f"{'Quantity':>12}"
        f"{'Latest Price':>15}"
        f"{'Invested':>14}"
        f"{'Market Value':>16}"
        f"{'Gain/Loss':>14}"
    )
    print("-" * 93)

    for item in results:
        print(
            f"{item['Symbol']:<10}"
            f"{item['Purchase Price']:>12,.2f}"
            f"{item['Quantity']:>12,.2f}"
            f"{item['Current Price']:>15,.2f}"
            f"{item['Total Invested']:>14,.2f}"
            f"{item['Market Value']:>16,.2f}"
            f"{item['Gain/Loss']:>14,.2f}"
        )
        print(f"  Return: {item['Return Percentage']:.2f}%")

    print("-" * 93)
    print(f"Total invested:     ${invested:,.2f}")
    print(f"Total market value: ${market_value:,.2f}")
    print(f"Total gain/loss:    ${gain_loss:,.2f}")
    print(f"Total return:        {return_percentage:.2f}%")
    print("=" * 90)


def save_to_csv(results):
    """Save the portfolio summary to a CSV file."""
    if not results:
        print("\nNo portfolio data to save.")
        return

    fieldnames = [
        "Symbol",
        "Purchase Price",
        "Quantity",
        "Current Price",
        "Total Invested",
        "Market Value",
        "Gain/Loss",
        "Return Percentage",
    ]

    try:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nPortfolio summary saved to {OUTPUT_FILE}.")

    except OSError as error:
        print(f"\nCould not save the CSV file: {error}")


def main():
    valid_symbols = load_valid_symbols()

    if valid_symbols is None:
        return

    print(f"Loaded {len(valid_symbols)} valid stock symbols.")

    portfolio = collect_portfolio(valid_symbols)

    if not portfolio:
        print("\nNo stocks were added. Exiting program.")
        return

    results, invested, market_value, gain_loss, total_return = (
        calculate_results(portfolio)
    )

    display_results(
        results,
        invested,
        market_value,
        gain_loss,
        total_return,
    )

    save_to_csv(results)


if __name__ == "__main__":
    main()