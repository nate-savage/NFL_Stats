from flask import Flask, render_template, redirect, session, request
from flask_app import app

from flask_app.models.player import Player
from flask_app.models.team import Team
from flask_app.models.game import Game
from flask_app.models.indiv_game import Indiv_Game


@app.route('/indiv_game/<id>')
def display_indiv_game(id):
    indiv_game = Indiv_Game.get_one({'id':id})
    player = indiv_game.player
    return render_template('indiv_game_page.html', indiv_game = indiv_game, player = player)

#set up route (add a session thing to make admin leve)
@app.route('/test6')
def test6():
    print('inserting all indiv games')
    #comment out if ran
    # Indiv_Game.insert_all_games()


    return redirect('/')


