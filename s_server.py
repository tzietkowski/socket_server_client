"""Server"""
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
        self.db.add_user('tom','1','admin')
        self.server_run = False
        self.login = False
        self.user_admin = False
        self.server_scoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = {'info': {'func': self.info ,'help': 'Info about the server version'},\
                        'stop': {'func': self.stop_server ,'help':'Server stop'},\
                        'help': {'func': self.help ,'help':'Server stop'},\
                        'new_user': {'func': self.new_user ,'help':'Add new user: \
                            name_user:password'},\
                        'del_user': {'func': self.del_user ,'help':'Remove user'},\
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


    def login_user(self)-> bool:
        """Function login user"""

        while not self.login:
            message = self.recv()
            self.name_user = message['command']['user']
            if self.name_user in self.db.users.keys() and self.db.users[\
                self.name_user].check_password(message['command']['password']):
                self.server.send(json.dumps(\
                    {'user': self.name_user, 'answer': 'ok'}).encode())
                print('login user: ' + self.name_user)
                self.user_admin = self.db.users[self.name_user].check_admin()
                return True
            else:
                self.server.send(json.dumps({\
                    'user': self.name_user, 'answer': 'wrong login or password'}).encode())
        return False

    def command(self)-> None:
        """Function run command"""

        while True:
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

        return json.loads(self.server.recv(64).decode())

    def info(self)-> str:
        """Function info about the server version"""

        return 'Ver 2.0, Server start: ' + time.ctime(self.time_start)


    def help(self)-> str:
        """Function help - list of commands"""

        lista = 'Tu bedzie lista '
        return lista


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
    

bobek = Server()
