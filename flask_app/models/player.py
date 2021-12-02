from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import numpy as np
import pandas as pd

from flask_app.models import game, team, indiv_game

from flask_app import app



class Player:
    schema = 'football_schema'
    #convert csv to a pandas dataframe
    df = pd.read_csv('/Users/natesavage/Documents/coding_dojo/python_stack/nfl_project/flask_app/static/nfl_pass_rush_receive_raw_data.csv') 
    acceptable_positions = {'RB':1,'WR':1,'QB':1,'TE':1,'FB':1}
    def __init__(self, data):
        self.id = data['id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        #ADD MORE HERE
        self.position = data['position']
        self.name = data['name']
        self.uniq = data['uniq']
        self.indiv_games = []
        self.current_team=''
        self.type='player'



    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM players JOIN indiv_games ON players.id = indiv_games.player_id JOIN games ON games.id = indiv_games.game_id WHERE players.id = %(id)s ORDER BY games.date DESC;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        player = cls(result[0])
        list_of_games =[]
        for data in result:
            indiv_dict = {
                'id':data['indiv_games.id'],
                'updated_at' : data['updated_at'],
                'created_at' : data['created_at'],
                #miscellaneous
                'fumbles' : data['fumbles'],
                'two_pt_conv' : data['two_pt_conv'],
                # deals with not calling self
                'game_id' :data['game_id'],
                'team_id':data['team_id'],
                'player': player,
                #receiving
                'targets' : data['targets'],
                'receptions' : data['receptions'],
                'rec_yards' : data['rec_yards'],
                'rec_long' : data['rec_long'],
                'rec_tds' : data['rec_tds'],
                #passing
                'pass_cmp' : data['pass_cmp'],
                'pass_att' : data['pass_att'],
                'pass_yards' :data['pass_yards'],
                'ints': data['ints'],
                'sacks': data['sacks'],
                'sack_yards' : data['sack_yards'],
                'pass_long': data['pass_long'],
                'pass_tds' : data['pass_tds'],
                #rushing 
                'rush_att' : data['rush_att'],
                'rush_yards' : data['rush_yards'],
                'rush_tds' : data['rush_tds'],
                'rush_long' : data['rush_long']
            }
            list_of_games.append(indiv_game.Indiv_Game(indiv_dict))
        player.indiv_games = list_of_games
        return player
    
    @classmethod
    def get_shallow_player(cls, data):
        query = 'SELECT * FROM players WHERE id = %(id)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM players;'
        result = connectToMySQL(cls.schema).query_db(query)
        players=[]
        for row in result:
            players.append(cls(row))
        return players

    @classmethod
    def get_by_position(cls,data):
        query = 'SELECT * FROM players WHERE position = %(position)s;'
        result = connectToMySQL(cls.schema).query_db(query,data)
        players=[]
        for row in result:
            players.append(cls(row))
        return players

    @classmethod
    def get_by_uniq(cls, data):
        query = 'SELECT * FROM players WHERE uniq = %(uniq)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        return cls(result[0])


    @classmethod
    def remove(cls, data):
        query = 'DELETE FROM players WHERE id = %(id)s;'
        connectToMySQL(cls.schema).query_db(query, data)
    
    @classmethod
    def insert(cls, data):
        query = 'INSERT INTO PLAYERS (name, position, uniq, updated_at, created_at) VALUES (%(name)s, %(position)s, %(uniq)s, NOW(), NOW());'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return result
    
    @staticmethod
    def player_dict(row):
        dict={
        'name': row['player'],
        'uniq':row['player_id'],
        'position':row['pos']
        }
        return dict
    
    #put player list as a class method and put the df of all player data into players? maybe there's a better way
    #to create some sort of global variable? maybe the init? but this is all about initializing my db so ...
    @classmethod
    def player_list(cls):
        dict_of_dicts ={}
        for i in range((len(cls.df.index))):
            if  (not (cls.df.iloc[i]['player_id'] in dict_of_dicts)) and (cls.df.iloc[i]['pos'] in cls.acceptable_positions):
                dict_of_dicts[cls.df.iloc[i]['player_id']] = cls.player_dict(cls.df.iloc[i])
        return dict_of_dicts
    
    #ONLY RUN ONCE OR THINGS WILL BE BAD
    #or maybe just use a validor lol
    @classmethod
    def insert_all_players(cls):
        for player in cls.player_list().values():
            # put into the db
            cls.insert(player)
        return cls.get_all()







# all_players = Player.player_list()

# print(all_players.values())

