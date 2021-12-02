from flask_app.config.mysqlconnection import connectToMySQL

import numpy as np
import pandas as pd

from flask_app.models import player, game, indiv_game

from flask_app import app


class Team:
    schema = 'football_schema'
    #convert csv to a pandas dataframe
    df = pd.read_csv('/Users/natesavage/Documents/coding_dojo/python_stack/nfl_project/flask_app/static/nfl_pass_rush_receive_raw_data.csv') 
    full_name_dict = {
    'GNB': 'Green Bay Packers',
    'CHI': 'Chicago Bears',
    'LAR': 'Los Angeles Rams',
    'CAR': 'Carolina Panthers',
    'TEN': 'Tennessee Titans',
    'CLE': 'Cleveland Browns',
    'DET': 'Detroit Lions',
    'ARI': 'Arizona Cardinals',
    'NYG': 'New York Giants',
    'DAL': 'Dallas Cowboys',
    'KAN': 'Kansas City Chiefs',
    'JAX': 'Jacksonville Jaguars',
    'MIA': 'Miami Dolphins',
    'BAL': 'Baltimore Ravens',
    'MIN': 'Minnesota Vikings',
    'ATL': 'Atlanta Falcons',
    'NWE': 'New England Patriots',
    'PIT': 'Pittsburgh Steelers',
    'BUF': 'Buffalo Bills',
    'NYJ': 'New York Jets',
    'WAS': 'Washington Football Team',
    'PHI': 'Philadelphia Eagles',
    'IND': 'Indianapolis Colts',
    'LAC': 'Los Angelos Chargers', 
    'CIN': 'Cincinnati Bengals', 
    'SEA': 'Seattle Seahawks', 
    'SFO': 'San Francisco 49ers', 
    'TAM': 'Tampa Bay Buccaneers', 
    'HOU': 'Houston Texans', 
    'NOR': 'New Orleans Saints',
    'DEN': 'Denver Broncos', 
    'LVR': 'Las Vegas Raiders'
    }

    def __init__(self, data):
        self.id = data['id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        #ADD MORE HERE
        self.name = data['name']
        self.abrev = data['abrev']
        self.games=[]
        self.type ='team'



    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM teams JOIN games ON teams.id = games.home_team_id OR teams.id = games.visitor_team_id WHERE teams.id = %(id)s ORDER BY games.date DESC;'
        # query = 'SELECT * FROM teams WHERE id = %(id)s;'
        result = connectToMySQL(cls.schema).query_db(query, data)
        team = cls(result[0])
        games =[]
        for row in result:
            game_dict={

                'id' : row['games.id'],
                'updated_at' : row['games.updated_at'],
                'created_at' : row['games.created_at'],
                'date':row['date'],
                'home_score' :row['home_score'],
                'visitor_score' : row['visitor_score'],
                'home_team_id' : row['home_team_id'],
                'visitor_team_id' : row['visitor_team_id'],
            }
            games.append(game.Game(game_dict))
        team.games = games
        return team
    

    @classmethod
    def get_shallow_team(cls,data):
        query = 'SELECT * FROM teams WHERE id=%(id)s;'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM teams;'
        result = connectToMySQL(cls.schema).query_db(query)
        teams=[]
        for row in result:
            teams.append(cls(row))
        return teams

    @classmethod
    def get_team_by_abrev(cls,data):
        query= 'SELECT * FROM teams WHERE abrev = %(abrev)s;'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return cls(result[0])



    @classmethod
    def remove(cls, data):
        query = 'DELETE FROM teams WHERE id = %(id)s;'
        connectToMySQL(cls.schema).query_db(query, data)
    
    @classmethod
    def insert(cls, data):
        query = 'INSERT INTO teams (name, abrev, updated_at, created_at) VALUES (%(name)s, %(abrev)s, NOW(), NOW());'
        result = connectToMySQL(cls.schema).query_db(query,data)
        return result
    
    #makes a dict of individual teams to insert
    @classmethod
    def team_dict(cls,row):
        team ={
            'abrev':row['team'],
            'name':cls.full_name_dict[row['team']]
        }
        return team
    
    @classmethod
    def all_team_dicts(cls):
        teams ={}
        for i in range(len(cls.df.index)):
            if not (cls.df.iloc[i]['team'] in teams):
                teams[cls.df.iloc[i]['team']]=cls.team_dict(cls.df.iloc[i])
        return teams

    #put all teams in DB be careful only run once!!!!
    @classmethod
    def insert_all_teams(cls):
        for team in cls.all_team_dicts().values():
            cls.insert(team)
        return cls.get_all()


# all_teams =Team.all_team_dicts()
# print(all_teams)
# print(len(all_teams.values()))

#can identify a game and not allow repeats by checking one team 
# against both stored and the game
