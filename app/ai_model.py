import json
from sklearn.tree import DecisionTreeClassifier	

class AppDecisionTree:
    def __init__(self):
        #create class-fields that store the data in JSON format (dictionary)
        self.__TRAINING_PATH = "./app/model data/games_training_data.json"
        self.__PREDICTION_PATH = "./app/model data/games_prediction_data.json"
        self.__GAME_HISTORY_PATH = "./app/model data/game_results.json"

    def __get_unique_dates(self, dict):
        unique_dates = {}

        for nested_dict in dict.values():
            curr_date = nested_dict["date"]
            if curr_date not in unique_dates:
                unique_dates[curr_date] = []
        
        return unique_dates

    def __create_results(self, predicitons, games, dict):
        i = 0
        for num in predicitons: #these are the classifications for each predicted game
            match = games[i] #the information about a game to be predicted
            match_date = match[0]
            home_team = match[1]
            visitor_team = match[2]

            #if the prediciton is 1, home team is predicted to win, else visitors
            if num == 1:
                result = home_team
            else:
                result = visitor_team

            #populate parameter-dictionary with the unique dates so that game predicitons can be displayed by dates played
            temp_dict = { #represents a specific game that was predicted
                "home": home_team,
                "visitors": visitor_team,
                "prediction": result
            }

            dict[match_date].append(temp_dict) #add this sub-dict to the array already within the dicitonary. Each list holds game predicitons for the same day
            i += 1

        return dict
    
    def __calculate_stats(self, games_dict, eval_dict):
        #create a dictionary to be used as a confusion matrix and additional variables
        confusion_matrix = {'true_win':0, 'wl_error':0, 'lw_error':0, 'true_loss':0}
        total_games = 0
        recorded_games = list(games_dict.values())
        all_games = []
        predicitons = list(eval_dict.values())
        all_predicitons = []
        len_records = len(recorded_games)
        len_predicitons = len(predicitons)

        #if we have the same number of game-days recorded for the predicitons and records, continue
        if len_records == len_predicitons:
            for i in range(len_records):
                all_games.extend(recorded_games[i]) #extend the list at this index into a list containing all game records in JSON format
                all_predicitons.extend(predicitons[i])
            num_comparisons = len(all_games)

            #now, iterate through the arr of dicitonaries and compare recorded game history to predicitons
            #populate matrix by comparing model predicitons to their known-true classes
            for i in range(num_comparisons):
                game_dict = all_games[i] #returns dictionary with game history
                pred_dict = all_predicitons[i] #returns the predicitons made for the same game
               
                true_winner = game_dict["winners"]
                
                if true_winner: #if there is a record for this game up to this point in time, include it in the stats calculation
                    #collect rest of the values from both dicitonaries necessary to constuct confusion matrix
                    pred_winner = pred_dict["prediction"]
                    home_team = game_dict["home"]
                    visitor_team = game_dict["visitors"]

                    if(pred_winner == home_team and true_winner == home_team): #true home team won prediciton
                        confusion_matrix['true_win'] += 1
                    elif(pred_winner == visitor_team and true_winner == home_team): #win to loss error
                        confusion_matrix['wl_error'] += 1
                    elif(pred_winner == home_team and true_winner == visitor_team): #loss to win error
                        confusion_matrix['lw_error'] += 1
                    elif(pred_winner == visitor_team and true_winner == visitor_team): #true home team lost prediciton
                        confusion_matrix['true_loss'] += 1
                    total_games += 1
        
            #calculate accuracy
            numerator = confusion_matrix['true_win'] + confusion_matrix['true_loss']
            denominator = total_games
            acc = (numerator / denominator) * 100
            acc = format(acc, '.2f')

            #calculate precision
            prec_home_win = confusion_matrix['true_win'] / (confusion_matrix['true_win'] + confusion_matrix['lw_error'])
            prec_home_loss = confusion_matrix['true_loss'] / (confusion_matrix['true_loss'] + confusion_matrix['wl_error'])
            prec = ((prec_home_win + prec_home_loss) / 2 ) * 100
            prec = format(prec, '.2f')

            #calculate recall
            rec_home_win = confusion_matrix['true_win'] / (confusion_matrix['true_win'] + confusion_matrix['wl_error'])
            rec_home_loss = confusion_matrix['true_loss'] / (confusion_matrix['true_loss'] + confusion_matrix['lw_error'])
            rec = ((rec_home_win + rec_home_loss) / 2) * 100
            rec = format(rec, '.2f')

            final_metrics = {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "games": total_games
            }

            return final_metrics
        
        else:
            return "The number of predicitons submitted is not the same as the number of games recorded for the season"

    def predict_games(self):
        #variables
        training_data = []
        training_classifiers = []
        testing_data = []
        game_info = [] #used to hold the string-game information data used when creating final results

        #load-in JSON files
        with open(self.__TRAINING_PATH, "r") as in_file1:
            feature_data = json.load(in_file1)

        with open(self.__PREDICTION_PATH, "r") as in_file2:
            predicitons = json.load(in_file2)

        #split training data into feature and classifier arrays to be inputted to model
        for game in feature_data.values(): #the JSON formatted data (dictionary)
            curr_game = []
            home_stats = game["home_team"]
            visiting_stats = game["visiting_team"]
            res_home_win = game["home_win"]
            curr_game.extend(home_stats)
            curr_game.extend(visiting_stats)
            training_data.append(curr_game)
            training_classifiers.append(res_home_win)

        #collect unique dates in the prediciton data to better display final results
        dates_array = self.__get_unique_dates(predicitons)
        
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

        predicted_games = self.__create_results(dt_prediction, game_info, dates_array)

        return predicted_games
    
    def calc_metrics(self, eval_dict):
        #open json file with the game history
        with open(self.__GAME_HISTORY_PATH, "r") as in_file1:
                games_dict = json.load(in_file1)
        #compare inputted parameter dict to that of the known game history
        metrics_dict = self.__calculate_stats(games_dict, eval_dict)
        #return metrics_dict
        return metrics_dict