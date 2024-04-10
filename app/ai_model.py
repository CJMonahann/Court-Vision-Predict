import json
from sklearn.tree import DecisionTreeClassifier	

class DecisionTree:
    def __get_unique_dates(dict):
        unique_dates = {}

        for nested_dict in dict.values():
            curr_date = nested_dict["date"]
            if curr_date not in unique_dates:
                unique_dates[curr_date] = []
        
        return unique_dates

    def __create_results(predicitons, games, dict):
        i = 0

        for num in predicitons: #these are the classifications for each predicted game
            temp_predict = []
            match = games[i] #the information about a game to be predicted
            match_date = match[0]
            home_team = match[1]
            visitor_team = match[2]

            #if the prediciton is 1, home team is predicted to win, else visitors
            if num == 1:
                result = home_team
            else:
                result = visitor_team

            temp_predict.append(home_team)
            temp_predict.append(visitor_team)
            temp_predict.append(result)

            #populate dictionary with the unique dates so that game predicitons can be displayed by dates played
            dict[match_date].append(temp_predict) #add this list to the array already within the dicitonary. Each list holds game predicitons for the same day
            i += 1

        return dict

    def predict_games():
        #variables
        training_data = []
        training_classifiers = []
        testing_data = []
        game_info = []

        #load-in JSON files
        with open("./app/model data/games_training_data.json", "r") as in_file1:
            data = json.load(in_file1)

        with open("./app/model data/games_prediction_data.json", "r") as in_file2:
            predicitons = json.load(in_file2)

        
        #split training data into feature and classifier arrays to be inputted to model
        for game in data.values():
            curr_game = []
            home_stats = game["home_team"]
            visiting_stats = game["visiting_team"]
            res_home_win = game["home_win"]
            curr_game.extend(home_stats)
            curr_game.extend(visiting_stats)
            training_data.append(curr_game)
            training_classifiers.append(res_home_win)

        #collect unique dates in the prediciton data to better display final results
        dates_array = DecisionTree.__get_unique_dates(predicitons)
        

        #split prediciton data into features
        for simulation in predicitons.values():
            temp_arr = []
            game_date = simulation["date"]
            home_name = simulation["home"]["nickname"]
            visitors_name = simulation["visitors"]["nickname"]
            #put match info into 'game info' array to be indexed later when displaying results
            temp_arr.append(game_date)
            temp_arr.append(home_name)
            temp_arr.append(visitors_name)
            game_info.append(temp_arr)

            #put game simulation feature data into the testing array to be inputted to the model
            testing_data.append(simulation["match_simulation"])
        
        #train and test Decision Tree Model
        dt_model = DecisionTreeClassifier()
        dt_model.fit(training_data, training_classifiers)
        dt_prediction = dt_model.predict(testing_data)

        predicted_games = DecisionTree.__create_results(dt_prediction, game_info, dates_array)

        return predicted_games
