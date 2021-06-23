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
        self.commands = {'info': {'func': 'self.info()','help': 'taka a sraka komenda'},\
                        'stop': {'func': 'self.stop_server()','help':'Server stop'}}
        
        try:
            self.server = self.start_server(host, port)
            self.login = self.login_user()
            self.command()
        except:
            print('cos nie tak z serwerem')
        finally:
            print('koniec')
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
                self.send(message['user'], self.commands[message['command']]['func'])
            else:
                self.send(message['user'], 'Wrong command')
                

    def send(self, user:str, message:str)-> None:
        """Function send message to client"""

        self.server.send(json.dumps({'user': user, 'command': message}).encode())



    def info(self)-> str:

        return ('Ver 1.0, Server start: ' + time.ctime(self.time_start))

    def help(self)-> str:
        pass


bobek = Server()








# def uptime_command() -> str: 
#     return json.dumps(time.strftime("%H:%M:%S", time.gmtime(time.time() - TIME_START_SERVER)))

# def info_command()-> str: 
#     return json.dumps('Ver 1.0, Server start: ' + time.ctime(TIME_START_SERVER))

# def help_command()-> str: 
#     return json.dumps({
#             'uptime' : 'czas zycia serwera',
#             'info' : 'numer wersji serwera, data utworzenia',
#             'help' : 'pomoc',
#             'stop' : 'zamyka serwer i klienta'
#     })



# def wrong_command()-> str: 
#     return json.dumps('Invalid command')

# def main() -> None:
#     db = DataBase()
#     db.add_user('tom','1','user')
#     serwer = start_server()
#     while login_user(serwer, db):
#         while True:
#             message = (serwer.recv(64)).decode()
#             serwer.send(message.encode())
#     stop_server()

#     #comands
#     # commands = {
#     #         'uptime': uptime_command,
#     #         'info': info_command,
#     #         'help': help_command,
#     #         'stop': server.close
#     #     }
#     # try:
#     #     while True:

#     #         message = (conn.recv(64)).decode()
#     #         if message in commands:
#     #             re_message = commands[message]()
#     #         else:
#     #             re_message = wrong_command()
#     #         conn.send(re_message.encode())

