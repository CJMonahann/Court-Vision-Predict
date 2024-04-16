import requests, time, json, os
from dotenv import load_dotenv
from datetime import date, datetime

class GameResults:
    #load the application's environment file for API key
    load_dotenv('.env')

    def __init__(self):
        self.__API_KEY = os.getenv("__API_KEY")
        self.__GAME_HISTORY_PATH = "./app/model data/game_results.json"

    #inputs user string date to check if correctly inputted
    def __input_validation(self, start_date, end_date):
        #error messages
        str_error = 'ERROR: please provide the desired date(s) as str data type(s)'
        time_error = 'ERROR: the provided starting date was larger than the ending date'
        #check if the input is a string
        is_str_start = isinstance(start_date, str)
        is_str_end = isinstance(end_date, str)

        if not(is_str_start and is_str_end):
            print(str_error)
            new_str_start = input('Please provide START date in YYYY-MM-DD format: ')
            new_str_end = input('Please provide END date in YYYY-MM-DD format: ')
        else:
            new_str_start = start_date
            new_str_end = end_date

            #check to see if we can convert date to YYYY-MM-DD format
            valid_start = False
            valid_end = False
            valid_dates = False
            format = "%Y-%m-%d"
            
            while not(valid_dates):
                try:
                    valid_start = bool(datetime.strptime(new_str_start, format))
                    valid_end = bool(datetime.strptime(new_str_end, format))
                    #means we can get dates, now check to make sure they're in chronological order
                    chron_start = time.strptime(new_str_start, format)
                    chron_end = time.strptime(new_str_end, format)
                    if chron_start > chron_end:
                        #unset booleans from being true and print error message for the next iteration
                        valid_start = False
                        valid_end = False
                        print(time_error)
                        new_str_start = input('ERROR: please provide START date in YYYY-MM-DD format: ')
                        new_str_end = input('ERROR: please provide END date in YYYY-MM-DD format: ')

                except ValueError:
                    new_str_start = input('ERROR: please provide START date in YYYY-MM-DD format: ')
                    new_str_end = input('ERROR: please provide END date in YYYY-MM-DD format: ')

                if valid_start and valid_end:
                    valid_dates = True
            
            return new_str_start, new_str_end

    def __get_games_history(self, start_date, end_date, season):
        game_results = {}

        url = "https://api-nba-v1.p.rapidapi.com/games"

        querystring = {"season":season}

        headers = {
            "X-RapidAPI-Key": self.__API_KEY,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()

        #reformat start and end date arguments into 'date' objects in YYYY-MMM-DD format
        start_date = self.__create_date_object(start_date)
        end_date = self.__create_date_object(end_date)

        if "response" in response: #if the API returns a call with the data, collect the data
            response = response["response"]

            for game in response:
                orig_date = game["date"]["start"][0:10]
                #split string from game's date into YYYY-MM-DD format
                game_date = self.__create_date_object(orig_date)

                found_start = start_date - game_date #per iteration, check the game's date against current date. If 0, we found start
                found_end = end_date - game_date #check the games
                within_start = found_start.days <= 0
                within_end = found_end.days >= 0
                
                if within_start and within_end: # if the game's date falls within the user's inputted date range, collect game data
                    if orig_date not in game_results: #only create new key value if not already in dicitionary
                         game_results[orig_date] = [] #create dicitonary entry with the found date, and a list to add all games that fall under that date

                    home_nickname =  game["teams"]["home"]["nickname"]
                    visitor_nickname =  game["teams"]["visitors"]["nickname"]

                    if game["scores"]["home"]["points"] is not None:
                            home_team_score = game["scores"]["home"]["points"]
                    else:
                            home_team_score = None
                            
                    if game["scores"]["visitors"]["points"] is not None:
                            visitor_team_score = game["scores"]["visitors"]["points"]
                    else:
                            visitor_team_score = None
                    
                    if home_team_score != None and visitor_team_score != None:
                            result = home_nickname if home_team_score > visitor_team_score else visitor_nickname 
                    else:
                        result = None #will indicate that the match history couldn't be recorded
                
                    if (home_nickname != None and visitor_nickname != None and result != None): #add complete log to JSON File
                        #if the teams can be represented in JSON format, dd it to the JSON object

                        temp_dict = { #represents a specific game that was predicted
                            "home": home_nickname,
                            "visitors": visitor_nickname,
                            "winners": result
                        }

                        game_results[orig_date].append(temp_dict)

                    elif (home_nickname != None and visitor_nickname != None): 
                        temp_dict = { #represents a specific game that was predicted
                            "home": home_nickname,
                            "visitors": visitor_nickname,
                            "winners": result #indicates game hasn't finished or hasn't been played yet - equates to none
                        }

            return game_results
    
    #create a date object from a string date in the format: YYYY-MM-DD
    def __create_date_object(self, str_date):
        yyyy = int(str_date[0:4])
        mm = int(str_date[5:7])
        dd = int(str_date[8:])
        date_obj = date(yyyy, mm, dd)
        return date_obj
    
    def get_results(self, start_date='2024-04-09', end_date='2024-04-14', season='2023'):
        start_date, end_date = self.__input_validation(start_date, end_date)
        testing_data = self.__get_games_history(start_date, end_date, season)
        #write all data to JSON file to be accessed for model training
        out_file = open(self.__GAME_HISTORY_PATH, "w")
        json.dump(testing_data, out_file)
        out_file.close()

gr = GameResults()
gr.get_results()