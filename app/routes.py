from flask import render_template, jsonify, Flask, request, redirect, url_for
from app import app
import requests
import sys
from app import user_prediction as upd

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/testAuth')
def test_auth():
    return render_template('landing_page_authenticated.html')

@app.route('/news')
def get_news():
    api_key = '993afd44706849768cc4008d9ce87f2b'
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

@app.route('/login.html', methods=["POST", "GET"])
def login_page():
    return render_template('login.html')

@app.route('/signup.html', methods=["POST", "GET"])
def signup_page():
    return render_template('signup.html')

@app.route('/predictions')
def predictions():
    gameDate,teams,cvpPrediction=upd.__getPredictedGames()
    return render_template('prediction-page.html',gameDate=gameDate,teams=teams,cvpPrediction=cvpPrediction)
