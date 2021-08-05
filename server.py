"""Server"""
#!/usr/bin/python3
import socket
import time
import json
import re
import os
from data_sqlite import Sql as db


class Server:
    """Class server"""

    def __init__(self) -> None:

        self.time_start = time.time()
        self.name_user = ''
        self.user_admin = False
        self.__host = '127.0.0.1'
        self.__port = 65432
        self.server_scoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = { 'pass': {'func': self.change_password ,\
                        'help':'Change password'},\
                        'del_m': {'func': self.del_message ,'help':'Remove message'},\
                        'del_u': {'func': self.del_user ,'help':'Remove user'},\
                        'help': {'func': self.help ,'help':'List of commands'},\
                        'info': {'func': self.info ,'help': 'Info about the server version'},\
                        'list': {'func': self.list_message ,'help':\
                             'List of all messages'},\
                        'logout': {'func': self.logout ,'help':'User logout'},\
                        'add_user': {'func': self.new_user ,'help':'Add new user'},\
                        'send' : {'func': self.send_message ,'help':\
                            'Sending message to user'},\
                        'stop': {'func': self.stop_server ,'help':'Server stop'},\
                        'uptime': {'func': self.uptime ,'help':'Server lifetime'}\
                            }

        try:
            self.__load_config()
            db().setup()
            self.server = self.start_server(self.__host, self.__port)
            self.command()
        except socket.error:
            print('Error server')
        finally:
            print('The end')
            self.stop_server()

    def __load_config(self) -> None:
        """Load config parameters"""

        if os.path.isfile('config.ini'):
             with open('config.ini', 'r') as outfile:
                data = json.load(outfile)
                self.__host = data['ip_serwer']
                self.__port = data['port']
        else:
            print('Configuration file not found')
            raise NameError('No configuration file')

    def admin_req(func):
        """Decorator check premmison"""

        def wrapper(self, *args, **kwargs):
            """Wraper"""

            if self.user_admin:
                return func(self, *args, **kwargs)
            else:
                return 'No premissed'

        return wrapper


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


    def login_user(self)-> None:
        """Function login user"""

        while self.name_user == '':
            message = self.recv()
            if db().check_user_exists(message['command']['user']) and \
                db().check_user_password(message['command']['user'],message['command']['password']):
                print('wysylam')
                self.server.send(json.dumps(\
                    {'user': message['command']['user'], 'answer': 'ok'}).encode())
                print('login user: ' + message['command']['user'])
                self.name_user = message['command']['user']
                self.user_admin = db().check_admin(self.name_user)
                return
            else:
                self.server.send(json.dumps({\
                    'user': self.name_user, 'answer': 'wrong login or password'}).encode())
        return


    def logout(self) -> str:
        """Function logout user"""

        self.name_user = ''
        self.user_admin = False

        return 'logout'


    def command(self)-> None:
        """Function run command"""

        while True:
            self.login_user()
            message = self.recv()
            if message['command'] in self.commands.keys():
                if message['command'] == 'stop':
                    return
                self.send(self.commands[message['command']]['func']())
            else:
                self.send('Wrong command')


    def send(self, message:str)-> None:
        """Function send message to client"""

        self.server.send(json.dumps({'user': self.name_user, 'command': message}).encode())

    def recv(self)->str:
        """Function recved message form client"""

        return json.loads(self.server.recv(2048).decode())

    def info(self)-> str:
        """Function info about the server version"""

        return 'Ver 2.0, Server start: ' + time.ctime(self.time_start)


    def help(self)-> str:
        """Function help - list of commands"""

        help_message = '\n'
        for key, value in self.commands.items():
            help_message += str(key) + ' - ' + str(value['help']) + '\n'
        return help_message


    def uptime(self) -> None:
        """Function server lifetime"""

        return time.strftime("%H:%M:%S", time.gmtime(time.time() - self.time_start))

    @admin_req
    def new_user(self) -> str:
        """Function add new user"""

        new_login, new_pass, new_premis = '','',''

        while True:
            self.send('New user login:')
            new_login = self.recv()['command']
            if not db().check_user_exists(new_login):
                self.send('New user password:')
                new_pass = self.recv()['command']
                self.send('New user premissons[admin/user]:')
                new_premis = True if self.recv()['command'] == 'admin' else False
                db().add_user(new_login, new_pass, new_premis)
                return 'added user '

    @admin_req
    def del_user(self) -> str:
        """Function remove user"""

        self.send('Username to remove:')
        del_name = self.recv()['command']
        if not db().check_user_exists(del_name):
            return 'No such user'
        else:
            db().del_user(del_name)
            return 'User removed'

    def send_message(self) -> str:
        """Function sending message"""

        self.send('Message to user:')
        login_to_send = self.recv()['command']
        if not db().check_user_exists(login_to_send):
            return 'No such user'
        else:
            if db().count_message(self.name_user) > 5 and self.user_admin:
                return 'The user has a full mailbox'
            self.send('Message(max 255 charakters):')
            message = self.recv()['command']
            db().add_message(self.name_user, login_to_send, message)
            return 'Message sent'

    def list_message(self) -> str:
        """Function list message"""
        text_list = '\nNr. From  - ID - Text \n'
        mess = db().list_message(self.name_user)
        
        for index, value in enumerate(mess, 1):
            text_list += str(index) + '. ' + str(value[1]) + ' - ' + str(value[3]) + ' - ' + str(value[2] + '\n')
        return text_list


    def del_message(self) -> str:
        """Function remove message"""
        
        self.send(self.list_message() + '\n' + 'Id message to remove:')
        message = self.recv()['command']
        if re.search(r'\d', message):
            db().del_message(int(message))
            return 'Message removed'
        else:
            return 'Wrong number'

    def change_password(self) -> str:
        """Function change password"""

        self.send('old password:')
        old = self.recv()['command']
        self.send('New password:')
        new_1 = self.recv()['command']
        self.send('Re new password:')
        new_2 = self.recv()['command']
        if new_1 == new_2:
            if db().change_user_password(self.name_user, old, new_1):
                return 'Password changed'
        return 'Password not changed'

serwer = Server()
