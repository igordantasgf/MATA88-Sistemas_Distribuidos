import os
import socket
import time

from common import MESSAGE_DIVISOR, RG_PATTERN, NAME_PATTERN
from operations import Operations, operation_message

# Diretórios para armazenar o estado do relógio lógico do cliente e transferencias
CLIENT_STATES_DIR = "client_states"
TRANFERS_DIR = "transfers"


# Relógio lógico do cliente
lamport_clock = 0
client_id = 0


def load_clock_state(client_socket):
    while 1:
        server_clock = client_socket.recv(1024).decode("utf-8")
        if not server_clock:  # <--- criar excessão para falha do recebimento do clock
            print("Erro ao receber clock do servidor")
            return 0
        else:
            print(f"server clock --> {server_clock}")
            return int(server_clock)


def load_server_id(client_socket):
    # Recebe os dados do cliente
    global client_id
    client_id = client_socket.recv(1024).decode("utf-8")
    if not client_id:
        print("Erro ao receber 'server_id'")
    else:
        print(f"server_id --> {client_id}")


def start_client():
    global lamport_clock

    # Cria o diretório para armazenar o estado do relógio lógico do cliente
    os.makedirs(CLIENT_STATES_DIR, exist_ok=True)

    # Configurações do cliente
    host = "127.0.0.1"
    port = 12345

    # Cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    # 1. Obtém id do cliente para armazenar dados
    load_server_id(client_socket)

    # 2. Carrega o estado anterior do relógio lógico do cliente
    lamport_clock = load_clock_state(client_socket)

    rg = input("Digite seu rg:\n")

    rg_message = f"{RG_PATTERN}{rg} {MESSAGE_DIVISOR} {lamport_clock}"
    client_socket.send(rg_message.encode("utf-8"))

    # Recebe os dados do servirdor
    data = client_socket.recv(1024)
    # Decodifica a mensagem e separa o conteúdo da mensagem
    received_data = data.decode("utf-8").split(MESSAGE_DIVISOR)

    # exibe o que foi enviado do servidor
    print(received_data[0].strip())

    if received_data[0].strip() != "Bem vindo!":
        name = input("Por favor digite seu nome:\n")

        name_message = f"{NAME_PATTERN}{name} {MESSAGE_DIVISOR} {lamport_clock}"
        client_socket.send(name_message.encode("utf-8"))

    while True:
        # Incrementa o relógio lógico do cliente
        lamport_clock += 1

        # Obtém a string do usuário
        message = input(
            "Qual operação você deseja realizar? Digite 1 para depositar, 2 para sacar, 3 para transferir, 4 para checar o seu saldo ou 'sair' para sair: \n"
        )

        if message.lower() == "sair":
            break

        try:
            # Obtém a operação selecionada pelo usuário
            operation = int(message)
            selected_operation = Operations(operation)
            recipient_account = None

            # Obtém a mensagem da operação selecionada pelo usuário
            if selected_operation == Operations.CHECK_BALANCE:
                value = 0
            else:
                operation_message_input = operation_message(selected_operation)
                value = input(operation_message_input)

                # Valida o valor digitado pelo usuário, ele deve ser um número e maior do que zero
                while not value.isdigit() or int(value) <= 0:
                    value = input("Digite um valor válido: ")

            if selected_operation is Operations.TRANSFER:
                recipient_account = input("Digite a conta do destinatário: ")

        except Exception:
            print("Operação inválida, tente novamente.\n")
            continue

        # Envia a string com o relógio lógico para o servidor
        message_with_clock = f"{operation} {MESSAGE_DIVISOR} {value} {MESSAGE_DIVISOR} {recipient_account} {MESSAGE_DIVISOR} {lamport_clock} "
        client_socket.send(message_with_clock.encode("utf-8"))

        # Recebe os dados do servirdor
        data = client_socket.recv(1024)
        # Decodifica a mensagem e separa o conteúdo da mensagem
        received_data = data.decode("utf-8").split(MESSAGE_DIVISOR)

        # exibe o que foi enviado do servidor
        print(received_data[0].strip())

        # mostra clock atual do cliente
        print(f"Clock atual: {lamport_clock}")

        # Aguarda um curto período para simular o atraso na rede
        time.sleep(0.1)

    # Fecha a conexão com o servidor
    client_socket.close()


if __name__ == "__main__":
    start_client()
