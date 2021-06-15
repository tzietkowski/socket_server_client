import json
import os

DATA_FILE_NAME = 'new1.json'

def load_data(fname:str) -> dict:
    if os.path.isfile(fname):
        # File exists
        with open(fname, 'r') as outfile:
            data = json.load(outfile)
    else: 
        # Create file with admin user
        with open(fname, 'w') as outfile:
            data = add_user('admin', hash('admin'), 1)
            json.dump(data, outfile)
    return data

def add_user(name:str, password:str, group:str) -> dict:
    if os.path.isfile(DATA_FILE_NAME):
        tmp = load_data(DATA_FILE_NAME)
    empty_user = {
    'user_' + name :{
        'name' : name,   #user name
        'password' : password,  #hash
        'group' : group,   #user/admin
        'messages': {       #message
            'limit' : 5,    #max message in box
            'char' : 256,   #max character in message
            'text' : ['']   #list of message
        }
    }
    
}
    return empty_user

add_user('tom', 'dupa', 1)