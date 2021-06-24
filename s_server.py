#!/usr/bin/python3
import socket
import time
import json
from users import DataBase


class Server:
    """Class server"""

    def __init__(self, host = '127.0.0.1', port = 65432) -> None:
        self.time_start = time.time()
        self.db = DataBase()
        # for testing!!!
        self.db.add_user('tom','1','user')
        self.server_run = False
        self.login = False
        self.server_scoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = {'info': {'func': self.info ,'help': 'Info about the server version'},\
                        'stop': {'func': self.stop_server ,'help':'Server stop'},\
                        'help': {'func': self.help ,'help':'Server stop'},\
                        'uptime': {'func': self.uptime ,'help':'Server lifetime'}\
                            }
        
        try:
            self.server = self.start_server(host, port)
            self.login = self.login_user()
            self.command()
        except:
            print('cos nie tak z serwerem')
        finally:
            print('The end')
            self.stop_server()


    def start_server(self, host:str, port:int) -> socket:
        """Function start server"""
        
        self.server_scoket.bind((host, port))
        self.server_scoket.listen()
        print("Wait to connect client")
        conn, addr = self.server_scoket.accept()
        print("Connected by", addr)
        return conn


    def stop_server(self)-> None:
        """Function stop server"""

        print('Closing the server')
        self.server_scoket.close()


    def login_user(self)-> bool:
        """Function login user"""

        while self.login == False:
            message = json.loads(self.server.recv(2024).decode())
            if message['command']['user'] in self.db.users.keys() and self.db.users[message['command']['user']].check_password(message['command']['password']):
                self.server.send(json.dumps({'user': message['command']['user'], 'answer': 'ok'}).encode())
                print('login user: ' + message['command']['user'])
                return True
            else:
                self.server.send(json.dumps({'user': message['user'], 'answer': 'wrong login or password'}).encode())



    def command(self)-> None:
        """Function run command"""

        while True:
            message = json.loads(self.server.recv(64).decode())
            if message['command'] in self.commands.keys():
                if message['command'] == 'stop':
                    return
                self.send(message['user'], self.commands[message['command']]['func']())
            else:
                self.send(message['user'], 'Wrong command')
                

    def send(self, user:str, message:str)-> None:
        """Function send message to client"""

        self.server.send(json.dumps({'user': user, 'command': message}).encode())



    def info(self)-> str:
        """Function info about the server version"""

        return ('Ver 2.0, Server start: ' + time.ctime(self.time_start))

    def help(self)-> str:
        """Function help - list of commands"""

        lista = 'Tu bedzie lista '
        return lista

    def uptime(self) -> None:

        return time.strftime("%H:%M:%S", time.gmtime(time.time() - self.time_start))


bobek = Server()