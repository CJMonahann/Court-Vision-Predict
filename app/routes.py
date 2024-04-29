from flask import render_template, jsonify, Flask, request, redirect, url_for, abort, sessions
from app import app, db
from dotenv import load_dotenv
import requests
import sys, os
from app import user_prediction as upd
from .models import db, Players
from .nba_data_teams import populate_nba_teams, get_nba_standings
from .nba_data_players import fetch_players_from_api, fetch_player_statistics
#ADDED AS AN EXAMPLE FOR THE DUMMY DATA
from app import make_accounts_example as mae
from app.models import Accounts
from app import collect_players as cPlrs
from app.forms import signUpForm # Makes forms functional in routes

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
    form = signUpForm() #should in theory allow user data to be sent to db, or at least set up the ability to do so
    if form.validate_on_submit():
       password = form.password.data
       logged_user = Accounts(username=form.username.data, email=form.email.data, password=password)
       db.session.add(logged_user)
       db.session.commit()
    #   flash('Account created. Please log in.') #currently nonfunctional, reminder to rewatch tutorial on flash messages
       return redirect('/login') #should send user to the login page once account is in db for final confirmation
    return render_template('signup.html', form = form )

@app.route('/user/<int:user_id>')
def user_page(user_id):
    # Query the user from the database based on user_id
    user = Accounts.query.get(user_id)

    # If user not found, return a 404 error page
    if not user:
        abort(404)

    # Render the user.html template and pass the user data
    return render_template('user.html', user=user)

    #'user/1' or 'user/2' for example

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

collect_players = cPlrs.CollectPlayers()
all_teams = [31, 19, 14, 23, 8, 11, 30, 17, 28, 16, 29, 40, 9, 22, 25, 41, 5, 1, 20, 26, 10, 6, 15, 7, 21, 38, 4, 27, 24, 2]
@app.route('/pop_players')
def pop_players(collect_players = collect_players, teams_arr = [1]):
    if collect_players.num_calls <= 0: #will only be called once every time you run the flask app
        db.drop_all()
        db.create_all()
        print('DATABASE REFRESHED - Collecting Players ...')
        collect_players.get_players(teams_arr) #collects players for team used in our app

    #all_accounts = db.session.query(Accounts).all()
    return render_template('landingpage.html')

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

# Route to fetch NBA players for a specific team
@app.route('/nba_players/<int:team_id>', methods=['GET'])
def fetch_nba_players_route(team_id):
    # Get the season from the request, default is '2023'
    season = request.args.get('season', '2023')
    try:
        # Fetch player data for the specified team and season
        players_data = fetch_players_from_api(team_id, season)
        # Return the player data as JSON response
        return jsonify({'status': 'success', 'players_data': players_data})
    except Exception as e:
        # If an error occurs during fetching, return an error message
        return jsonify({'status': 'error', 'message': str(e)})

# Route to fetch NBA player statistics for a specific player
@app.route('/nba_player_statistics/<int:player_id>', methods=['GET'])
def fetch_nba_player_statistics_route(player_id):
    # Get the season from the request, default is '2023'
    season = request.args.get('season', '2023')
    try:
        # Fetch player statistics for the specified player and season
        player_statistics = fetch_player_statistics(player_id, season)
        # Return the player statistics as JSON response
        return jsonify({'status': 'success', 'player_statistics': player_statistics})
    except Exception as e:
        # If an error occurs during fetching, return an error message
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    