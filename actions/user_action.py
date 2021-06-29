from os import chdir
from ..models import user_model
import sqlite3
from hashlib import md5

class User_Action:
    def __init__(self, db_connection):
        self.db_connection=db_connection
    
    def login(self, user: user_model.User):
        conn = sqlite3.connect(self.db_connection)
        cursor = conn.cursor()
        sql = """
            SELECT * FROM tbl_user 
            WHERE user_name LIKE ? AND user_password LIKE ?
        """
        password = md5(user.user_password.encode()).hexdigest()
        cursor.execute(sql,(user.user_name, password))
        row = cursor.fetchone()
        if row == None:
            return 'Invalid username or password', 401
        authenticated_user = user_model.User(
            user_id=row[0],
            user_name=row[1],
            role=row[3]
        )
        return authenticated_user,200