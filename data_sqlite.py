import os
import json
import sqlite3

class Sql():
    """Class of communication with the database"""

    def __init__(self) -> None:
        self.connection = sqlite3.connect('data_base.db')
        self.cursor = self.connection.cursor()
    
    def __del__(self) -> None:
        self.connection.close()

    def setup(self) -> None:
        """Function create tables"""

        command = '''CREATE TABLE IF NOT EXISTS users(
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            pass TEXT NOT NULL,
            admin INTEGER DEFALUT '0' NOT NULL)'''
        self.cursor.execute(command)
        self.connection.commit()
        command = '''CREATE TABLE IF NOT EXISTS messages(
            id_mess INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            user_from INTEGER NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE  )'''
        self.cursor.execute(command)
        self.connection.commit()
        self.add_user('admin', 'admin', 1)


    def check_user_exists(self , name_user:str) -> bool:
        """Function that checks if the user is in the bottom database"""

        command = """
            SELECT
                1 
            WHERE EXISTS (
                SELECT 
                    name 
                FROM 
                    users 
                WHERE 
                    name='%s');
        """ %(name_user)
        self.cursor.execute(command)
        self.connection.commit()
        return bool(self.cursor.fetchone())
    
    def add_user(self, name:str, password:str, group = 0) -> bool:
        """Function add new user"""

        if not self.check_user_exists(name):
            command = """
                INSERT INTO 
                    users (name, pass, admin) 
                VALUES 
                    ('%s','%s', %s);
            """ %(name, password, group)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False

    def del_user(self, name) -> None:
        """Function delete user"""

        if self.check_user_exists(name):
            command = """
                DELETE FROM 
                    users 
                WHERE
                    name='%s';
            """ %(name)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False

    def check_user_password(self,name:str, input_password:str) -> bool:
        """Function check password"""

        command = """
            SELECT
                pass
            FROM
                users
            WHERE
                name='%s';
        """ %(name)
        self.cursor.execute(command)
        self.connection.commit()
        password = self.cursor.fetchone()
        return password[0] == input_password
        
    def check_name(self, id:int) -> str:
        """Function name user"""

        command = """
                SELECT
                    name
                FROM
                    users
                WHERE
                    id_user='%i';
            """ %(id)
        self.cursor.execute(command)
        self.connection.commit()
        name = self.cursor.fetchone()
        if name != None:
            return name[0]
        return 'User not exists'


     
    def check_id(self, name:str) -> int:
        """Function check id user"""
         
        command = """
            SELECT
                id_user
            FROM
                users
            WHERE
                name='%s';
        """ %(name)
        self.cursor.execute(command)
        self.connection.commit()
        id = self.cursor.fetchone()
        return id[0]
        

    def add_message(self,name:str, to_user:str, message:str)-> bool:
        """Function send message"""

        if self.check_user_exists(to_user) and \
            (self.count_message(name) < 5 or self.check_admin(name)):
            command = """
                INSERT INTO
                    messages(id_user, user_from, message) 
                VALUES
                    (%i,%i,'%s'); 
            """ %(self.check_id(to_user), self.check_id(name), message[0:255])
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False

    def del_message(self, number_message:int)-> bool:
        """Function delete message"""

        
        command = """
            DELETE FROM
                messages 
            WHERE
                id_mess=%i;
        """ %(number_message)
        self.cursor.execute(command)
        self.connection.commit()
        return True


    def list_message(self, name)-> list:
        """Function list message"""

        command = """
            SELECT
                users.id_user, user_from, message, id_mess
            FROM
                users
            JOIN
                messages
            ON
                users.id_user = messages.id_user
            WHERE
                users.id_user=%i;
        """ %(self.check_id(name))
        self.cursor.execute(command)
        self.connection.commit()
        answer = self.cursor.fetchall()
        return [(self.check_name(message[0]), self.check_name(message[1]), message[2], message[3]) for message in answer]

    def change_user_password(self,name:str, old_password:str, new_passsword:str) -> bool:
        """Function change password"""

        if self.check_user_password(name, old_password):
            command = """
                UPDATE
                    users
                SET
                    pass='%s'
                WHERE
                    name='%s';
            """ %(new_passsword, name)
            self.cursor.execute(command)
            self.connection.commit()
            return self.check_user_password(name, new_passsword)
        return False


    def check_admin(self, name:str) -> bool:
        """Function checking admin users"""

        command = """
            SELECT
                admin
            FROM
                users
            WHERE
                name='%s';
        """ %(name)
        self.cursor.execute(command)
        self.connection.commit()
        admin = self.cursor.fetchone()
        return True if admin[0] == 1 else False


    def count_message(self, name:str)-> int:
        """Function count message"""
        
        command = """
            SELECT
                count(message)
            FROM
                messages
            WHERE
                id_user=%i;
        """ %(self.check_id(name))
        self.cursor.execute(command)
        self.connection.commit()
        admin = self.cursor.fetchone()
        return admin[0]

