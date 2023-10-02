import socket
import threading

PORT = 8000
PC_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(PC_NAME)
TCP_ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!Q"
HEADER_SIZE_IN_BYTES = 8

def send (sock, message):
    message_encoded = message.encode(FORMAT)
    message_length = len(message_encoded)
    message_send_length = str(message_length).encode(FORMAT)
    padding_needed = HEADER_SIZE_IN_BYTES - len(message_send_length)
    # this repeats the space byte by padding needed times
    padding = b' ' * padding_needed
    padded_message_send_length = message_send_length + padding
    sock.send(padded_message_send_length)
    sock.send(message_encoded)
    
def receive(sock):
    while True:
        try:
            message_length_encoded = sock.recv(HEADER_SIZE_IN_BYTES)
            message_length_string = message_length_encoded.decode(FORMAT)
            if message_length_string:
                message_length_int = int(message_length_string)
                message_encoded = sock.recv(message_length_int)
                message = message_encoded.decode(FORMAT)
                print(f"\n{message}")
        except ConnectionResetError:
            print("Server connection was closed.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(TCP_ADDR)

    receive_thread = threading.Thread(target=receive, args=(client,))
    receive_thread.start()
    
    try:
        message = input(f"Enter message, or enter '{DISCONNECT_MESSAGE}' to disconnect: ")
        while message != DISCONNECT_MESSAGE:
            send(client, message)
            message = input("Enter message: ")
    except KeyboardInterrupt:
        pass
    finally:
        send(client, DISCONNECT_MESSAGE)
        receive_thread.join()
        client.close()
