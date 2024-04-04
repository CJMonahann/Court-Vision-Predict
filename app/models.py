from app import db
from sqlalchemy import ForeignKey

# This defines the DB schema
class Accounts(db.Model):
    __tablename__ = 'Accounts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False)
    last_name = db.Column(db.String(30), unique=False)
    profile_picture_url = db.Column(db.String(100), unique=False)
    user_name = db.Column(db.String(30), unique=False)
    password = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(30), unique=False)
    city = db.Column(db.String(30), unique=False)
    state = db.Column(db.String(30), unique=False)
    favorite_team = db.Column(db.Integer, ForeignKey("NbaTeams.api_id", ondelete="CASCADE"))
    fav_player1 = db.Column(db.Integer, ForeignKey("Players.api_id", ondelete="CASCADE"))
    fav_player2 = db.Column(db.Integer, ForeignKey("Players.api_id", ondelete="CASCADE"))
    fav_player3 = db.Column(db.Integer, ForeignKey("Players.api_id", ondelete="CASCADE"))
    fav_player4 = db.Column(db.Integer, ForeignKey("Players.api_id", ondelete="CASCADE"))
    fav_player5 = db.Column(db.Integer, ForeignKey("Players.api_id", ondelete="CASCADE"))
    is_mod = db.Column(db.Boolean, unique=False, default=False)

class Moderators(db.Model): 
    __tablename__ = 'Moderators'
    id = db.Column(db.Integer, primary_key=True)
    mod_id = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    assignedTeam = db.Column(db.Integer, ForeignKey("NbaTeams.api_id", ondelete="CASCADE"))

class SuspendedAccounts(db.Model): 
    __tablename__ = 'SuspendedAccounts'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    mod_id = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    date_suspended = db.Column(db.String(30), unique=False)
    time_suspended = db.Column(db.String(30), unique=False)
    date_permitted_return = db.Column(db.String(30), unique=False)
    suspension_reason = db.Column(db.String(100), unique=False)

class RemovedAccounts(db.Model): 
    __tablename__ = 'RemovedAccounts'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    mod_id = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    date_removed = db.Column(db.String(30), unique=False)
    time_removed = db.Column(db.String(30), unique=False)
    removal_reason = db.Column(db.String(100), unique=False)


class HelpPortalMessages(db.Model): 
    __tablename__ = 'HelpPortalMessages'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    message = db.Column(db.String(300), unique=False)

class RemovedHelpRequest(db.Model): 
    __tablename__ = 'RemovedHelpRequest'
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, ForeignKey("HelpPortalMessages.id", ondelete="CASCADE"))
    mod_id = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    message_date = db.Column(db.String(30), unique=False)
    message_time = db.Column(db.String(30), unique=False)
    original_message = db.Column(db.String(300), unique=False)
    date_resolved = db.Column(db.String(30), unique=False)
    time_resolved = db.Column(db.String(30), unique=False)
    mod_message = db.Column(db.String(300), unique=False)

class NbaNews(db.Model): 
    __tablename__ = 'NbaNews'
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(300), unique=False)
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    information = db.Column(db.String(500), unique=False)
    link = db.Column(db.String(300), unique=False)

class NbaTeams(db.Model): 
    __tablename__ = 'NbaTeams'
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=False) #the teams ID number from the API
    name = db.Column(db.String(30), unique=False)
    nickname = db.Column(db.String(30), unique=False)
    code = db.Column(db.Integer, unique=True)
    city = db.Column(db.String(30), unique=False)
    logo = db.Column(db.String(30), unique=False)
    all_star = db.Column(db.String(30), unique=False)
    nba_franchise = db.Column(db.String(30), unique=False)
    division = db.Column(db.String(30), unique=False)

class Players(db.Model): 
    __tablename__ = 'Players'
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=False) #the player's ID number from the API
    team_id = db.Column(db.Integer, ForeignKey("NbaTeams.api_id", ondelete="CASCADE"))
    first_name = db.Column(db.String(30), unique=False)
    last_name = db.Column(db.String(30), unique=False)
    date_of_birth = db.Column(db.String(30), unique=False)
    country = db.Column(db.String(30), unique=False)
    starting_year = db.Column(db.String(30), unique=False)
    pro = db.Column(db.String(30), unique=False)
    height = db.Column(db.Float, unique=False)
    weight = db.Column(db.Float, unique=False)
    college = db.Column(db.String(30), unique=False)
    affiliation = db.Column(db.String(30), unique=False)
    num_jersey = db.Column(db.Integer, unique=False)
    position = db.Column(db.String(30), unique=False)
    active = db.Column(db.String(30), unique=False)

class PlayerStatistics(db.Model):
    __tablename__ = 'PlayerStatistics'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, ForeignKey("Players.api_id", ondelete="CASCADE"))
    points = db.Column(db.Integer, unique=False)
    min = db.Column(db.String(8), unique=False)
    fgm = db.Column(db.Float, unique=False)
    fga = db.Column(db.Float, unique=False)
    fgp = db.Column(db.Float, unique=False)
    ftm = db.Column(db.Float, unique=False)
    fta = db.Column(db.Float, unique=False)
    ftp = db.Column(db.Float, unique=False)
    tpm = db.Column(db.Float, unique=False)
    tpa = db.Column(db.Float, unique=False)
    tpp = db.Column(db.Float, unique=False)
    off_reb = db.Column(db.Float, unique=False)
    def_reb = db.Column(db.Float, unique=False)
    tot_reb = db.Column(db.Float, unique=False)
    assists = db.Column(db.Float, unique=False)
    p_fouls = db.Column(db.Float, unique=False)
    steals = db.Column(db.Float, unique=False)
    turnovers = db.Column(db.Float, unique=False)
    blocks = db.Column(db.Float, unique=False)
    plus_minus = db.Column(db.Float, unique=False)
    comment = db.Column(db.String(30), unique=False)

class TeamForumPosts(db.Model): 
    __tablename__ = 'TeamForumPosts'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, ForeignKey("NbaTeams.api_id", ondelete="CASCADE"))
    account_id = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    message = db.Column(db.String(300), unique=False)

class RemovedTeamForumPosts(db.Model): 
    __tablename__ = 'RemovedTeamForumPosts'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, ForeignKey("TeamForumPosts.id", ondelete="CASCADE"))
    mod_id = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    post_date = db.Column(db.String(30), unique=False)
    post_time = db.Column(db.String(30), unique=False)
    post_message = db.Column(db.String(300), unique=False)
    date_removed = db.Column(db.String(30), unique=False)
    time_removed = db.Column(db.String(30), unique=False)
    reason_removed = db.Column(db.String(100), unique=False)


class ScheduledGames(db.Model): 
    __tablename__ = 'ScheduledGames'
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.Integer, ForeignKey("NbaTeams.api_id", ondelete="CASCADE"))
    team2 = db.Column(db.Integer, ForeignKey("NbaTeams.api_id", ondelete="CASCADE"))
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    location = db.Column(db.String(30), unique=False)
    game_outcome = db.Column(db.String(30), unique=False)

class AccountVsModelPredicitons(db.Model): 
    __tablename__ = 'AccountVsModelPredicitons'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    game_id = db.Column(db.Integer, ForeignKey("ScheduledGames.id", ondelete="CASCADE"))
    model_game_prediciton = db.Column(db.String(30), unique=False)
    account_game_prediciton = db.Column(db.String(30), unique=False)
    game_outcome = db.Column(db.String(30), unique=False)