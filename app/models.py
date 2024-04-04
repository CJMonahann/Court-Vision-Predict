from app import db
from sqlalchemy import ForeignKey

# This defines the DB schema
class Accounts(db.Model):
    __tablename__ = 'Accounts'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), unique=False)
    lastName = db.Column(db.String(30), unique=False)
    profilePictureUrl = db.Column(db.String(100), unique=False)
    userName = db.Column(db.String(30), unique=False)
    password = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(30), unique=False)
    city = db.Column(db.String(30), unique=False)
    state = db.Column(db.String(30), unique=False)
    favoriteTeam = db.Column(db.Integer, ForeignKey("NbaTeams.id", ondelete="CASCADE"))
    favPlayer1 = db.Column(db.Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    favPlayer2 = db.Column(db.Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    favPlayer3 = db.Column(db.Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    favPlayer4 = db.Column(db.Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    favPlayer5 = db.Column(db.Integer, ForeignKey("Players.id", ondelete="CASCADE"))
    isMod = db.Column(db.Boolean, unique=False, default=False)

class Moderators(db.Model): 
    __tablename__ = 'Moderators'
    id = db.Column(db.Integer, primary_key=True)
    modID = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    assignedTeam = db.Column(db.Integer, ForeignKey("NbaTeams.id", ondelete="CASCADE"))

class SuspendedAccounts(db.Model): 
    __tablename__ = 'SuspendedAccounts'
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    modId = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    dateSuspended = db.Column(db.String(30), unique=False)
    timeSuspended = db.Column(db.String(30), unique=False)
    datePermittedReturn = db.Column(db.String(30), unique=False)
    suspensionReason = db.Column(db.String(100), unique=False)

class RemovedAccounts(db.Model): 
    __tablename__ = 'RemovedAccounts'
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    modId = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    dateRemoved = db.Column(db.String(30), unique=False)
    timeRemoved = db.Column(db.String(30), unique=False)
    removalReason = db.Column(db.String(100), unique=False)


class HelpPortalMessages(db.Model): 
    __tablename__ = 'HelpPortalMessages'
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    message = db.Column(db.String(300), unique=False)

class RemovedHelpRequest(db.Model): 
    __tablename__ = 'RemovedHelpRequest'
    id = db.Column(db.Integer, primary_key=True)
    messageId = db.Column(db.Integer, ForeignKey("HelpPortalMessages.id", ondelete="CASCADE"))
    modId = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    messageDate = db.Column(db.String(30), unique=False)
    messageTime = db.Column(db.String(30), unique=False)
    originalMessage = db.Column(db.String(300), unique=False)
    dateResolved = db.Column(db.String(30), unique=False)
    timeResolved = db.Column(db.String(30), unique=False)
    modMessage = db.Column(db.String(300), unique=False)

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
    apiId = db.Column(db.Integer, unique=False) #the teams ID number from the API
    name = db.Column(db.String(30), unique=False)
    nickname = db.Column(db.String(30), unique=False)
    code = db.Column(db.Integer, unique=True)
    city = db.Column(db.String(30), unique=False)
    logo = db.Column(db.String(30), unique=False)
    allStar = db.Column(db.String(30), unique=False)
    nbaFranchise = db.Column(db.String(30), unique=False)
    division = db.Column(db.String(30), unique=False)

class Players(db.Model): 
    __tablename__ = 'Players'
    id = db.Column(db.Integer, primary_key=True)
    apiId = db.Column(db.Integer, unique=False) #the player's ID number from the API
    teamId = db.Column(db.Integer, ForeignKey("NbaTeams.apiId", ondelete="CASCADE"))
    firstName = db.Column(db.String(30), unique=False)
    lastName = db.Column(db.String(30), unique=False)
    dateOfBirth = db.Column(db.String(30), unique=False)
    country = db.Column(db.String(30), unique=False)
    startingYear = db.Column(db.String(30), unique=False)
    pro = db.Column(db.String(30), unique=False)
    height = db.Column(db.Float, unique=False)
    weight = db.Column(db.Float, unique=False)
    college = db.Column(db.String(30), unique=False)
    affiliation = db.Column(db.String(30), unique=False)
    numJersey = db.Column(db.Integer, unique=False)
    position = db.Column(db.String(30), unique=False)
    active = db.Column(db.String(30), unique=False)

class PlayerStatistics(db.Model):
    __tablename__ = 'PlayerStatistics'
    id = db.Column(db.Integer, primary_key=True)
    playerId = db.Column(db.Integer, ForeignKey("Players.apiId", ondelete="CASCADE"))
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
    offReb = db.Column(db.Float, unique=False)
    defReb = db.Column(db.Float, unique=False)
    totReb = db.Column(db.Float, unique=False)
    assists = db.Column(db.Float, unique=False)
    pFouls = db.Column(db.Float, unique=False)
    steals = db.Column(db.Float, unique=False)
    turnovers = db.Column(db.Float, unique=False)
    blocks = db.Column(db.Float, unique=False)
    plusMinus = db.Column(db.Float, unique=False)
    comment = db.Column(db.String(30), unique=False)

class TeamForumPosts(db.Model): 
    __tablename__ = 'TeamForumPosts'
    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.Integer, ForeignKey("NbaTeams.apiId", ondelete="CASCADE"))
    accountId = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    message = db.Column(db.String(300), unique=False)

class RemovedTeamForumPosts(db.Model): 
    __tablename__ = 'RemovedTeamForumPosts'
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, ForeignKey("TeamForumPosts.id", ondelete="CASCADE"))
    modId = db.Column(db.Integer, ForeignKey("Moderators.id", ondelete="CASCADE"))
    postDate = db.Column(db.String(30), unique=False)
    postTime = db.Column(db.String(30), unique=False)
    postMessage = db.Column(db.String(300), unique=False)
    dateRemoved = db.Column(db.String(30), unique=False)
    timeRemoved = db.Column(db.String(30), unique=False)
    reasonRemoved = db.Column(db.String(100), unique=False)


class ScheduledGames(db.Model): 
    __tablename__ = 'ScheduledGames'
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.Integer, ForeignKey("NbaTeams.apiId", ondelete="CASCADE"))
    team2 = db.Column(db.Integer, ForeignKey("NbaTeams.apiId", ondelete="CASCADE"))
    date = db.Column(db.String(30), unique=False)
    time = db.Column(db.String(30), unique=False)
    location = db.Column(db.String(30), unique=False)
    gameOutcome = db.Column(db.String(30), unique=False)

class AccountVsModelPredicitons(db.Model): 
    __tablename__ = 'AccountVsModelPredicitons'
    id = db.Column(db.Integer, primary_key=True)
    accountID = db.Column(db.Integer, ForeignKey("Accounts.id", ondelete="CASCADE"))
    gameID = db.Column(db.Integer, ForeignKey("ScheduledGames.id", ondelete="CASCADE"))
    modelGamePrediciton = db.Column(db.String(30), unique=False)
    accountGamePrediciton = db.Column(db.String(30), unique=False)
    gameOutcome = db.Column(db.String(30), unique=False)