"""users"""
import json
import os
from re import S


class DataBase():
    """Class DataBase"""


    users = dict()

    def __init__(self, file = 'data.json') -> None:
        self.database_file = file
        self.load_data()

    def load_data(self) -> None:
        """Function load data from json file"""

        if os.path.isfile(self.database_file):
            with open(self.database_file, 'r') as outfile:
                data = json.load(outfile)
                self.users = {db.get('name') : \
                        User(db.get('name'), \
                            db.get('password'), \
                            db.get('messages'), \
                            db.get('group')) \
                    for db in data}

        else:
            with open(self.database_file, 'w+') as outfile:
                self.add_user('admin','','admin')

    def save_data(self) -> None:
        """Function save data"""

        with open(self.database_file, 'w') as outfile:
            json.dump([value.save() for value in self.users.values()], outfile)

    def add_user(self, name:str, password:str, group = 'user') -> None:
        """Function add new user"""

        self.users[name] = User(name, password, [], group)
        self.save_data()

    def del_user(self, name):
        """Function delete user"""

        del self.users[name]
        self.save_data()


class User:
    """Clas User"""

    def __init__(self, name:str, password:str, message:list, group = 'user') -> None:
        self.name = name
        self.__password = password
        self.__group = group
        self.__message = message
        self.__max_message = 5 if group == 'user' else 0
        self.__count_message = len(message)
        self.__max_char = 255

    def max_char(self) -> int:
        """Function return max characters"""

        return self.__max_char

    def save(self)-> dict:
        """Function save user"""

        return {\
            'name': self.name,\
            'password': self.__password, \
            'group': self.__group, \
            "messages": self.__message}

    def check_password(self,input_password:str) -> bool:
        """Function check password"""

        return self.__password == input_password

    def add_message(self,from_user:str, new_message:str)->bool:
        """Function add new message"""

        if (self.__group == 'user' and \
             len(self.__message) == self.__max_message) or \
             (len(new_message) > self.__max_char):
            return False
        self.__count_message += 1
        self.__message.append((from_user, new_message))
        return True

    def del_message(self, number_message)-> bool:
        """Function delete message"""
        if (0 < number_message < self.__count_message + 1) and self.__count_message != 0:
            try:
                del self.__message[number_message]
                self.__count_message -= 1
                return True
            except IndexError:
                return False
        return False

    def list_message(self)->list:
        """Function list message"""

        return self.__message

    def change_password(self,new_passsword:str) -> None:
        """Function change password"""

        self.__password = new_passsword

    def check_admin(self):
        """Function checking admin users"""

        return self.__group == 'admin'

    def count_message(self)-> bool:
        """Function count message"""

        return self.__count_message < self.__max_message or self.__group == 'admin'

