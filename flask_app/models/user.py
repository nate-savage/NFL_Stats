from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    schema = 'football_schema'
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.password = data['password']
        self.level = data['level']


    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        result = connectToMySQL(cls.schema).query_db(query)
        users=[]
        for row in result:
            users.append(User(row))
        return users
    
    @classmethod
    def create(cls, data):
        #take raw pw and hash it
        pw_hash = bcrypt.generate_password_hash(data['password'])
        hashed_data ={**data,  'password':pw_hash}

        query = 'INSERT INTO users (email, created_at, updated_at, password, level) VALUES ( %(email)s, NOW(), NOW(), %(password)s, 0) ;'
        
        results = connectToMySQL(cls.schema).query_db(query, hashed_data)
        return results
    
    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        user = User(result[0])
        return user
    
    @classmethod
    def remove(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        connectToMySQL(cls.schema).query_db(query, data)



    @classmethod
    def check_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def register_validator(cls,data):
        is_vaild = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email')
            is_vaild=False
        if cls.check_email({'email':data['email']}):
            flash('User already exists')
            is_valid = False
        if len(data['password'])<8:
            flash('Password must be at least 8 characters')
            is_vaild = False
        if data['password'] != data['confirm_password']:
            flash('Passwords must match')
            is_vaild =False
        return is_vaild



