import socket
import message as ms
from message import Message
import pickle

HOST = "localhost"
PORT = 9899

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect_ex((HOST, PORT))


while True:
    raw_msg = input("<Message>: \n")
    message_object = Message(message=raw_msg, ip=HOST)
    pickle_message = pickle.dumps(message_object)
    client_socket.send(pickle_message).encode("utf-8")



    print("Waiting for response...")
    try:
        response = client_socket.recv(4096)
        unpickled_response = pickle.load(response)

        print(unpickled_response.message)

    except Exception as e:
        print(f"Error: {e}")