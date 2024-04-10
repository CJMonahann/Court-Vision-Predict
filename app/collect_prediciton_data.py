import requests, time, json, os
from dotenv import load_dotenv
from datetime import date

class CollectPredicitionData:
    #load environment variable for API key
    load_dotenv('.env')

    #API KEY
    __API_KEY = os.getenv("__API_KEY")

    #implements min-max normalization technique to normalize an array of data
    def __normalize_data(data):
        normalized_data = []
        sample_min = min(data)
        sample_max = max(data)

        for feature in data:
            norm_feature = (feature - sample_min) / (sample_max - sample_min)
            formated_num = format(norm_feature, '.2f')
            normalized_data.append(float(formated_num))

        return normalized_data

    def __get_current_schedule(start_date, end_date, season):
        #constant variables
        MAX_CALLS = 401 #allowed called to be made to the API per minute (we have a restriction)

        scheduled_games = {}

        url = "https://api-nba-v1.p.rapidapi.com/games"

        querystring = {"season":season}

        headers = {
            "X-RapidAPI-Key": CollectPredicitionData.__API_KEY,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()

        new_date = date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:]))
        yeet_date = date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:]))

        if "response" in response:
            response = response["response"]

            num_game = 1
            num_api_calls = 1

            for game in response:
                orig_date = game["date"]["start"][0:10]
                curr_date = date(int(orig_date[0:4]), int(orig_date[5:7]), int(orig_date[8:]))

                delta_start = new_date - curr_date #if these dates are the same, found start
                delta_end = yeet_date - curr_date
                
                if delta_start.days <= 0 and delta_end.days >= 0:
                    home_team_id = game["teams"]["home"]["id"]
                    home_name =  game["teams"]["home"]["name"]
                    home_nickname =  game["teams"]["home"]["nickname"]

                    visitor_team_id = game["teams"]["visitors"]["id"]
                    visitor_name =  game["teams"]["visitors"]["name"]
                    visitor_nickname =  game["teams"]["visitors"]["nickname"]
                
                    if (home_team_id != None and visitor_team_id != None) and (home_name != None and visitor_name != None) and (home_nickname != None and visitor_nickname != None):
                        #if the teams can be represented in JSON format, collect their stats, and add it to the JSON object
                        match_stats = [] #represents a hypothetical match between two teams based off their team stats

                        if num_api_calls < MAX_CALLS:
                            home_stats = CollectPredicitionData.__get_team_stats(home_team_id, season)
                            visitor_stats = CollectPredicitionData.__get_team_stats(visitor_team_id, season)
                            match_stats.extend(home_stats)
                            match_stats.extend(visitor_stats)
                        else:
                            time.sleep(70)
                            home_stats = CollectPredicitionData.__get_team_stats(home_team_id, season)
                            visitor_stats = CollectPredicitionData.__get_team_stats(visitor_team_id, season)
                            match_stats.extend(home_stats)
                            match_stats.extend(visitor_stats)
                            num_api_calls = 0

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
                    
    def __get_team_stats(id, season):
        team_stats = []

        url = "https://api-nba-v1.p.rapidapi.com/teams/statistics"

        querystring = {"id":id,"season":season}

        headers = {
            "X-RapidAPI-Key": CollectPredicitionData.__API_KEY,
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
            normalize_stats = CollectPredicitionData.__normalize_data(team_stats)

            return normalize_stats


    def collect_prediction_data(start_date='2024-04-09', end_date='2024-04-14', season='2023'):
        testing_data = CollectPredicitionData.__get_current_schedule(start_date, end_date, season)
        #write all data to JSON file to be accessed for model training
        out_file = open("./app/model data/games_prediction_data.json", "w")
        json.dump(testing_data, out_file)
        out_file.close()