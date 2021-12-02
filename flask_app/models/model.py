from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class CHANGEME:
    schema = 'RENAME ME'
    def __init__(self, data):
        self.id = data['id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        #ADD MORE HERE


    @classmethod
    def get_one(cls,data):

        query = 'SELECT * FROM CHANGEME WHERE id = %(id)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def remove(cls, data):
        query = 'DELETE FROM CHANGEME WHERE id = %(id)s;'
        connectToMySQL(cls.schema).query_db(query, data)

