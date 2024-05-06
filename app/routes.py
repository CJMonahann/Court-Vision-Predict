from flask import render_template, jsonify, Flask, request, redirect, url_for, abort, session
from app import app, db
from dotenv import load_dotenv
import requests
import sys, os
from app import user_prediction as upd
from .models import db, Players, PlayerStatistics, NbaTeams
from .nba_data_teams import populate_nba_teams, get_nba_standings
from .nba_data_players import fetch_players_from_api, fetch_player_statistics
#ADDED AS AN EXAMPLE FOR THE DUMMY DATA
from app import make_accounts_example as mae
from app.models import Accounts, UserPrediction
from app import collect_players as cPlrs
from app.forms import signUpForm # Makes forms functional in routes
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=5) #Sets the maximum time before user is logged out as 5 days
import random #allows use of random number generation for user ID
random.seed(3)
load_dotenv()  # Load environment variables from .env file
import os

@app.route('/')
def index():
    if "user_name" in session:
        return render_template('landing_page_authenticated.html') 
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

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = signUpForm()
    print("Login page accessed.")  # Debug statement
    if "user_name" in session:
        print("User already logged in. Redirecting...")  # Debug statement
        return redirect(url_for("landing_page_authenticated"))
    if form.validate_on_submit():
        print("Form validated.")  # Debug statement
        input_username = form.user_name.data
        input_email = form.email.data
        input_password = form.password.data
        print("Submitted username:", input_username)  # Debug statement
        print("Submitted email:", input_email)  # Debug statement
        print("Submitted password:", input_password)  # Debug statement
        logged_user = Accounts.query.filter_by(user_name=input_username, email=input_email).first()
        if logged_user is None:
            print("User not found, please try again.")  # Debug statement
        elif logged_user.password != input_password:  # Assuming password is stored as plaintext
            print("Password incorrect, please try again.")  # Debug statement
        else:
            print("You have been logged in.")  # Debug statement
            session['user_name'] = input_username
            print("Session user_name set to:", input_username)  # Debug statement
            print("Redirecting to landing page...")  # Debug statement
            return redirect(url_for("landing_page_authenticated"))
    else:
        print("Form validation failed.")  # Debug statement
        print("Form errors:", form.errors)  # Debug statement
    return render_template('login.html', form=form)


@app.route('/landing_page_authenticated')
def landing_page_authenticated():
    if "user_name" in session:
        return render_template('landing_page_authenticated.html')
    else:
        print("User not logged in. Redirecting to login page...")
        return redirect(url_for('login_page'))
    
@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user_name', None)
    # Redirect the user to the login page
    return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = signUpForm()
    if form.validate_on_submit():
       password = form.password.data
       logged_user = Accounts(user_name=form.user_name.data, email=form.email.data, password=password)
       db.session.add(logged_user)
       db.session.commit()
       return redirect(url_for('login_page'))
    return render_template('signup.html', form=form)

@app.route('/user')
def user():
    # Check if user_name is stored in session
    if 'user_name' not in session:
        return redirect(url_for('login_page'))  # Redirect to login page if not logged in

    user_name = session['user_name']
    
    # Query the user from the database based on user_name
    user = Accounts.query.filter_by(user_name=user_name).first()

    # If user not found, return a 404 error page
    if not user:
        abort(404)

    # Render the user.html template and pass the user data
    return render_template('user.html', user=user)


@app.route('/user/<string:user_name>')
def user_page(user_name):
    # Query the user from the database based on user_name
    user = Accounts.query.filter_by(user_name=user_name).first()

    # If user not found, return a 404 error page
    if not user:
        abort(404)

    # Render the user.html template and pass the user data
    return render_template('user.html', user=user)

@app.route('/edit-profile/<string:user_name>', methods=['GET', 'POST'])
def edit_profile(user_name):
    user = Accounts.query.filter_by(user_name=user_name).first()
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
        return redirect(url_for('user_page', user_name=user.user_name))

    # Render the edit profile template with the user data
    return render_template('edit_profile.html', user=user)

@app.route('/predictions')
def predictions():
    # Check if user is authenticated
    if 'user_name' in session:
        # User is authenticated, redirect to predictions_auth.html
        return redirect(url_for('predictions_auth'))
    
    # If user is not authenticated, render prediction-page.html
    gameDate, teams, cvpPrediction = upd.__getPredictedGames()
    return render_template('prediction-page.html', gameDate=gameDate, teams=teams, cvpPrediction=cvpPrediction)

@app.route('/predictions_auth')
def predictions_auth():
    # Add logic here to fetch data or perform actions related to the authenticated predictions page
    gameDate, teams, cvpPrediction = upd.__getPredictedGames()
    return render_template('predictions-page_auth.html', gameDate=gameDate, teams=teams, cvpPrediction=cvpPrediction)

@app.route('/popular_players')
def popular_players_page():
    # Check if user is authenticated
    if 'user_name' in session:
        # User is authenticated, render popular_players_auth.html
        return render_template('popular_players_auth.html')
    
    # If user is not authenticated, render popular_players.html
    return render_template('popular_players.html')

@app.route('/popular_players_auth')
def popular_players_auth():
    # Add logic here to fetch data or perform actions related to the authenticated popular players page
    return render_template('popular_players_auth.html')

@app.route('/teams_pages')
def teams_page():
    # Check if user is authenticated
    if 'user_name' in session:
        # User is authenticated, redirect to teams_page_auth.html
        return redirect(url_for('teams_page_auth'))
    
    # If user is not authenticated, render teams_page.html
    return render_template('teams_page.html')

@app.route('/teams_pages_auth')
def teams_page_auth():
    # Add logic here to fetch data or perform actions related to the authenticated teams page
    return render_template('teams_page_auth.html')


@app.route('/prediction/submit', methods=['POST', 'GET'])
def userPredictionSubmit():
    if 'user_name' in session:
        account = Accounts.query.filter_by(user_name=session['user_name']).first()
        userID = account.id

        if request.method == 'POST':
            user_id = userID
            form_id = request.form['form_id']
            game_date = request.form['game_date']
            home_team = request.form['home_team']
            visiting_team = request.form['visiting_team']
            user_prediction = request.form['prediction']
        
            existing_prediction = UserPrediction.query.filter_by(user_id=user_id, form_id=form_id, game_date=game_date, home_team=home_team, visiting_team=visiting_team, user_prediction=user_prediction).first()
            if existing_prediction:
                return jsonify({'success': False, 'message': 'User has already made a prediction for this game'})   
        
            new_prediction = UserPrediction(user_id=user_id, form_id=form_id, game_date=game_date, home_team=home_team, visiting_team=visiting_team, user_prediction=user_prediction)
            db.session.add(new_prediction)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Prediction submitted successfully'})
    
        elif request.method == 'GET':
            user_id = userID
            form_id = request.args.get('form_id')
            user_submission = UserPrediction.query.filter_by(user_id=user_id, form_id=form_id).first()

            if user_submission:
                return jsonify({'success': True, 'prediction': user_submission.user_prediction})
            else:
                return jsonify({'success': False, 'message': 'No prediction found for this game'})
    else:
        return jsonify({'warning': 'No User in Current Session'})


#ALL OF THIS CODE IS JUST TO POPULATE DB WITH EXAMPLE ACCS - THIS ROUTE (and all files) WILL BE REMOVED

acc_obj = mae.MakeAccounts()
@app.route('/pop_accounts')
def pop_accounts(acc_obj = acc_obj):
    if acc_obj.num_calls <= 0: #will only be called once every time you run the flask app
        acc_obj.populate_accounts() #this creates the fake accounts to use for now, and increments 'num_calls'
        print('EXAMPLE ACCOUNTS CREATED')

    all_accounts = db.session.query(Accounts).all()
    return render_template('pop_accounts_example.html', accounts = all_accounts)


'''
collect_players = cPlrs.CollectPlayers()
all_teams = [31, 19, 14, 23, 8, 11, 30, 17, 28, 16, 29, 40, 9, 22, 25, 41, 5, 1, 20, 26, 10, 6, 15, 7, 21, 38, 4, 27, 24, 2]
@app.route('/pop_players')
def pop_players(collect_players = collect_players, teams_arr = all_teams):
    if collect_players.num_calls <= 0: #will only be called once every time you run the flask app
        db.drop_all()
        db.create_all()
        print('DATABASE REFRESHED - Collecting Players ...')
        collect_players.get_players(teams_arr) #collects players for team used in our app

    #all_accounts = db.session.query(Accounts).all()
    return render_template('landingpage.html')
'''

# Route to populate NBA teams
@app.route('/populate_nba_teams', methods=['GET'])
def populate_nba_teams_route():
    # Check if the request is from the database
    from_db = request.args.get('from_db', '').lower() == 'true'
    # Call populate_nba_teams function based on the source of data
    return populate_nba_teams() if from_db else populate_nba_teams(standings_data=get_nba_standings())

# Route to get NBA standings
@app.route('/nba_standings', methods=['GET'])
def get_nba_standings_route():
    # Get the season from the request, default is '2023'
    season = request.args.get('season', '2023')
    # Return NBA standings for the requested season
    return jsonify(get_nba_standings(season))

@app.route('/players/<int:team_id>')
def get_players(team_id):
    players = Players.query.filter_by(team_id=team_id).all()
    player_data = [
        {
            "api_id": player.api_id,  # Include the api_id
            "first_name": player.first_name,
            "last_name": player.last_name,
            "position": player.position,
            "num_jersey": player.num_jersey
        }
        for player in players
    ]
    return jsonify(player_data)


# Route to fetch player statistics by player ID
@app.route('/player_statistics/<int:player_id>')
def get_player_statistics(player_id):
    # Assuming PlayerStatistics is your SQLAlchemy model
    player_stats = PlayerStatistics.query.filter_by(player_id=player_id).first()
    if player_stats:
        # Return player statistics as JSON response
        return jsonify({
            "points": player_stats.points,
            "min": player_stats.min,
            "fgm": player_stats.fgm,
            "fga": player_stats.fga,
            "fgp": player_stats.fgp,
            "ftm": player_stats.ftm,
            "fta": player_stats.fta,
            "ftp": player_stats.ftp,
            "tpm": player_stats.tpm,
            "tpa": player_stats.tpa,
            "tpp": player_stats.tpp,
            "off_reb": player_stats.off_reb,
            "def_reb": player_stats.def_reb,
            "tot_reb": player_stats.tot_reb,
            "assists": player_stats.assists,
            "p_fouls": player_stats.p_fouls,
            "steals": player_stats.steals,
            "turnovers": player_stats.turnovers,
            "blocks": player_stats.blocks,
            "plus_minus": player_stats.plus_minus,
            "comment": player_stats.comment
        })
    else:
        # Return empty JSON object with 404 status code if player stats not found
        return jsonify({}), 404

@app.route('/leaders/json')
def leaders_json():
    # Join PlayerStatistics with Players table to get player information
    leaders_query = db.session.query(PlayerStatistics, Players.first_name, Players.last_name).join(Players, PlayerStatistics.player_id == Players.api_id)

    # Get top 10 leaders for each statistic
    points_leaders = leaders_query.order_by(PlayerStatistics.points.desc()).limit(20).all()
    assists_leaders = leaders_query.order_by(PlayerStatistics.assists.desc()).limit(20).all()
    rebounds_leaders = leaders_query.order_by(PlayerStatistics.tot_reb.desc()).limit(20).all()

    # Prepare data for JSON response
    points_data = [{'api_id': leader[0].player_id, 'first_name': leader[1], 'last_name': leader[2], 'points': leader[0].points} for leader in points_leaders]
    assists_data = [{'api_id': leader[0].player_id, 'first_name': leader[1], 'last_name': leader[2], 'assists': leader[0].assists} for leader in assists_leaders]
    rebounds_data = [{'api_id': leader[0].player_id, 'first_name': leader[1], 'last_name': leader[2], 'rebounds': leader[0].tot_reb} for leader in rebounds_leaders]

    return jsonify({
        'points_leaders': points_data,
        'assists_leaders': assists_data,
        'rebounds_leaders': rebounds_data
    })
    
if __name__ == '__main__':
    app.run(debug=True)
    
@app.route('/predict_data')
def predict_data():
    pred = db.session.query(UserPrediction).all()
    return render_template('predict_data.html', pred = pred)