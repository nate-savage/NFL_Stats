from flask import Flask, render_template, redirect, session, request
from flask_app import app

from flask_app.models.player import Player
from flask_app.models.team import Team
from flask_app.models.game import Game
from flask_app.models.indiv_game import Indiv_Game

@app.route('/games')
def games():
    games =Game.get_all()
    return render_template('games.html',games =games)

@app.route('/games/<id>')
def game_page(id):
    game = Game.get_one({'id':id})
    indiv_games = Indiv_Game.get_by_game({'game_id':id})
    return render_template('game_page.html',game=game, indiv_games = indiv_games)


#set up stuff
@app.route('/test5')
def test5():
    print('INSERTING ALL GAMES')
    #only run this once lol
    # Game.insert_all_games()

    return redirect('/')



