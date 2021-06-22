#!/usr/bin/python3
import socket
import json

class Client:

    def __init__(self, host ='127.0.0.1', port = 65432) -> None:
        self.login = False
        self.connected_with_serwer = False
        self.connect(host, port)
        self.command()

    def connect(self, host:str, port:int)-> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host,port))
        self.connected_with_serwer = True
        print('Connected to the server')

    def command(self)-> None:
        while self.connected_with_serwer:
            print('Please log in')
            self.login_user()
            while self.login:
                self.send_command(input('command: '))
                self.recv_command()

    def login_user(self)->bool:
        while True:
            self.send_command(json.dumps({'user' : input('Login: '), 'password': input('Password: ')}))
            #self.client.send(json.dumps({'user' : input('Login: '), 'password': input('Password: ')}).encode())
            if json.loads(self.client.recv(2048))['answer'] == 'ok':
                self.login = True
                print('Logged in')
                return True
            print('Wrong login or password')

    def send_command(self, command:str):
        print('komenda wyslana: ' + command)
        self.client.send(command.encode())
        
    def recv_command(self):
        print('komenda odebrana')
        print(self.client.recv(2048).decode())

bobek = Client()
