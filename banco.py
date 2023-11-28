import csv
import os

def read_user_data():
    # Read user data from the CSV file into a list of dictionaries
    if not os.path.exists('user_data.csv'):
        create_user_data_file()

    with open('user_data.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        user_data = list(reader)
    return user_data

def create_user_data_file():
    # Create the user data CSV file with header
    with open('user_data.csv', 'w', newline='') as file:
        fieldnames = ['username', 'balance']  # Adjust fieldnames based on your user data structure
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

def write_user_data(user_data):
    with open('user_data.csv', 'w', newline='') as file:
        fieldnames = ['username', 'balance']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(user_data)

def deposit_money(username, amount):
    user_data = read_user_data()

    user_index = next((index for (index, user) in enumerate(user_data) if user['username'] == username), None)

    if user_index is not None:
        user_data[user_index]['balance'] = str(float(user_data[user_index]['balance']) + amount)

        write_user_data(user_data)

        print(f"Deposit successful. New balance for {username}: {user_data[user_index]['balance']}")
    else:
        print(f"User '{username}' not found.")
