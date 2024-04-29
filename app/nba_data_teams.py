# Import necessary libraries
import os  # For accessing environment variables
import requests  # For making HTTP requests
from flask import request, jsonify
from dotenv import load_dotenv
import app  # Import request and jsonify from flask
from .models import db, NbaTeams  # Import database models
load_dotenv('.env')

# Function to fetch NBA standings from the API
def fetch_standings_from_api(season='2023'):
    # Define API endpoint and parameters
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"league": "standard", "season": season}
    # Set headers for the request including RapidAPI key and host
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": os.getenv('RAPIDAPI_HOST')
    }
    # Send GET request to the API
    response = requests.get(url, headers=headers, params=querystring)
    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        json_response = response.json()
        # Check if response contains data
        if 'response' in json_response:
            # Return standings data
            return json_response['response']
        else:
            # If response doesn't contain data, raise an exception
            raise Exception("API response does not contain standings data")
    else:
        # Raise exception if request failed
        raise Exception("Failed to fetch data from API")


# Function to populate NBA teams in the database
def populate_nba_teams(standings_data=None):
    # Check if the request is from the database
    from_db = request.args.get('from_db', '').lower() == 'true'
    if from_db:
        try:
            # Query all NBA teams from the database
            all_teams = NbaTeams.query.all()
            teams_info = []
            # Convert team data to JSON format
            for team in all_teams:
                team_info = {
                    "api_id": team.api_id,
                    "name": team.name,
                    "nickname": team.nickname,
                    "code": team.code,
                    "logo": team.logo,
                    "conference": team.conference,
                    "wins": team.wins,
                    "losses": team.losses,
                    "last_ten_wins": team.last_ten_wins,
                    "last_ten_losses": team.last_ten_losses,
                    "win_percentage": team.win_percentage,
                    "streak": team.streak
                }
                teams_info.append(team_info)
            # Return team data as JSON response
            return jsonify(teams_info), 200
        except Exception as e:
            # Return error message if an exception occurs
            return jsonify({"error": str(e)}), 500
    else:
        try:
            # Check if standings data is provided
            if standings_data is None:
                standings_data = fetch_standings_from_api()
            # Clear existing NBA teams data in the database
            db.session.query(NbaTeams).delete()
            # Populate NBA teams data from standings data
            for team_data in standings_data:
                team_info = team_data.get('team', {})
                conference_info = team_data.get('conference', {})
                win_info = team_data.get('win', {})
                loss_info = team_data.get('loss', {})
                # Create a new NbaTeams object and add it to the session
                new_team = NbaTeams(
                    api_id=team_info.get('id'),
                    name=team_info.get('name'),
                    nickname=team_info.get('nickname'),
                    code=team_info.get('code'),
                    logo=team_info.get('logo'),
                    conference=conference_info.get('name'),
                    wins=win_info.get('total'),
                    losses=loss_info.get('total'),
                    last_ten_wins=win_info.get('lastTen'),
                    last_ten_losses=loss_info.get('lastTen'),
                    win_percentage=float(win_info.get('percentage')),
                    streak=team_data.get('streak')
                )
                db.session.add(new_team)
            # Commit changes to the database
            db.session.commit()
            # Return success message as JSON response
            return jsonify({"message": "NBA teams populated successfully"}), 200
        except Exception as e:
            # Rollback changes if an exception occurs and return error message
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

# Function to get NBA standings data for a given season
def get_nba_standings(season='2023'):
    try:
        # Fetch NBA standings data for the specified season
        standings_data = fetch_standings_from_api(season)
        # Return the standings data
        return standings_data
    except Exception as e:
        # Return an error message if an exception occurs
        return {'error': str(e)}
