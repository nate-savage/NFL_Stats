from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import numpy as np
import pandas as pd

from flask_app.models import player, team, indiv_game

from flask_app import app



class Game:
    schema = 'football_schema'
    #convert csv to a pandas dataframe
    df = pd.read_csv('/Users/natesavage/Documents/coding_dojo/python_stack/nfl_project/flask_app/static/nfl_pass_rush_receive_raw_data.csv') 

    def __init__(self, data):
        self.id = data['id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        #ADD MORE HERE
        self.date=data['date']
        self.home_score =data['home_score']
        self.visitor_score = data['visitor_score']
        #deals with not calling self infinitely
        if(not 'home_team' in data):
            self.home_team = team.Team.get_shallow_team({'id':data['home_team_id']})
        else:
            self.home_team = data['home_team']
        if(not 'visitor_team' in data):
            self.visitor_team = team.Team.get_shallow_team({'id':data['visitor_team_id']})
        else:
            self.visitor_team = data['visitor_team']
        self.type = 'game'





    @classmethod
    def get_one(cls,data):

        query = 'SELECT * FROM games WHERE id = %(id)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM games;'
        result = connectToMySQL(cls.schema).query_db(query)
        games=[]
        for row in result:
            games.append(cls(row))
        return games

    @classmethod
    def get_by_home_date(cls, data):
        query= 'SELECT * FROM games WHERE date = %(date)s AND home_team_id = %(home_team_id)s;'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return cls(result[0])

    @classmethod
    def remove(cls, data):
        query = 'DELETE FROM games WHERE id = %(id)s;'
        connectToMySQL(cls.schema).query_db(query, data)
    
    @classmethod
    def insert(cls, data):
        query = 'INSERT INTO games (date, home_score, visitor_score, home_team_id, visitor_team_id, created_at, updated_at) VALUES (%(date)s, %(home_score)s, %(visitor_score)s, %(home_team_id)s, %(visitor_team_id)s, NOW(), NOW());'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return result
    
    @staticmethod
    def game_dict(row):
        game ={
            #PUT STUFF HERE
            'date' : row['game_date'],
            'home_score':row['home_score'],
            'visitor_score':row['vis_score'],
            'home_team_id': team.Team.get_team_by_abrev({'abrev':row['home_team']}).id,
            'visitor_team_id':team.Team.get_team_by_abrev({'abrev':row['vis_team']}).id,
        }
        return game

    @classmethod
    def all_game_dicts(cls):
        games ={}
        for i in range(len(cls.df.index)):
            date_home = cls.df.iloc[i]['game_date']+cls.df.iloc[i]['home_team']
            if not (date_home in games):
                games[date_home]=cls.game_dict(cls.df.iloc[i])
        return games

    @classmethod
    def insert_all_games(cls):
        for game in cls.all_game_dicts().values():
            # print(game)
            cls.insert(game)
        return cls.get_all()

# all_games =Game.all_game_dicts()

# Game.insert_all_games()
# print((all_games.values()))
# print(len(all_games.keys())) #this number is how many games but it means nothig cause mid season lol

#can identify a game and not allow repeats by checking one home team 
# against both stored and the game
