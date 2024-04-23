import requests, os, json
from dotenv import load_dotenv
from app import db
from app.models import NbaTeams, Players

class CollectPlayers():
    load_dotenv('.env')

    def __init__(self):
        self.__API_KEY = os.getenv("__API_KEY")
        self.num_calls = 0

    def __collect_players(self, team_id, season = "2023"):

        url = "https://api-nba-v1.p.rapidapi.com/players"

        querystring = {"team":team_id,"season":season}

        headers = {
            "X-RapidAPI-Key": self.__API_KEY,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()

        #variables
        team_id = str(team_id)
        num_api_calls = 1
        MAX_CALLS = 401 #allowed called to be made to the API per minute (we have a restriction)

        if "response" in response:
            response = response["response"]

            for player in response:
                #collect player data
                player_id = player["id"]
                first_name = player["firstname"]
                last_name = player["lastname"]
                date_of_birth = player["birth"]["date"]
                country = player["birth"]["country"]
                starting_year = player["nba"]["start"]
                pro = player["nba"]["pro"]
                height = player["height"]["meters"] #collects height in meters
                weight = player["weight"]["pounds"]
                college = player["college"]
                affiliation = player["affiliation"]
                num_jersey = player["leagues"]["standard"]["jersey"]
                position = player["leagues"]["standard"]["pos"]
                active = player["leagues"]["standard"]["active"]

                #create database object and add record to the Players table
                create_player = Players(
                    api_id = player_id,
                    team_id = team_id,
                    first_name = first_name,
                    last_name = last_name,
                    date_of_birth = date_of_birth,
                    country = country,
                    starting_year = starting_year,
                    pro = pro,
                    height = height,
                    weight = weight,
                    college = college,
                    affiliation = affiliation,
                    num_jersey = num_jersey,
                    position = position,
                    active = active
                )

                db.session.add(create_player)
                db.session.commit()

                print(f'Player: {first_name} {last_name} added to database!')
        
    def get_players(self, arr):
        for team_id in arr:
            self.__collect_players(team_id)