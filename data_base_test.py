from abc import abstractclassmethod
import json
import os
import pytest
from users import DataBase


@pytest.fixture()
def data_base_for_testing():
    return DataBase('new_file.json')

class TestDataBase():

    def teardown_method(self):
        print('\n===Teardown Method===')

    def test_load_data_create_file(self):
        DataBase('new_file.json')
        with open('new_file.json', 'r') as outfile:
            data = json.load(outfile)
        assert data == [{"name": "admin", "password": "", "group": "admin", "messages": []}]

    def teardown_method(self):
        os.remove('new_file.json')

    def test_load_data(self, data_base_for_testing):
        data_base_for_testing.load_data()
        user_to_check = 'admin'
        answer = user_to_check in data_base_for_testing.users
        assert answer == True
    
    def teardown_method(self):
        os.remove('new_file.json')

    def test_save_data(self, data_base_for_testing):
        data_base_for_testing.add_user('test', 'test1', 'admin')
        with open('new_file.json', 'r') as outfile:
                data_after = json.load(outfile)
        answer =  {'group': 'admin', 'messages': [], 'name': 'test', 'password': 'test1'} in data_after
        assert answer == True

    def teardown_method(self):
        os.remove('new_file.json')

    def test_add_user(self, data_base_for_testing):
        data_base_for_testing.add_user('test1', 'test1', 'admin')
        with open('new_file.json', 'r') as outfile:
                data_after = json.load(outfile)
        answer = {"name": "test1", "password": "test1", "group": "admin", "messages": []} in data_after
    
        assert answer == True

    def teardown_method(self):
        os.remove('new_file.json')

    def test_del_user_exist(self, data_base_for_testing):
        data_base_for_testing
     
    def teardown_method(self):
        os.remove('new_file.json')