from flask import Flask, render_template, redirect, session, request
from flask_app import app


from flask_app.models.player import Player
from flask_app.models.team import Team
from flask_app.models.game import Game
from flask_app.models.indiv_game import Indiv_Game
from flask_app.models.advanced_stat import Advanced_Stat
from flask_app.models import api


@app.route('/search')
def search():
    return render_template('search.html', type='none')

@app.route('/search/<type>')
def search_type(type):
    teams = Team.get_all()
    return render_template('search.html',type = type, teams =teams)

#search post route
@app.route('/search/page', methods =['POST'] )
def search_page():
    #this logic stupid 
    data = request.form
    session['query'] = Advanced_Stat.query_gen(data)
    return redirect ('/search/display')


#display search
@app.route('/search/display')
def display_search():

    result = Advanced_Stat.query(session['query'])
    obj_type = result[0].type
    key_stat = session['query']['key_stat']
    return render_template('search_results.html', result = result, obj_type = obj_type, key_stat = key_stat)


@app.route('/search/<obj_type>/<id>')
def display_search_page(obj_type,id):
    obj_type = obj_type
    if obj_type == 'game':
        result = Game.get_one({'id':id})
    elif obj_type == 'team':
        result = Team.get_one({'id':id})
    elif obj_type =='indiv_game':
        result = Indiv_Game.get_one({'id':id})
    elif obj_type == 'player':
        result = Player.get_one({'id':id})
    return render_template('search_page.html', result = result, obj_type = obj_type)

