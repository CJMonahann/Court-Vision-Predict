import requests, time, json, os
from dotenv import load_dotenv
from datetime import date

class CollectTrainingData:
	#load environment variable for API key
	load_dotenv('.env')

	def __init__(self):
		self.__API_KEY = os.getenv("__API_KEY")
		self.__TRAINING_PATH = "./app/model data/games_training_data.json"

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

	def __load_in_games(self, season, MAX_SAMPLES):
		#constant variables
		MAX_CALLS = 401 #allowed called to be made to the API per minute (we have a restriction)

		season_games_data = {}

		#call to API-NBA to get all the games played in a particular season
		url = "https://api-nba-v1.p.rapidapi.com/games"

		querystring = {"season":str(season)}

		headers = {
			"X-RapidAPI-Key": self.__API_KEY,
			"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
		}

		response = requests.get(url, headers=headers, params=querystring)
		response = response.json()

		if "response" in response:
			response = response["response"]

			#iterate through games to extract statistics
			num_api_calls = 1

			for game in response[:MAX_SAMPLES]: #NEED TO TAKE THIS OUT TO GET FULL DATA

				game_id = game["id"]

				if game["date"]["end"] is not None:
					date = game["date"]["end"][0:10]
				else:
					date = None
				
				if game["scores"]["home"]["points"] is not None:
						home_team_score = game["scores"]["home"]["points"]
				else:
						home_team_score = None
						
				if game["scores"]["visitors"]["points"] is not None:
						visitor_team_score = game["scores"]["visitors"]["points"]
				else:
						visitor_team_score = None
				
				if home_team_score and visitor_team_score != None:
						res_home_win = 1 if home_team_score > visitor_team_score else 0 #1 if the home team won, else 0
				else:
					res_home_win = None #will indicate that the match history couldn't be recorded

				if num_api_calls < MAX_CALLS: #if we haven't reaches the max API calls per minute, collect game stats
					try:
						home_stats, visitor_stats = self.__get_game_stats(game_id)
					except TypeError:
						home_stats = None
						visitor_stats = None
				else: #put program to rest and wait for API allowance to refresh
					time.sleep(70)
					try:
						home_stats, visitor_stats = self.__get_game_stats(game_id)
					except TypeError:
						home_stats = None
						visitor_stats = None
					num_api_calls = 0
					
				#add data to the larger dictionary to be added to JSON file
				if (home_stats != None) and (visitor_stats != None) and (res_home_win != None): #if there is no None value recorded for any of the desired variables

					season_games_data[game_id] = {
						"home_team": home_stats,
						"visiting_team": visitor_stats,
						"home_win": res_home_win
					}

				num_api_calls += 1

			return season_games_data

	def __get_game_stats(self, game_id):
		final_visiting_stats = []
		final_home_stats = []

		url = "https://api-nba-v1.p.rapidapi.com/games/statistics"

		querystring = {"id":str(game_id)}

		headers = {
			"X-RapidAPI-Key": self.__API_KEY,
			"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
		}

		response = requests.get(url, headers=headers, params=querystring)
		response = response.json()

		if "response" in response: #if there is a game stat history
			response = response["response"]

			#collect visitor team stats
			visiting_team = response[0]['statistics'][0]
			del visiting_team['min']
			visiting_statistics = list(visiting_team.values())
			for num in visiting_statistics:
				if num is not None:
					final_visiting_stats.append(float(num)) #ADDED PART TO CONVERT ALL STRINGS TO DIGITS
				else:
					return
			
			#collect home team stats
			home_team = response[1]['statistics'][0]
			del home_team['min']
			home_statistics = list(home_team.values())
			for num in home_statistics:
				if num is not None:
					final_home_stats.append(float(num)) #ADDED PART TO CONVERT ALL STRINGS TO DIGITS
				else:
					return 
				
			#if we haven't returned, it means we have a full array of data, and can normalize it
			normalized_home = self.__normalize_data(final_home_stats)
			normalized_visitors = self.__normalize_data(final_visiting_stats)

			return normalized_home, normalized_visitors

	def collect_training_data(self, years=[2020,2021,2022], num_samples=40):
		total_data = {}

		#collect game data from the API for a specific season
		for year in years:
			games_data = self.__load_in_games(year, num_samples)
			total_data.update(games_data) #append games_data dict to total_data dict
		
		#write all data to JSON file to be accessed for model training
		out_file = open(self.__TRAINING_PATH, "w")
		json.dump(total_data, out_file)
		out_file.close()