import socket
import threading

PORT = 8000
PC_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(PC_NAME)
TCP_ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!Q"
HEADER_SIZE_IN_BYTES = 8
ACTIVE = True


def send (sock, message):
    message_encoded = message.encode(FORMAT)
    message_length = len(message_encoded)
    message_send_length = str(message_length).encode(FORMAT)
    padding_needed = HEADER_SIZE_IN_BYTES - len(message_send_length)
    padding = b' ' * padding_needed
    padded_message_send_length = message_send_length + padding
    sock.send(padded_message_send_length)
    sock.send(message_encoded)
    
def receive(sock):
    with threading.Lock():
        global ACTIVE
        is_active = ACTIVE
    while is_active:
        try:
            sock.settimeout(0.1)
            message_length_encoded = sock.recv(HEADER_SIZE_IN_BYTES)
            message_length_string = message_length_encoded.decode(FORMAT)
            if message_length_string:
                message_length_int = int(message_length_string)
                message_encoded = sock.recv(message_length_int)
                message = message_encoded.decode(FORMAT)
                print(message)
        except socket.timeout:
                pass  
        with threading.Lock():
            is_active = ACTIVE

    
if __name__ == "__main__":
    print ("Enter Username: ")
    username = input()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(TCP_ADDR)
    send(client, username)
    receive_thread = threading.Thread(target=receive, args=(client,))
    receive_thread.start()
    try:
        message = input(f"enter message, or enter '{DISCONNECT_MESSAGE}' to disconnect: \n")
   
        while message != DISCONNECT_MESSAGE:
            send (client, message)
            message = input()
        
    except KeyboardInterrupt:
        pass
    with threading.Lock():
        ACTIVE = False
    receive_thread.join()
    send (client, DISCONNECT_MESSAGE)
    client.close()
    