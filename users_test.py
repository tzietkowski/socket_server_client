import py
from users import User
import pytest

user_data = [pytest.param(User('admin','admin1',[],'admin')),
             pytest.param(User('user','user1',[],'user'))]

@pytest.fixture()
def user_admin():
    user = User('admin','admin1',[],'admin')
    return user

@pytest.fixture()
def user_normal():
    user = User('user','user1',[])
    return user

class TestUser():
    
    @pytest.mark.parametrize('user', user_data)
    def test_max_char(self, user):
        assert user.max_char() == 255

    @pytest.mark.parametrize('user', user_data)
    def test_save(self, user):
        answer_admin = {\
            'name': 'admin',\
            'password': 'admin1', \
            'group': 'admin', \
            "messages": []}
        
        answer_normal = {\
            'name': 'user',\
            'password': 'user1', \
            'group': 'user', \
            "messages": []}
        if user.check_admin():
            assert user.save() == answer_admin
        else:
            assert user.save() == answer_normal

    @pytest.mark.parametrize('user', user_data)
    def test_check_password(self, user):
        if user.check_admin():
            assert user.check_password('admin1') == True
            assert user.check_password('admin') == False
            assert user.check_password('user1') == False
            assert user.check_password('user') == False
        else:
            assert user.check_password('admin1') == False
            assert user.check_password('admin') == False
            assert user.check_password('user1') == True
            assert user.check_password('user') == False

    @pytest.mark.parametrize('user', user_data)
    def test_add_message(self, user):
        assert user.add_message('test','mesage1')

    @pytest.mark.parametrize("count_char, permission" , [(255, True), (256, True), (257, False)])
    def test_add_message_max_char(self, count_char, permission):
        user = User('user','user1',[],'user')
        message = ''.join(['a' for _ in range(count_char - 1 )])
        assert user.add_message('test', message) == permission
    
    @pytest.mark.parametrize("count_message, permission" , [(4, True), (5, True), (6, False)])
    def test_add_message_max5_message_normal_user(self, count_message, permission):
        user = User('user','user1',[],'user')
        answer = all([user.add_message('test','message') for _ in range(count_message)])
        assert answer == permission

    @pytest.mark.parametrize("count_message, permission" , [(4, True), (5, True), (10, True)])
    def test_add_message_max5_message_admin_user(self, count_message, permission):
        user = User('user','user1',[],'admin')
        answer = all([user.add_message('test','message') for _ in range(count_message)])
        assert answer == permission


    @pytest.mark.parametrize('user', user_data)
    def test_del_message_empty(self, user):
        assert user.del_message(0) == False
        assert user.del_message(1) == False
        assert user.del_message(100) == False

    @pytest.mark.parametrize('user', user_data)
    def test_del_message(self, user):
        user.add_message('test','message')
        assert user.del_message(1) == True

    
    def test_list_message(self):
        user = User('user1','user1',[["admin", "asfsafsaf"]],'user')
        assert user.list_message() == [["admin", "asfsafsaf"]]
    
    def test_list_message_empty(self):
        user = User('user1','user1',[],'user')
        assert user.list_message() == []
    
    @pytest.mark.parametrize("old_password, new_password, good" , [('pass1', 'pass1', True), ('pass2', 'pass2', True), ('pass1', 'pass2', False)])
    def test_change_password(self, old_password, new_password, good):
        user = User('user1',old_password,[],'user')
        user.change_password(new_password)
        answer = user.check_password(old_password)
        assert answer == good

    @pytest.mark.parametrize("group_user, good" , [('admin', True), ('user', False)])
    def test_check_admin(self, group_user, good):
        user = User('user1','user1',[],group_user)
        assert user.check_admin() == good

class TestDataBase():
    pass