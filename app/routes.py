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
from app.models import Accounts
from app import collect_players as cPlrs
from app.forms import signUpForm # Makes forms functional in routes
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=5) #Sets the maximum time before user is logged out as 5 days
import random #allows use of random number generation for user ID
random.seed(3)

load_dotenv()  # Load environment variables from .env file

@app.route('/')
def index():
    if "user" in session:
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

@app.route('/login')
def login_page():
    if "user" in session:
        return redirect(url_for("user"))    
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    form = signUpForm() #should in theory allow user data to be sent to db, or at least set up the ability to do so
    if form.validate_on_submit():
       #user_id = getrandbits(6) #Not working despite import of random module, look up why
       password = form.password.data
       logged_user = Accounts(username=form.username.data, email=form.email.data, password=password)
       db.session.add(logged_user)
       db.session.commit()
    #  flash('Account created. Please log in.') #currently nonfunctional, importing didn't work. Reminder to rewatch tutorial
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
    