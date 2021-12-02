from flask import Flask, render_template, redirect, session, request
from flask_app import app


from flask_app.models.player import Player
from flask_app.models.team import Team
from flask_app.models.game import Game
from flask_app.models.indiv_game import Indiv_Game


@app.route('/test4')
def test4():
    print('INSERTING ALL TEAMS')
        #un - comment and run if you deleted it all lol
    # Team.insert_all_teams()

    return redirect('/')

@app.route('/teams')
def teams():
    return render_template('teams.html',teams = Team.get_all())

@app.route('/teams/<id>')
def team_page(id):
    return render_template('team_page.html',team = Team.get_one({'id':id}))



