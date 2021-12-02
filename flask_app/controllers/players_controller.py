from flask import Flask, render_template, redirect, session, request
from flask_app import app


from flask_app.models.player import Player
from flask_app.models.team import Team
from flask_app.models.game import Game
from flask_app.models.indiv_game import Indiv_Game
from flask_app.models.user import User
from flask_app.models.api import get_player_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    if 'user_id' in session:
        user = User.get_one({'id':session['user_id']})
        if (user.level == '0'):
            return redirect ('/')
        else:
            return render_template('db_setup.html')
            
    return redirect('/')



@app.route('/test2')
def test2():
    print('INSERTING PLAYERS')
    #un - comment and run if you deleted it all lol
    # Player.insert_all_players()

    return redirect('/')
    

@app.route('/position', methods=['POST'])
def positon():
    data = request.form
    # print(data)
    positinal_group=Player.get_by_position(data)
    print(positinal_group[1].name)
    return redirect('/')

@app.route('/players')
def players():
    return render_template('players.html', players = Player.get_all())

@app.route('/players/<position>')
def players_positon(position):
    return render_template('players.html',players = Player.get_by_position({'position':position}))

@app.route('/players/<int:id>')
def player_page(id):
    player = Player.get_one({'id':id})
    bonus_data = get_player_data(player)
    return render_template('player_page.html',player =player, bonus_data = bonus_data)
