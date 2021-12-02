from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import numpy as np
import pandas as pd

from flask_app.models import player, team, indiv_game, game

from flask_app import app


class Advanced_Stat:
    schema = 'football_schema'
    #convert csv to a pandas dataframe
    

    def __init__(self, data):
        self.type = data['type']

    @classmethod
    def query_gen(cls, data):
        if data['type'] == 'players':
            #go to players query
            return cls.player_q(data)
        elif data['type'] == 'teams':
            # go to teams
            return cls.team_q(data)
        elif data['type'] =='games':
            #go to games
            return cls.game_q(data)
        elif data['type']=='indiv_games':
            return cls.indiv_game_q(data)

    @classmethod
    def player_q(cls,data):
        pass

    @classmethod
    def team_q(cls,data):
        pass

    @classmethod
    def game_q(cls,data):
        pass

    @classmethod
    def indiv_game_q(cls, data):
        result={}
        query = 'SELECT * FROM indiv_games JOIN players ON indiv_games.player_id = players.id '
        #filter by position
        prev_where = False
        if data['position'] != 'none':
            query += 'WHERE players.position = %(position)s '
            prev_where = True
        #filter by team
        if data['team'] != 'none':
            if prev_where:
                query += ' AND '
            else:
                query += ' WHERE '
            query +='  indiv_games.team_id = %(team)s '
            
        #all this below could just be the special strings lol im a fool!
        if data['most']=='yards':
            query += 'ORDER BY (rec_yards + pass_yards + rush_yards) DESC'
            result['key_stat']='yards'
        elif data['most']=='tds':
            query +='ORDER BY (rec_tds + pass_tds +rush_tds) DESC'
            result['key_stat']='tds'
        elif data['most'] == 'rec_tds':
            query += 'ORDER BY rec_tds DESC'
            result['key_stat'] = 'rec_tds'
        elif data['most'] == 'rec_yards':
            query += 'ORDER BY rec_yards DESC'
            result['key_stat'] = 'rec_yards'
        elif data['most'] == 'rush_tds':
            query += 'ORDER BY rush_tds DESC'
            result['key_stat'] = 'rush_tds'
        elif data['most'] == 'rush_yards':
            query += 'ORDER BY rush_yards DESC'
            result['key_stat'] = 'rush_yards'
        elif data['most'] == 'pass_yards':
            query += 'ORDER BY pass_yards DESC'
            result['key_stat'] = 'pass_yards'
        elif data['most'] == 'pass_tds':
            query += 'ORDER BY pass_tds DESC'
            result['key_stat'] = 'pass_tds'
        

        #end the query
        query += ' LIMIT 100;'
        #return a list to be stored in session and passed along later
        result['query']=query
        result['data']=data
        result['obj_type']='indiv_game'
        return result


    @classmethod
    def query(cls,dict):
        query = dict['query']
        data = dict['data']
        obj_type = dict['obj_type']
        list =[]
        result = connectToMySQL(cls.schema).query_db(query, data)
        if obj_type == 'indiv_game':
            # return indiv_game.Indiv_Game(result[0])
            for row in result:
                list.append(indiv_game.Indiv_Game(row))
            return list
                
        elif obj_type == 'game':
            return game.Game(result[0])
        elif obj_type == 'team':
            return team.Team(result[0])
        elif obj_type == 'player':
            return player.Player(result[0])




