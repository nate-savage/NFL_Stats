import requests
import json
from flask_app.models import player, team, indiv_game

# api_key= '2'
# api_url_base = 'https://www.thesportsdb.com/api/v1'
# team_name = 'Ravens'
# player_name = 'Lamar%20Jackson'
# url_for_player = f'https://www.thesportsdb.com/api/v1/json/{api_key}/searchplayers.php?t={team_name}&p={player_name}'

# response = requests.get(url_for_player)
# player = response.json()
# print(player['player'][0]['idTeam'])

# api_url_base = 'https://www.thesportsdb.com/api/v1'


def get_player_data(player):
    team_name=''
    for char in player.indiv_games[0].team.name:
        if char == ' ':
            team_name+= '%20'
        else:
            team_name+=char
    player_name = ''
    for char in player.name:
        if char == ' ':
            player_name+= '%20'
        else:
            player_name+=char
    api_key= '2'
    url_for_player = f'https://www.thesportsdb.com/api/v1/json/{api_key}/searchplayers.php?t={team_name}&p={player_name}'
    response = requests.get(url_for_player)
    clean = response.json()
    
    player_dict ={}
    if clean['player'] == None:
        player_dict['height'] = 'unavailable'
        player_dict['weight'] = 'unavailable'
        return  player_dict
    cleaner = clean['player'][0]
    player_dict['height'] = cleaner['strHeight']
    player_dict['weight'] = cleaner['strWeight']
    return player_dict




# raw = {'player': [{'idPlayer': '34164817',
#     'idTeam': '134922',


#     'strPlayer': 'Lamar Jackson',
#     'strTeam': 'Baltimore Ravens',
#     'strTeam2': None,
#     'strSport': 'American Football',

#     'strBirthLocation': 'Pompano Beach, Florida',
#     'strDescriptionEN': 'Lamar Demeatrice Jackson Jr. (born January 7, 1997) is an American football quarterback for the Baltimore Ravens of the National Football League (NFL). He played college football at Louisville and was selected 32nd overall by the Ravens in the first round of the 2018 NFL Draft. At Louisville, Jackson won the Heisman Trophy, Maxwell Award, and Walter Camp Award and was a unanimous All-American as a sophomore in 2016.',

#     'strHeight': '6 ft 3 in (1.91 m)',
#     'strWeight': '212 lb (96 kg)',

#     'strThumb': 'https://www.thesportsdb.com/images/media/player/thumb/xkpk9z1547955406.jpg',}]}