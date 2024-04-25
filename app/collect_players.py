import requests, os, json, time
from dotenv import load_dotenv
from app import db
from app.models import Players, PlayerStatistics

class CollectPlayers():
    load_dotenv('.env')

    def __init__(self):
        self.__API_KEY = os.getenv("__API_KEY")
        self.num_calls = 0
        self.__num_API_calls = 0

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
        self.__num_API_calls += 1
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

                #collecr the player's stats and add them to the PlayerStatistics table
                if self.__num_API_calls >= MAX_CALLS: #then we need to wait
                    time.sleep(70)
                    self.__num_API_calls = 0

                self.__collect_player_stats(player_id)

                self.__num_API_calls += 1


    def __collect_player_stats(self, player_id, season = "2023"):

        url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

        querystring = {"id":str(player_id),"season":season}

        headers = {
            "X-RapidAPI-Key": self.__API_KEY,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()

        if "response" in response:
            response = response["response"] #returns stat history from all games played by the player
            player_info = response[-1] #we want the last recorded game for the most relevent stats

            points = player_info["points"]
            min = player_info["min"]
            fgm = player_info["fgm"]
            fga = player_info["fga"]
            fgp = player_info["fgp"]
            ftm = player_info["ftm"]
            fta = player_info["fta"]
            ftp = player_info["ftp"]
            tpm = player_info["tpm"]
            tpa = player_info["tpa"]
            tpp = player_info["tpp"]
            off_reb = player_info["offReb"]
            def_reb = player_info["defReb"]
            tot_reb = player_info["totReb"]
            assists = player_info["assists"]
            p_fouls = player_info["pFouls"]
            steals = player_info["steals"]
            turnovers = player_info["turnovers"]
            blocks = player_info["blocks"]
            plus_minus = player_info["plusMinus"]
            comment = player_info["comment"]

            #add record of data for the player into the database
            create_stat = PlayerStatistics(
                player_id = player_id,
                points = points,
                min = min,
                fgm = fgm,
                fga = fga,
                fgp = fgp,
                ftm = ftm,
                fta = fta,
                ftp = ftp,
                tpm = tpm,
                tpa = tpa,
                tpp = tpp,
                off_reb = off_reb,
                def_reb = def_reb,
                tot_reb = tot_reb,
                assists = assists,
                p_fouls = p_fouls,
                steals = steals,
                turnovers = turnovers,
                blocks = blocks,
                plus_minus = plus_minus,
                comment = comment
            )

            db.session.add(create_stat)
            db.session.commit()

            print("Stat for player was created!")
        
    def get_players(self, arr):
        for team_id in arr:
            self.__collect_players(team_id)
            print('DONE COLLECTING ALL PLAYERS AND STATS')