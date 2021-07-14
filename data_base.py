import re
import psycopg2

class Data_base_sql():
    """Class of communication with the database"""

    def __init__(self) -> None:
        self.connection = psycopg2.connect(
                                host="localhost",
                                database="db_user",
                                user="tomek",
                                password="p1")
        self.cursor = self.connection.cursor()
    
    def __del__(self) -> None:
        self.cursor.close()
        self.connection.close()

    def check_table_exist(self, name_table:str) -> None:
        """Function that checks if the table is in the bottom database"""
        
        command = """
            SELECT 1 WHERE EXISTS (SELECT FROM information_schema.tables WHERE table_name = '%s');
        """ %(name_table)
        self.cursor.execute(command)
        self.connection.commit()
        return bool(self.cursor.fetchone())

    def create_tables(self) -> None:
        """Function create tables"""

        commands = (
                    """
                    CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(25) NOT NULL UNIQUE,
                        pass VARCHAR(25) NOT NULL,
                        admin BOOLEAN DEFAULT FALSE
                    );
                    """,
                     """
                    CREATE TABLE IF NOT EXISTS message(
                        id SERIAL,
                        id_user INTEGER NOT NULL,
                        user_from INTEGER NOT NULL,
                        message VARCHAR(255) NOT NULL,
                        PRIMARY KEY (id),
                        FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE   
                    );
                    """
                   )
        for command in commands:
            self.cursor.execute(command)
            self.connection.commit()


    def check_user_exists(self , name_user:str) -> bool:
        """Function that checks if the user is in the bottom database"""

        command = """
            SELECT 1 WHERE EXISTS (SELECT name FROM users WHERE name='%s');
        """ %(name_user)
        self.cursor.execute(command)
        self.connection.commit()
        return bool(self.cursor.fetchone())
    
    def add_user(self, name:str, password:str, group = False) -> bool:
        """Function add new user"""

        if not self.check_user_exists(name):
            command = """
                insert into users (name, pass, admin) values ('%s','%s', %s);
            """ %(name, password, group)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False

    def del_user(self, name) -> None:
        """Function delete user"""

        if self.check_user_exists(name):
            command = """
                delete from users where name='%s';
            """ %(name)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False

    def check_user_password(self,name:str, input_password:str) -> bool:
        """Function check password"""

        if self.check_user_exists(name):
            command = """
                select pass from users where name='%s';
            """ %(name)
            self.cursor.execute(command)
            self.connection.commit()
            password = self.cursor.fetchone()
            return password[0] == input_password
        return False

    def add_message(self,name:str, to_user:str, message:str)-> bool:
        """Function send message"""

        if self.check_user_exists(name) and self.check_user_exists(to_user):
            self.cursor.execute('''select id from users where name='%s';'''%(name))
            self.connection.commit()
            name_id = self.cursor.fetchone()
            self.cursor.execute('''select id from users where name='%s';'''%(to_user))
            self.connection.commit()
            to_user_id = self.cursor.fetchone()
            command = """
                insert into message(id_user, user_from, message) values(%i,%i,'%s'); 
            """ %(to_user_id[0], name_id[0], message)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False
        

    def del_message(self, name:str, number_message:int)-> bool:
        """Function delete message"""

        if self.check_user_exists(name):
            command = """
                delete from message where id='%s';
            """ %(name)
            self.cursor.execute(command)
            self.connection.commit()
            return True
        return False

    def list_message(self)-> list:
        """Function list message"""

        pass

    def change_user_password(self,name:str, old_password:str, new_passsword:str) -> bool:
        """Function change password"""

        if self.check_user_exists(name) and self.check_user_password(name, old_password):
            command = """
                update users set pass='%s' where name='%s';
            """ %(new_passsword, name)
            self.cursor.execute(command)
            self.connection.commit()
            return self.check_user_password(name, new_passsword)
        return False


    def check_admin(self, name:str) -> bool:
        """Function checking admin users"""

        if self.check_user_exists(name):
            command = """
                select admin from users where name='%s';
            """ %(name)
            self.cursor.execute(command)
            self.connection.commit()
            admin = self.cursor.fetchone()
            return admin[0]
        return False

    def count_message(self)-> bool:
        """Function count message"""

        pass

db = Data_base_sql()
print(db.add_message('tomek','tomek111','asfasf'))