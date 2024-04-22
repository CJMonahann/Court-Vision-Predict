from flask import render_template, jsonify, Flask, request, redirect, url_for, abort
from app import app, db
from dotenv import load_dotenv
import requests
import sys, os
from app import user_prediction as upd

#ADDED AS AN EXAMPLE FOR THE DUMMY DATA
from app import make_accounts_example as mae
from app.models import Accounts

load_dotenv()  # Load environment variables from .env file

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/news')
def get_news():
    api_key = os.getenv('NEWS_API_KEY')
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

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/user/<int:user_id>')
def user_page(user_id):
    # Query the user from the database based on user_id
    user = Accounts.query.get(user_id)

    # If user not found, return a 404 error page
    if not user:
        abort(404)

    # Render the user.html template and pass the user data
    return render_template('user.html', user=user)

@app.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    user = Accounts.query.get(user_id)
    if not user:
        abort(404)

    if request.method == 'POST':
        # Update user profile based on form data
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.city = request.form['city']
        user.state = request.form['state']
        user.favorite_team = request.form['favorite_team']
        # Update other fields similarly

        # Commit changes to the database
        db.session.commit()

        # Redirect to the user profile page
        return redirect(url_for('user_page', user_id=user.id))

    # Render the edit profile template with the user data
    return render_template('edit_profile.html', user=user)

@app.route('/predictions')
def predictions():
    gameDate,teams,cvpPrediction=upd.__getPredictedGames()
    return render_template('prediction-page.html',gameDate=gameDate,teams=teams,cvpPrediction=cvpPrediction)

@app.route('/popular_players')
def popular_players_page():
    return render_template('popular_players.html')

@app.route('/nba_standings')
def get_nba_standings():
    season = request.args.get('season', '2023')  # Default season if not provided

    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"league": "standard", "season": season}
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPIDAPI_HOST')
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        standings_data = response.json()
        return jsonify(standings_data)
    else:
        return jsonify({'error': 'Failed to fetch NBA standings'}), 500

@app.route('/teams_pages')
def teams_page():
    return render_template('teams_page.html')

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