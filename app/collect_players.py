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


    def __collect_player_stats(self, player_id, season="2023"):
        url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
        querystring = {"id": str(player_id), "season": season}
        headers = {
            "X-RapidAPI-Key": self.__API_KEY,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            player_statistics = response.json().get('response', [])

            if player_statistics:
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
                    total_points += int(stat.get('points', 0))
                    total_fgm += int(stat.get('fgm', 0))
                    total_fga += int(stat.get('fga', 0))
                    total_ftm += int(stat.get('ftm', 0))
                    total_fta += int(stat.get('fta', 0))
                    total_tpm += int(stat.get('tpm', 0))
                    total_tpa += int(stat.get('tpa', 0))
                    total_offReb += int(stat.get('offReb', 0))
                    total_defReb += int(stat.get('defReb', 0))
                    total_totReb += int(stat.get('totReb', 0))
                    total_assists += int(stat.get('assists', 0))
                    total_pFouls += int(stat.get('pFouls', 0))
                    total_steals += int(stat.get('steals', 0))
                    total_turnovers += int(stat.get('turnovers', 0))
                    total_blocks += int(stat.get('blocks', 0))
                    plus_minus = stat.get('plusMinus', '--')
                    if plus_minus.isdigit():  # Check if it's a valid integer
                        total_plusMinus += int(plus_minus)

                # Calculate averages
                num_games = len(player_statistics)
                avg_points = total_points / num_games if num_games > 0 else 0
                avg_fgm = total_fgm / num_games if num_games > 0 else 0
                avg_fga = total_fga / num_games if num_games > 0 else 0
                avg_ftm = total_ftm / num_games if num_games > 0 else 0
                avg_fta = total_fta / num_games if num_games > 0 else 0
                avg_tpm = total_tpm / num_games if num_games > 0 else 0
                avg_tpa = total_tpa / num_games if num_games > 0 else 0
                avg_offReb = total_offReb / num_games if num_games > 0 else 0
                avg_defReb = total_defReb / num_games if num_games > 0 else 0
                avg_totReb = total_totReb / num_games if num_games > 0 else 0
                avg_assists = total_assists / num_games if num_games > 0 else 0
                avg_pFouls = total_pFouls / num_games if num_games > 0 else 0
                avg_steals = total_steals / num_games if num_games > 0 else 0
                avg_turnovers = total_turnovers / num_games if num_games > 0 else 0
                avg_blocks = total_blocks / num_games if num_games > 0 else 0
                avg_plusMinus = total_plusMinus / num_games if num_games > 0 else 0

                # Add statistics to the database
                create_stat = PlayerStatistics(
                    player_id=player_id,
                    points=avg_points,
                    min=None,  # Assuming 'min' is not available in the response
                    fgm=avg_fgm,
                    fga=avg_fga,
                    fgp=None,  # Calculate field goal percentage if required
                    ftm=avg_ftm,
                    fta=avg_fta,
                    ftp=None,  # Calculate free throw percentage if required
                    tpm=avg_tpm,
                    tpa=avg_tpa,
                    tpp=None,  # Calculate three-point percentage if required
                    off_reb=avg_offReb,
                    def_reb=avg_defReb,
                    tot_reb=avg_totReb,
                    assists=avg_assists,
                    p_fouls=avg_pFouls,
                    steals=avg_steals,
                    turnovers=avg_turnovers,
                    blocks=avg_blocks,
                    plus_minus=avg_plusMinus,
                    comment=""  # Assuming 'comment' is not available in the response
                )

                db.session.add(create_stat)
                db.session.commit()

                print("Stat for player was created!")
     
    def get_players(self, arr):
        for team_id in arr:
            self.__collect_players(team_id)
            print('DONE COLLECTING ALL PLAYERS AND STATS')
