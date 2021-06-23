"""users"""
import json
import os


class DataBase():
    """Clas DataBase"""

    database_file = 'data.json'
    users = dict()

    def __init__(self) -> None:
        self.load_data()

    def load_data(self):
        """Function load data from json file"""

        if os.path.isfile(DataBase.database_file):
            with open(DataBase.database_file, 'r') as outfile:
                data = json.load(outfile)
                self.users = {db.get('name') : \
                        User(db.get('name'), \
                            db.get('password'), \
                            db.get('messages'), \
                            db.get('group')) \
                    for db in data}

        else:
            with open(DataBase.database_file, 'w+') as outfile:
                self.add_user('admin','','admin')

    def save_data(self):
        """Function save data"""

        with open(DataBase.database_file, 'w') as outfile:
            json.dump([value.save() for value in self.users.values()], outfile)

    def add_user(self, name:str, password:str, group = 'user'):
        """Function add new user"""

        if name not in self.users.keys():
            self.users[name] = User(name, password, [], group)
            self.save_data()

    def del_user(self, name):
        """Function delete user"""

        if name in self.users.keys():
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

    def __str__(self) -> str:
        """Function return name user"""

        return self.name

    def save(self)->dict:
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

        if 0 < number_message < self.__count_message + 1:
            self.__count_message -= 1
            del self.__message[number_message - 1]
            return True
        return False

    def list_message(self)->list:
        """Function list message"""

        return [{index: value} for index, value in enumerate(self.__message, 1)]

    def change_password(self,new_passsword:str):
        """Function change password"""

        self.__password = new_passsword
