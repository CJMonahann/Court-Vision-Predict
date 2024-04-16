from app.ai_model import AppDecisionTree as ADT

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
