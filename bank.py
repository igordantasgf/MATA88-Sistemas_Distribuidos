import csv
import os

from operations import Operations


class Bank:
    def read_user_data(self):
        # Read user data from the CSV file into a list of dictionaries
        if not os.path.exists("user_data.csv"):
            self.create_user_data_file()

        with open("user_data.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            user_data = list(reader)
        return user_data

    def create_user_data_file():
        # Create the user data CSV file with header
        with open("user_data.csv", "w", newline="") as file:
            fieldnames = [
                "client_id",
                "balance",
            ]  # Adjust fieldnames based on your user data structure
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    def write_user_data(self, user_data):
        with open("user_data.csv", "w", newline="") as file:
            fieldnames = ["client_id", "balance"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(user_data)

    def perform_operation(self, client_id, operation, amount, recipient_account):
        match operation:
            case Operations.DEPOSIT:
                return self.deposit_money(client_id, amount)
            case Operations.WITHDRAW:
                return self.withdraw_money(client_id, amount)
            case Operations.TRANSFER:
                return self.transfer_money(client_id, amount, recipient_account)
            case _:
                return print("Operação inválida, tente novamente")

    def withdraw_money(self, client_id, amount):
        # Read user data
        user_data = self.read_user_data()

        # Find the user in the data
        user_index = next(
            (
                index
                for (index, user) in enumerate(user_data)
                if user["client_id"] == client_id
            ),
            None,
        )

        if user_index is not None:
            balance = float(user_data[user_index]["balance"])
            if balance < float(amount):
                return f"Saldo insuficiente para o saque. Saldo disponível: {balance} reais"

            # Update user balance
            user_data[user_index]["balance"] = str(balance - float(amount))
        else:
            return "Conta do usuário não encontrada, por favor faça um depósito para abrir sua conta"

        # Write the updated user data back to the CSV file
        self.write_user_data(user_data)

        print(
            f"Update successfully. New balance for {client_id}: {user_data[-1]['balance']}"
        )
        return f"Saque de {amount} reais realizado com sucesso. Novo saldo: {user_data[-1]['balance']} reais"

    def deposit_money(self, client_id, amount):
        # Read user data
        user_data = self.read_user_data()

        # Find the user in the data
        user_index = next(
            (
                index
                for (index, user) in enumerate(user_data)
                if user["client_id"] == client_id
            ),
            None,
        )

        if user_index is not None:
            # Update user balance
            user_data[user_index]["balance"] = str(
                float(user_data[user_index]["balance"]) + float(amount)
            )
        else:
            # If user not found, create a new entry
            new_user = {"client_id": client_id, "balance": str(amount)}
            user_data.append(new_user)

        # Write the updated user data back to the CSV file
        self.write_user_data(user_data)

        print(
            f"Update successfully. New balance for {client_id}: {user_data[-1]['balance']}"
        )
        return f"Depósito de {amount} reais realizado com sucesso. Novo saldo: {user_data[-1]['balance']} reais"

    def transfer_money(self, client_id, amount, recipient_account):
        # Read user data
        user_data = self.read_user_data()

        # Find the user in the data
        user_index = next(
            (
                index
                for (index, user) in enumerate(user_data)
                if user["client_id"] == client_id
            ),
            None,
        )

        recipient_index = next(
            (
                index
                for (index, user) in enumerate(user_data)
                if user["client_id"] == recipient_account
            ),
            None,
        )

        if user_index is not None and recipient_index is not None:
            balance = float(user_data[user_index]["balance"])
            if balance < float(amount):
                return f"Saldo insuficiente para a transferência. Saldo disponível: {balance} reais"

            # Update user balance
            user_data[user_index]["balance"] = str(balance - float(amount))

            user_data[recipient_index]["balance"] = str(
                float(user_data[recipient_index]["balance"]) + float(amount)
            )
            # Write the updated user data back to the CSV file
            self.write_user_data(user_data)
            return "Transferência de {amount} reais realizada para a conta {recipient_account} com sucesso. Novo saldo:  reais"

        elif user_index is None:
            return "Conta do usuário não encontrada. Por favor, faça um depósito para abrir sua conta"

        elif recipient_account is None:
            return "Conta do destinatário não encontrada. Verifique os digitos e tente novamente "

        print(
            f"Update successfully. New balance for {client_id}: {user_data[-1]['balance']}"
        )
