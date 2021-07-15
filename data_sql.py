import os
import json
import psycopg2

class Sql():
    """Class of communication with the database"""

    def __init__(self) -> None:
        self.__load_config()
        self.connection = psycopg2.connect(
                                host="localhost",
                                database = self.__db_name,
                                user = self.__user_db,
                                password = self.__pass_db)
        self.cursor = self.connection.cursor()
    
    def __del__(self) -> None:
        self.cursor.close()
        self.connection.close()

    def __load_config(self) -> None:
        """Load config parameters"""

        if os.path.isfile('config.ini'):
             with open('config.ini', 'r') as outfile:
                data = json.load(outfile)
                self.__db_name = data['db_name']
                self.__user_db = data['user_db']
                self.__pass_db = data['pass_db']
        else:
            print('Configuration file not found')
            raise NameError('No configuration file')
    def check_table_exist(self, name_table:str) -> None:
        """Function that checks if the table is in the bottom database"""
        
        command = """
            SELECT 1 WHERE EXISTS (SELECT FROM information_schema.tables WHERE table_name = '%s');
        """ %(name_table)
        self.cursor.execute(command)
        self.connection.commit()
        return bool(self.cursor.fetchone())

    def setup(self) -> None:
        """Function create tables"""

        if not self.check_table_exist('users') and not self.check_table_exist('messages'):
            commands = (
                        """
                        CREATE TABLE IF NOT EXISTS users(
                            id_user SERIAL PRIMARY KEY,
                            name VARCHAR(25) NOT NULL UNIQUE,
                            pass VARCHAR(25) NOT NULL,
                            admin BOOLEAN DEFAULT FALSE
                        );
                        """,
                        """
                        CREATE TABLE IF NOT EXISTS messages(
                            id_mess SERIAL,
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
    
    def add_user(self, name:str, password:str, group = False) -> bool:
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
        return admin[0]


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