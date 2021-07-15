"""Client"""
#!/usr/bin/python3
import socket
import json

class Client:
    """Class client"""

    def __init__(self, host ='127.0.0.1', port = 65432):
        self.user_name = ''
        self.connected_with_serwer = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect(host, port)
            self.command()
        except socket.error:
            print('Server error')
        finally:
            self.disconnect()


    def connect(self, host:str, port:int)-> None:
        """Function connect to serwer"""

        self.client.connect((host,port))
        self.connected_with_serwer = True
        print('Connected to the server')


    def disconnect(self)->None:
        """Function disconnect to the serwer"""

        print('Closing connection to the server')
        self.client.close()


    def command(self)-> None:
        """Function of sending and receiving commands"""

        while self.connected_with_serwer:
            self.login_user()
            while not self.user_name == '':
                command_to_send = input('command: ')
                self.send_command(command_to_send)
                if command_to_send == 'stop':
                    return
                else:
                    self.recv_command()
                    if command_to_send == 'logout':
                        self.user_name = ''



    def login_user(self)->bool:
        """Function login user in server"""

        while True:
            print('Please log in')
            self.send_command({\
                    'user' : input('Login: '), \
                    'password': input('Password: ')})
            answer_from_server = json.loads(self.client.recv(2048).decode())
            if answer_from_server['answer'] == 'ok':
                self.user_name = answer_from_server['user']
                print('Logged in')
                return True
            print('Wrong login or password')


    def send_command(self, command:str):
        """Function send command to server"""

        self.client.send(json.dumps({'user': self.user_name, 'command': command}).encode())


    def recv_command(self):
        """Function receiving from server"""

        print('Server: ' + json.loads(self.client.recv(2048).decode())['command'])


client1 = Client()
