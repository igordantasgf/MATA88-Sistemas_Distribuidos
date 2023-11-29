import os
import socket
import threading
from datetime import datetime

from bank import Bank

from common import MESSAGE_DIVISOR
from operations import Operations, is_valid_operation

# Diretório para armazenar os estados dos relógios lógicos dos clientes
CLIENT_STATES_DIR = "client_states"

# Lista para armazenar as mensagens com timestamp e relógio lógico de Lamport
messages = []

# Dicionário para armazenar o estado do relógio lógico de cada cliente
client_states = {}

# Relógio lógico do servidor
lamport_clock = 0


def handle_client(client_socket, client_address, client_id):
    global lamport_clock

    # 1. Envia o identificador server-side do cliente para ele
    client_socket.send(client_id.encode("utf-8"))

    # 2. Envia o atual clock para o cliente
    client_socket.send(str(lamport_clock).encode("utf-8"))

    while True:
        try:
            # Recebe os dados do cliente
            data = client_socket.recv(1024)
            if not data:
                break

            # Decodifica a mensagem e separa o conteúdo da mensagem
            received_data = data.decode("utf-8").split(MESSAGE_DIVISOR)

            # extrai o relógio lógico do cliente, sempre é enviado no final do conteúdo
            client_lamport_clock = int(received_data[-1].strip())

            # extrai a operação
            operation = int(received_data[0].strip())
            if is_valid_operation(operation):
                selected_operation = Operations(operation)
                # Caso a operação seja válida extrai o valor da operação e a conta do destinário  em caso de transferência
                value, recipient_account = (
                    int(received_data[1].strip()),
                    received_data[2].strip(),
                )

                bank = Bank()

                message = bank.perform_operation(
                    client_id, selected_operation, value, recipient_account
                )

            # Atualiza o relógio lógico do servidor
            lamport_clock = max(lamport_clock, client_lamport_clock) + 1

            # Adiciona a mensagem à lista com timestamp e relógio lógico de Lamport
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_with_timestamp = f"{message} {MESSAGE_DIVISOR} {timestamp} {MESSAGE_DIVISOR} Lamport Clock: {lamport_clock} {MESSAGE_DIVISOR}  | {received_data[0].strip()}"
            messages.append(message_with_timestamp)
            client_socket.send(message_with_timestamp.encode("utf-8"))
            print(f"Received: {message_with_timestamp} from {client_address}")

        except Exception as e:
            print(e)
            # Handle the exception (e.g., print an error message)
            print("Algum erro aconteceu")


    # Fecha a conexão com o cliente
    client_socket.close()


def start_server():

    # Cria o diretório para armazenar os estados dos relógios lógicos dos clientes
    os.makedirs(CLIENT_STATES_DIR, exist_ok=True)

    # Configurações do servidor
    host = "127.0.0.1"
    port = 12345

    # Cria um socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket ao endereço e à porta
    server_socket.bind((host, port))

    # Habilita o servidor para aceitar conexões de até 5 clientes
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Espera por uma conexão e cria uma nova thread para lidar com o cliente
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Gera um ID único para o cliente com base no endereço e porta
        client_id = f"{addr[1]}"

        # Inicia a thread do cliente
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, addr, client_id)
        )
        client_handler.start()


if __name__ == "__main__":
    start_server()
