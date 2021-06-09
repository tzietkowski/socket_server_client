#!/usr/bin/python3
import socket

HOST = '127.0.0.1'
PORT = 65432

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    message = client.recv(64)
    print(message.decode())
    while True:
        answer = input("Command: ")
        client.send(answer.encode())
        if answer == 'stop':
            client.close()
            return
        message = client.recv(2048)
        print(message.decode())

main()
