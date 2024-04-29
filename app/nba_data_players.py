# Import necessary libraries
import os  # For accessing environment variables
import requests  # For making HTTP requests
from flask import request, jsonify
from dotenv import load_dotenv
import app  # Import request and jsonify from flask
from .models import db, Players  # Import database models
load_dotenv('.env')

def fetch_players_from_api(team_id, season='2023'):
    # Define API endpoint and parameters
    url = "https://api-nba-v1.p.rapidapi.com/players"
    querystring = {"team": team_id, "season": season}
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
            # Return players data
            return json_response['response']
        else:
            # If response doesn't contain data, raise an exception
            raise Exception("API response does not contain players data")
    else:
        # Raise exception if request failed
        raise Exception("Failed to fetch data from API")
    
def fetch_player_statistics(player_id, season='2023'):
    # Define API endpoint and parameters
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
    querystring = {"id": player_id, "season": season}
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
            # Get the list of player statistics
            player_statistics = json_response['response']
            # Initialize variables to store sum of statistical data
            total_points = 0
            total_fgm = 0
            total_fga = 0
            total_ftm = 0
            total_fta = 0
            total_tpm = 0
            total_tpa = 0
            total_offReb = 0
            total_defReb = 0
            total_totReb = 0
            total_assists = 0
            total_pFouls = 0
            total_steals = 0
            total_turnovers = 0
            total_blocks = 0
            total_plusMinus = 0

            # Iterate through player statistics to calculate sum
            for stat in player_statistics:
                total_points += stat['points']
                total_fgm += stat['fgm']
                total_fga += stat['fga']
                total_ftm += stat['ftm']
                total_fta += stat['fta']
                total_tpm += stat['tpm']
                total_tpa += stat['tpa']
                total_offReb += stat['offReb']
                total_defReb += stat['defReb']
                total_totReb += stat['totReb']
                total_assists += stat['assists']
                total_pFouls += stat['pFouls']
                total_steals += stat['steals']
                total_turnovers += stat['turnovers']
                total_blocks += stat['blocks']
                total_plusMinus += int(stat['plusMinus'])

            # Calculate averages
            num_games = len(player_statistics)
            avg_points = total_points / num_games
            avg_fgm = total_fgm / num_games
            avg_fga = total_fga / num_games
            avg_ftm = total_ftm / num_games
            avg_fta = total_fta / num_games
            avg_tpm = total_tpm / num_games
            avg_tpa = total_tpa / num_games
            avg_offReb = total_offReb / num_games
            avg_defReb = total_defReb / num_games
            avg_totReb = total_totReb / num_games
            avg_assists = total_assists / num_games
            avg_pFouls = total_pFouls / num_games
            avg_steals = total_steals / num_games
            avg_turnovers = total_turnovers / num_games
            avg_blocks = total_blocks / num_games
            avg_plusMinus = total_plusMinus / num_games

            # Return averages
            return {
                'PTS': avg_points,
                'FGM': avg_fgm,
                'FGA': avg_fga,
                'FTM': avg_ftm,
                'FTA': avg_fta,
                'TPM': avg_tpm,
                'TPA': avg_tpa,
                'ORB': avg_offReb,
                'DRB': avg_defReb,
                'TRB': avg_totReb,
                'AST': avg_assists,
                'PF': avg_pFouls,
                'STL': avg_steals,
                'TOR': avg_turnovers,
                'BLK': avg_blocks,
                'PLUS MINUS': avg_plusMinus,
            }
        else:
            # If response doesn't contain data, raise an exception
            raise Exception("API response does not contain player statistics data")
    else:
        # Raise exception if request failed
        raise Exception("Failed to fetch data from API")