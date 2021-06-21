import json
import os

class Data_base():
    
    database_file = 'data_user_class.json'

    def __init__(self) -> None:
        self.load_users()
 
    def load_users(self):
        self.users = [User(db.get('name'), db.get('password'), db.get('messages'), db.get('group')) for db in self.load_data_from_json()]
        print(*self.users)

    def load_data_from_json(self) -> list:
        if os.path.isfile(Data_base.database_file):
            with open(Data_base.database_file, 'r') as outfile:
                data = json.load(outfile)
        else:
            with open(Data_base.database_file, 'w+') as outfile:
                self.save_data_from_json(
                    [{
                    'name': 'admin',
                    'password': 3815113479867748683,
                    'group': 'admin',
                    'messages': {'id': 0, 'from': '', 'text': ''}}])
                data = json.load(outfile)
        return data.get('data')
     
    def save_data_to_json(self,data):
        with open(Data_base.database_file, 'w') as outfile:
            json.dump({'data': data}, outfile)
        
    def add_user(self):
        pass

    def del_user(self):
        pass


class User:
    
    def __init__(self, name:str, password:str, message:list, group = 'user') -> None:
        self.name = name
        self.__password = password
        self.__group = group
        self.__message = message
        self.__max_message = 5 if group == 'user' else 0
        self.__count_message = len(message)
        self.__max_char = 255

    def check_password(self,input_password:str) -> bool:
        return self.__password == input_password

    def add_message(self,from_user:str, new_message:str)->bool:
        if (self.__group == 'user' and len(self.__message) == self.__max_message) or (len(new_message) > self.__max_char):
            return False
        self.__count_message += 1
        self.__message.append((self.__count_message, from_user, new_message))
        return True

    def del_message(self, id)-> bool:
        if 0 < id < self.__count_message + 1:
            del self.__message[id - 1]
            return True
        return False

    def list_message(self)->list:
        return self.__message

    def change_password(self,new_passsword:str):
        self.__password = new_passsword

DB = Data_base()

#print(DB.users[0].name)
