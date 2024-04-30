from app import db
from app.models import Accounts

class MakeAccounts:
    def __init__(self):
        self.num_calls = 0

    def populate_accounts(self):
        example_data = {
            "person1": {
                "first_name": "Bob",  
                "last_name": "Stephens",
                "profile_picture_url": None,
                "user_name": "Stephs2002",
                "password": "password123",
                "email": "bSteph@gmail.com",
                "city": "NYC",
                "state": "NY",
                "favorite_team": 1,
                "fav_player1": 3,
                "fav_player2": 4, 
                "fav_player3": 5, 
                "fav_player4": 6,
                "fav_player5": 7,
                "is_mod": False
            },
                "person2": {
                "first_name": "Mary",  
                "last_name": "Bridge",
                "profile_picture_url": None,
                "user_name": "marmar5638",
                "password": "fish8790",
                "email": "mBridge@gmail.com",
                "city": "Miami",
                "state": "FL",
                "favorite_team": 12,
                "fav_player1": 15,
                "fav_player2": 7, 
                "fav_player3": 8, 
                "fav_player4": 2,
                "fav_player5": 13,
                "is_mod": False
            }
        }

        for person in example_data.values():
            #get information to create Accout object
                f_name = person["first_name"]  
                l_name = person["last_name"]
                pic = person["profile_picture_url"]
                usr_name = person["user_name"]
                psswrd = person["password"]
                email = person["email"]
                city = person["city"]
                st = person["state"]
                fav_team = person["favorite_team"]
                player_1 = person["fav_player1"]
                player_2 = person["fav_player2"] 
                player_3 = person["fav_player3"] 
                player_4 = person["fav_player4"]
                player_5 = person["fav_player5"]
                is_mod = person["is_mod"]

                create_person = Accounts(first_name = f_name,
                                        last_name = l_name,
                                        profile_picture_url = pic,
                                        user_name = usr_name,
                                        password = psswrd,
                                        email = email,
                                        city = city,
                                        state = st,
                                        favorite_team = fav_team,
                                        fav_player1 = player_1,
                                        fav_player2 = player_2,
                                        fav_player3 = player_3,
                                        fav_player4 = player_4,
                                        fav_player5 = player_5,
                                        is_mod = is_mod)
                
                db.session.add(create_person)
                db.session.commit()

                self.num_calls += 1