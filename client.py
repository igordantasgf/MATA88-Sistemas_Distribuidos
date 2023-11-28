import socket
import time
import os

# Diretórios para armazenar o estado do relógio lógico do cliente e transferencias
CLIENT_STATES_DIR = "client_states"
TRANFERS_DIR = "transfers"

# Relógio lógico do cliente
lamport_clock = 0
client_id = 0

def save_clock_state():
    print(f"Armazenando time={lamport_clock} no client {client_id}")

    # Salva o estado do relógio lógico do cliente em um arquivo
    state_file_path = os.path.join(CLIENT_STATES_DIR, f"client_{client_id}_state.txt")
    with open(state_file_path, "w") as file:
        file.write(str(lamport_clock))

def load_clock_state():

    # Initialization:   When the client starts, it initializes its logical clock. 
    #                   This initialization involve setting the logical clock to a value  
    #                   greater than the maximum logical time it had before it was closed,
    #                   loading the previous 

    state_file_path = os.path.join(CLIENT_STATES_DIR, f"client_{client_id}_state.txt")
    try:
        # Tenta carregar o estado do relógio lógico do cliente a partir do arquivo
        with open(state_file_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        # Se o arquivo não existir, retorna 0
        print(f"Arquivo do client {client_id} com time-stamp não encontrado")
        return 0

def load_server_id(client_socket):
    # Recebe os dados do cliente
    global client_id
    client_id = client_socket.recv(1024).decode('utf-8')
    if not client_id:
        print("Erro ao receber 'server_id'")
    else:
        print(f"server_id --> {client_id}")


def start_client():
    global lamport_clock

    # Cria o diretório para armazenar o estado do relógio lógico do cliente
    os.makedirs(CLIENT_STATES_DIR, exist_ok=True)

    # Configurações do cliente
    host = '127.0.0.1'
    port = 12345

    # Cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    load_server_id(client_socket)

    # Carrega o estado anterior do relógio lógico do cliente
    lamport_clock = load_clock_state()

    while True:
        # Incrementa o relógio lógico do cliente
        lamport_clock += 1

        # Obtém a string do usuário
        message = input("Enter a string to send to the server (or 'exit' to quit): ")

        if message.lower() == 'exit':
            break

        # Envia a string com o relógio lógico para o servidor
        message_with_clock = f"{message} | {lamport_clock}"
        client_socket.send(message_with_clock.encode('utf-8'))

        # Aguarda um curto período para simular o atraso na rede
        time.sleep(0.1)

    # Salva o estado do relógio lógico do cliente antes de fechar a conexão
    save_clock_state()

    # Fecha a conexão com o servidor
    client_socket.close()

if __name__ == "__main__":
    start_client()
