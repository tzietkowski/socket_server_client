"""Server"""
#!/usr/bin/python3
import socket
import time
import json
import re
from users import DataBase


class Server:
    """Class server"""

    def __init__(self, host = '127.0.0.1', port = 65432) -> None:
        self.time_start = time.time()
        self.db = DataBase()
        self.name_user = ''
        self.user_admin = False
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
            self.server = self.start_server(host, port)
            self.command()
        except socket.error:
            print('Error server')
        finally:
            print('The end')
            self.stop_server()

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
            if message['command']['user'] in self.db.users.keys() and self.db.users[\
                message['command']['user']].check_password(message['command']['password']):
                print('wysylam')
                self.server.send(json.dumps(\
                    {'user': message['command']['user'], 'answer': 'ok'}).encode())
                print('login user: ' + message['command']['user'])

                self.name_user = message['command']['user']
                self.user_admin = self.db.users[self.name_user].check_admin()
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
            if new_login not in self.db.users.keys():
                self.send('New user password:')
                new_pass = self.recv()['command']
                self.send('New user premissons[admin/user]:')
                new_premis = self.recv()['command']
                while not (new_premis == 'admin' or new_premis == 'user'):
                    self.send('New user premissons[admin/user]:')
                    new_premis = self.recv()['command']
                self.db.add_user(new_login, new_pass, new_premis)
                return 'added user '

    @admin_req
    def del_user(self) -> str:
        """Function remove user"""

        self.send('Username to remove:')
        del_name = self.recv()['command']
        if del_name not in self.db.users.keys():
            return 'No such user'
        else:
            self.db.del_user(del_name)
            return 'User removed'

    def send_message(self) -> str:
        """Function sending message"""

        self.send('Message to user:')
        login_to_send = self.recv()['command']
        if login_to_send not in self.db.users.keys():
            return 'No such user'
        else:
            if not self.db.users[login_to_send].count_message():
                return 'The user has a full mailbox'
            self.send('Message(max 255 charakters):')
            message = self.recv()['command']
            if len(message) > self.db.users[self.name_user].max_char():
                return 'Message too long'
            self.db.users[login_to_send].add_message(self.name_user, message)
            self.db.save_data()
            return 'Message sent'

    def list_message(self) -> str:
        """Function list message"""

        text_list = '\nNr. From  - Text \n'
        for index, value in enumerate(self.db.users[self.name_user].list_message(), 1):
            text_list += str(index) + '. ' + str(value[0]) + ' - ' + str(value[1] + '\n')
        return text_list

    def del_message(self) -> str:
        """Function remove message"""

        self.send('Numer message to remove:')
        message = self.recv()['command']
        if re.search(r'\d', message):
            self.db.users[self.name_user].del_message(int(message))
            self.db.save_data()
            return 'Message removed'
        else:
            return 'Wrong number'

    def change_password(self) -> str:
        """Function change password"""

        self.send('old password:')
        if self.db.users[self.name_user].check_password(self.recv()['command']):
            self.send('New password:')
            pass1 = self.recv()['command']
            self.send('Re new password:')
            pass2 = self.recv()['command']
            if pass1 == pass2:
                self.db.users[self.name_user].change_password(pass1)
                self.db.save_data()
                return 'Password changed'
        return 'Password not changed'

serwer1 = Server()
