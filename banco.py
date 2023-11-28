import csv
import os

class Banco:

    def read_user_data():
        # Read user data from the CSV file into a list of dictionaries
        if not os.path.exists('user_data.csv'):
            Banco.create_user_data_file()

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

    def update_money(_, username, amount):
        # Read user data
        user_data =  Banco.read_user_data()

        # Find the user in the data
        user_index = next((index for (index, user) in enumerate(user_data) if user['username'] == username), None)

        if user_index is not None:
            # Update user balance
            user_data[user_index]['balance'] = str(float(user_data[user_index]['balance']) + float(amount))
        else:
            # If user not found, create a new entry
            new_user = {'username': username, 'balance': str(amount)}
            user_data.append(new_user)

        # Write the updated user data back to the CSV file
        Banco.write_user_data(user_data)

        print(f"Update successfully. New balance for {username}: {user_data[-1]['balance']}")
