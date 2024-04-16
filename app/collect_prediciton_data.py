import requests, time, json, os
from dotenv import load_dotenv
from datetime import date, datetime

class CollectPredicitionData:
    #load the application's environment file for API key
    load_dotenv('.env')

    def __init__(self):
        self.__API_KEY = os.getenv("__API_KEY")
        self.__PREDICTION_PATH = "./app/model data/games_prediction_data.json"

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


    #implements min-max normalization technique to normalize an array of data
    def __normalize_data(self, data):
        normalized_data = []
        sample_min = min(data)
        sample_max = max(data)

        for feature in data:
            norm_feature = (feature - sample_min) / (sample_max - sample_min)
            formated_num = format(norm_feature, '.2f')
            normalized_data.append(float(formated_num))

        return normalized_data

    def __get_current_schedule(self, start_date, end_date, season):
        #constant variables
        MAX_CALLS = 401 #allowed called to be made to the API per minute (we have a restriction)

        scheduled_games = {}

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

            num_game = 1 #used to increment a key within a later dictionary that holds individual game records as values
            num_api_calls = 1 #used to check the amount of API calls made per iteration

            for game in response:
                orig_date = game["date"]["start"][0:10]
                #split string from game's date into YYYY-MM-DD format
                game_date = self.__create_date_object(orig_date)

                found_start = start_date - game_date #per iteration, check the game's date against current date. If 0, we found start
                found_end = end_date - game_date #check the games
                within_start = found_start.days <= 0
                within_end = found_end.days >= 0
                
                if within_start and within_end: # if the game's date falls within the user's inputted date range, collect game data
                    home_team_id = game["teams"]["home"]["id"]
                    home_name =  game["teams"]["home"]["name"]
                    home_nickname =  game["teams"]["home"]["nickname"]

                    visitor_team_id = game["teams"]["visitors"]["id"]
                    visitor_name =  game["teams"]["visitors"]["name"]
                    visitor_nickname =  game["teams"]["visitors"]["nickname"]
                
                    if (home_team_id != None and visitor_team_id != None) \
                        and (home_name != None and visitor_name != None) and \
                            (home_nickname != None and visitor_nickname != None):
                        #if the teams can be represented in JSON format, collect their stats, and add it to the JSON object

                        if num_api_calls < MAX_CALLS:
                            #represents a hypothetical match between two teams based off their team stats
                            match_stats = self.__simulate_match(home_team_id, visitor_team_id, season)
                        else:
                            time.sleep(70) #stall the program until the API can be used again
                            match_stats = self.__simulate_match(home_team_id, visitor_team_id, season)
                            num_api_calls = 0 #reset the number of allowed API calls

                        #create the JSON object that represents a hypothetical game
                        scheduled_games[f'game{num_game}'] = {
                            "date": orig_date,
                            "home": {
                                "id": home_team_id,
                                "name": home_name,
                                "nickname": home_nickname
                            },
                            "visitors": {
                                "id": visitor_team_id,
                                "name": visitor_name,
                                "nickname": visitor_nickname
                            },
                            "match_simulation": match_stats
                        }

                        num_game += 1
                        num_api_calls += 1

            return scheduled_games
    
    #create a date object from a string date in the format: YYYY-MM-DD
    def __create_date_object(self, str_date):
        yyyy = int(str_date[0:4])
        mm = int(str_date[5:7])
        dd = int(str_date[8:])
        date_obj = date(yyyy, mm, dd)
        return date_obj
                    
    def __get_team_stats(self, id, season):
        team_stats = []

        url = "https://api-nba-v1.p.rapidapi.com/teams/statistics"

        querystring = {"id":id,"season":season}

        headers = {
            "X-RapidAPI-Key": self.__API_KEY,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()

        if "response" in response:
            response = response["response"][0]

            #collect the team's statistics
            del response["games"]
            curr_statistics = list(response.values())
            for num in curr_statistics:
                if num is not None:
                    team_stats.append(float(num))
                else:
                    team_stats.append(0) #still need data for the team, so 0 will represent unknown/null for AI model
            
            #normalize data
            normalize_stats = self.__normalize_data(team_stats)

            return normalize_stats
    
    #simulates a match between two teams and returns a list with the features from the result of the 'match'
    def __simulate_match(self, home_id, visitors_id, season):
        match_stats = []
        #get stats from the individual teams - based off team statistics
        home_stats = self.__get_team_stats(home_id, season)
        visitor_stats = self.__get_team_stats(visitors_id, season)
        match_stats.extend(home_stats)
        match_stats.extend(visitor_stats)
        #returm the list with the simulated match features
        return match_stats

    def collect_prediction_data(self, start_date='2024-04-09', end_date='2024-04-14', season='2023'):
        start_date, end_date = self.__input_validation(start_date, end_date)
        testing_data = self.__get_current_schedule(start_date, end_date, season)
        #write all data to JSON file to be accessed for model training
        out_file = open(self.__PREDICTION_PATH, "w")
        json.dump(testing_data, out_file)
        out_file.close()