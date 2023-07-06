
import time
import json
import requests
import yfinance as yf
# Global variables
users = {}




def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    
    if len(data) > 0:
        price = data["Close"].iloc[-1]
        return price
    else:
        return None
    time.sleep(5)

def save_data():
    with open('data.json', 'w') as file:
        json.dump(users, file)


def load_data():
    global users
    try:
        with open('data.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        pass


def register():
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists. Please choose a different username.")
        return

    password = input("Enter a password: ")
    users[username] = {'password': password, 'portfolio': {}, 'balance': 1000}
    save_data()
    print("Registration successful! please login")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username]['password'] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None











        


def buy_stock(username):
    stock_symbol = input("Enter the stock symbol: ")
    quantity = int(input("Enter the quantity: "))

    stock_price = get_stock_price(stock_symbol)
    if stock_price is None:
        print("Failed to fetch stock price. Please try again later.")
        return

    total_cost = stock_price * quantity
    if total_cost > users[username]['balance']:
        print("Insufficient funds.")
        return

    if stock_symbol in users[username]['portfolio']:
        users[username]['portfolio'][stock_symbol] += quantity
    else:
        users[username]['portfolio'][stock_symbol] = quantity

    users[username]['balance'] -= total_cost
    save_data()
    print(f"You bought {quantity} shares of {stock_symbol}.")


def sell_stock(username):
    stock_symbol = input("Enter the stock symbol: ")
    quantity = int(input("Enter the quantity: "))

    if stock_symbol not in users[username]['portfolio'] or users[username]['portfolio'][stock_symbol] < quantity:
        print("You do not own enough shares of the stock.")
        return

    stock_price = get_stock_price(stock_symbol)
    if stock_price is None:
        print("Failed to fetch stock price. Please try again later.")
        return

    total_sale = stock_price * quantity
    users[username]['portfolio'][stock_symbol] -= quantity
    users[username]['balance'] += total_sale
    save_data()
    print(f"You sold {quantity} shares of {stock_symbol}.")


def view_portfolio(username):
    print("Portfolio:")
    portfolio = users[username]['portfolio']
    balance = users[username]['balance']
    print("Balance = ",balance)
    if not portfolio:
        print("No stocks in portfolio.")
        return

    for stock_symbol, quantity in portfolio.items():
        print(f"{stock_symbol}: {quantity} shares")


# Main program
load_data()

while True:
    print("\n---- Stock Trading Game ----")
    print("1. Register")
    print("2. Login")

    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        register()
    elif choice == '2':
        username = login()
        if username:
            while True:
                print("\n---- Stock Trading Game Menu ----")
                print("1. Buy Stock")
                print("2. Sell Stock")
                print("3. View Portfolio")
                print("4. Exit")
                

                user_choice = input("Enter your choice (1-5): ")

                if user_choice == '1':
                    buy_stock(username)
                elif user_choice == '2':
                    sell_stock(username)
                elif user_choice == '3':
                    view_portfolio(username)
               
                elif user_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
    else:
        print("Invalid choice. Please try again.")
