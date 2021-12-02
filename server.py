from flask_app import app
from flask_app.controllers import games_controller, players_controller, teams_controller, indiv_games_controller, advanced_stats_controller, users_controller



if (__name__=='__main__'):
    app.run(debug=True)