import numpy as np
import pandas as pd
import time

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import player, team, game

from flask_app import app


#all data is from https://www.advancedsportsanalytics.com/nfl-raw-data

class Indiv_Game:
    df = pd.read_csv('/Users/natesavage/Documents/coding_dojo/python_stack/nfl_project/flask_app/static/nfl_pass_rush_receive_raw_data.csv') 
    schema = 'football_schema'
    def __init__(self, data):
        #standard stuff
        self.id = data['id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        #miscellaneous
        self.fumbles = data['fumbles']
        self.two_pt_conv = data['two_pt_conv']
        # deals with not calling self
        if('game' in data):
            self.game = data['game']
        else:
            self.game = game.Game.get_one({'id':data['game_id']})
        #FIXed
        if('team' in data):
            self.team = data['team']
        else:
            self.team = team.Team.get_shallow_team({'id':data['team_id']})
        #FIXed
        if('player' in data):
            self.player = data['player']
        else:
            self.player = player.Player.get_shallow_player({'id':data['player_id']})
        #receiving
        self.targets = data['targets']
        self.receptions = data['receptions']
        self.rec_yards = data['rec_yards']
        self.rec_long = data['rec_long']
        self.rec_tds = data['rec_tds']
        #passing
        self.pass_cmp = data['pass_cmp']
        self.pass_att = data['pass_att']
        self.pass_yards =data['pass_yards']
        self.ints = data['ints']
        self.sacks = data['sacks']
        self.sack_yards = data['sack_yards']
        self.pass_long= data['pass_long']
        self.pass_tds = data['pass_tds']
        #rushing 
        self.rush_att = data['rush_att']
        self.rush_yards = data['rush_yards']
        self.rush_tds = data['rush_tds']
        self.rush_long = data['rush_long']
        #other
        self.type = 'indiv_game'
        self.tds = self.pass_tds+self.rush_tds+self.rec_tds
        self.yards = self.rec_yards+self.rush_yards+self.pass_yards



    @classmethod
    def get_one(cls,data):

        query = 'SELECT * FROM indiv_games WHERE id = %(id)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM indiv_games;'
        result = connectToMySQL(cls.schema).query_db(query)
        indiv_games=[]
        for row in result:
            indiv_games.append(cls(row))
        return indiv_games
    
    @classmethod
    def get_by_player(cls,data):
        query = 'SELECT * FROM indiv_games WHERE player_id =%(player_id)s;'
        result = connectToMySQL(cls.schema).query_db(query,data)
        player_games=[]
        for row in result:
            player_games.append(cls(row))
        return player_games

    @classmethod
    def remove(cls, data):
        query = 'DELETE FROM indiv_games WHERE id = %(id)s;'
        connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def add_indiv_game(cls,data):
        query = 'INSERT INTO indiv_games '
        result = connectToMySQL(cls.schema).query_db(query,data)
        return result
    
    @staticmethod
    def indiv_dict(row):
        dict ={
            #recevieing
            'targets': row['targets'],
            'receptions': row['rec'],
            'rec_yards': row['rec_yds'],
            'rec_tds':row['rec_td'],
            'rec_long':row['rec_long'],
            #rushing
            'rush_att':row['rush_att'],
            'rush_yards':row['rush_yds'],
            'rush_tds':row['rush_td'],
            'rush_long':row['rush_long'],
            #passing
            'pass_cmp':row['pass_cmp'],
            'pass_att':row['pass_att'],
            'pass_yards':row['pass_yds'],
            'pass_tds':row['pass_td'],
            'sacks':row['pass_sacked'],
            'sack_yards':row['pass_sacked_yds'],
            'ints':row['pass_int'],
            'pass_long':row['pass_long'],
            #miscellaneous
            'fumbles':row['fumbles_lost'],
            'two_pt_conv':row['two_point_conv'],
            #methods to get ids below
            'team_id':( team.Team.get_team_by_abrev({'abrev':row['team']}).id), 
            'game_id':game.Game.get_by_home_date({'date':row['game_date'], 'home_team_id':(team.Team.get_team_by_abrev({'abrev': row['home_team']})).id}).id,
            'player_id': player.Player.get_by_uniq({'uniq':row['player_id']}).id
        }
        return dict
    
    @classmethod
    def get_by_game(cls, data):
        query = 'SELECT * FROM indiv_games WHERE game_id = %(game_id)s;'
        result = connectToMySQL(cls.schema).query_db(query,data)
        indiv_games =[]
        #home teams
        for row in result:
            indiv_games.append(cls(row))
        return indiv_games

    @classmethod
    def all_game_dicts(cls):
        all_games = []
        for i in range(len(cls.df.index)):
            time.sleep(.05)
            if (cls.df.iloc[i]['pos'] in player.Player.acceptable_positions):
                all_games.append(cls.indiv_dict(cls.df.iloc[i]))
        return all_games
    
    @classmethod
    def insert_game(cls, data):
        query = 'INSERT INTO indiv_games (player_id, game_id, team_id, pass_cmp, pass_att, pass_yards, ints, sacks, sack_yards, pass_long, rush_att, rush_yards, rush_tds, pass_tds, rush_long, targets, receptions, rec_yards, rec_tds, rec_long, fumbles, two_pt_conv, updated_at, created_at) VALUES (%(player_id)s,%(game_id)s,%(team_id)s,%(pass_cmp)s,%(pass_att)s,%(pass_yards)s,%(ints)s,%(sacks)s,%(sack_yards)s,%(pass_long)s,%(rush_att)s,%(rush_yards)s,%(rush_tds)s,%(pass_tds)s,%(rush_long)s,%(targets)s,%(receptions)s,%(rec_yards)s,%(rec_tds)s,%(rec_long)s,%(fumbles)s,%(two_pt_conv)s,NOW(),NOW());'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return result


    @classmethod
    def insert_all_games(cls):
        all_games = cls.all_game_dicts()
        for game in all_games:
            cls.insert_game(game)
        return



