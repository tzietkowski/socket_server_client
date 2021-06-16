import json
import os

DATA_FILE_NAME = 'data_user.json'

def load_data(fname = DATA_FILE_NAME) -> list:
    if os.path.isfile(fname):
        with open(fname, 'r') as outfile:
            data = json.load(outfile)
    else:
        with open(fname, 'w') as outfile:
            data = {'data': [{
                'name': 'admin',
                'password': 3815113479867748683,
                'group': 'admin',
                'messages': {'limit': 0, 'char': 256, 'text': ['']}}]}
            json.dump(data, outfile)
    return data.get('data')

def save_data(data:list, database = DATA_FILE_NAME):
    with open(database, 'w') as outfile:
        json.dump({'data': data}, outfile)

def check_name(name:str, data_base:list) -> bool:
    for user in data_base:
        if user.get('name') == name:
            return False
    return True

def add_user(name:str, password = '', group = 'user') -> bool:
    temp_base = load_data()
    if check_name(name,temp_base):
        new_user = {
            'name' : name,   #user name
            'password' : hash(password),  #hash
            'group' : 'admin' if group == 'admin' else 'user',   #user/admin
            'messages': {       #message
                'limit' : 0 if group == 'admin' else 5,    #max message in box
                'char' : 256,   #max character in message
                'text' : ['']   #list of message
            }}
        temp_base.append(new_user)
        save_data(temp_base)
        return True
    #wyslij komunikat ze podana nazwa jest zajeta
    return False

def del_user(name:str) -> bool:
    temp_base = load_data()
    #no user in database
    if check_name(name,temp_base):
        return False
    for index, user in enumerate(temp_base):
        if user.get('name') == name:
            del temp_base[index]
            save_data(temp_base)
        return True



