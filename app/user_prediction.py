from app import db
from flask_sqlalchemy import SQLAlchemy
from app.ai_model import AppDecisionTree as ADT

class UserPrediction(db.Model): # trying out db out for this, not sure where to place it
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.String(255), nullable=False)
    home_team = db.Column(db.String(255), nullable=False)
    visiting_team = db.Column(db.String(255), nullable=False)
    user_prediction = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def __getPredictedGames():
    result = ADT().predict_games()
    gameDate=[]
    teams=[]
    cvpPrediction=[]
    for date, game in result.items():
        for i in range(len(game)):
            gameDate.append(date)
            teams.append([game[i]['home'],game[i]['visitors']])
            cvpPrediction.append(game[i]['prediction'])

    return gameDate,teams,cvpPrediction
