from flask import render_template, jsonify, Flask, request, redirect, url_for
from app import app, db
import requests
import sys
from app import user_prediction as upd
import os

#ADDED AS AN EXAMPLE FOR THE DUMMY DATA
from app import make_accounts_example as mae
from app.models import Accounts, UserPrediction

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/news')
def get_news():
    api_key = os.getenv('__NEWS_API_KEY')
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        news_data = response.json()
        return jsonify(news_data)
    else:
        return jsonify({'error': 'Failed to fetch news'}), 500

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html')

@app.route('/predictions')
def predictions():
    userID = 1 # Change to the current session's user id 
    gameDate,teams,cvpPrediction=upd.__getPredictedGames()
    return render_template('prediction-page.html',user_id=userID,gameDate=gameDate,teams=teams,cvpPrediction=cvpPrediction)

@app.route('/prediction/submit', methods=['POST', 'GET'])
def userPredictionSubmit():
    if request.method == 'POST':
        user_id = request.form['user_id']
        form_id = request.form['form_id']
        game_date = request.form['game_date']
        home_team = request.form['home_team']
        visiting_team = request.form['visiting_team']
        user_prediction = request.form['prediction']
        print(user_id,game_date,home_team,visiting_team,user_prediction)
        
        existing_prediction = UserPrediction.query.filter_by(user_id=user_id, form_id=form_id, game_date=game_date, home_team=home_team, visiting_team=visiting_team, user_prediction=user_prediction).first()
        if existing_prediction:
            return jsonify({'success': False, 'message': 'User has already made a prediction for this game'})

        new_prediction = UserPrediction(user_id=user_id, form_id=form_id, game_date=game_date, home_team=home_team, visiting_team=visiting_team, user_prediction=user_prediction)
        db.session.add(new_prediction)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Prediction submitted successfully'})
    elif request.method == 'GET':
        user_id = request.args.get('user_id')
        form_id = request.args.get('form_id')
        game_date = request.args.get('game_date')
        home_team = request.args.get('home_team')
        visiting_team = request.args.get('visiting_team')
        user_prediction = request.args.get('prediction')
    
        # Query the database for the user's prediction for the specified form
        user_submission = UserPrediction.query.filter_by(user_id=user_id, form_id=form_id, game_date=game_date, home_team=home_team, visiting_team=visiting_team, user_prediction=user_prediction).first()
    
        if user_submission:
            return jsonify({'success': True, 'prediction': user_submission.user_prediction})
        else:
            return jsonify({'success': False, 'message': 'No prediction found for this game'})


#ALL OF THIS CODE IS JUST TO POPULATE DB WITH EXAMPLE ACCS - THIS ROUTE (and all files) WILL BE REMOVED
acc_obj = mae.MakeAccounts()
@app.route('/pop_accounts')
def pop_accounts(acc_obj = acc_obj):
    if acc_obj.num_calls <= 0: #will only be called once every time you run the flask app
        db.drop_all()
        db.create_all()
        acc_obj.populate_accounts() #this creates the fake accounts to use for now, and increments 'num_calls'
        print('DATABASE REFRESHED - EXAMPLE ACCOUNTS CREATED')

    all_accounts = db.session.query(Accounts).all()
    return render_template('pop_accounts_example.html', accounts = all_accounts)

@app.route('/predict_data')
def predict_data():
    pred = db.session.query(UserPrediction).all()
    return render_template('predict_data.html', pred = pred)