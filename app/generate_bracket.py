import pandas as pd
import math

# import data sets that will be used from kaggle
seeds = pd.read_csv("..\\csvs\\kaggle\\predictive\\NCAATourneySeeds.csv")
regions = pd.read_csv("..\\csvs\\kaggle\\predictive\\Seasons.csv")
team_names = pd.read_csv("..\\csvs\\kaggle\\predictive\\Teams.csv")
regular_season = pd.read_csv("..\\csvs\\kaggle\\regular_season_stats.csv", encoding = 'latin-1')


# our made data sets 
outcomes_14 = pd.read_csv("..\\csvs\\1314\\1314_outcomes.csv", encoding = 'latin-1')
outcomes_15 = pd.read_csv("..\\csvs\\1415\\1415_outcomes.csv", encoding = 'latin-1')
outcomes_16 = pd.read_csv("..\\csvs\\1516\\1516_outcomes.csv", encoding = 'latin-1')
outcomes_17 = pd.read_csv("..\\csvs\\1617\\1617_outcomes.csv", encoding = 'latin-1')
outcomes = [outcomes_14, outcomes_15, outcomes_16, outcomes_17]


pd.set_option('display.max_rows',1755)

# adjust data sets to only 2014 and later
seeds = seeds[seeds.Season > 2013]

names = []
for team in seeds.TeamID:
    names.append(team_names['TeamName'][team_names['TeamID'] == team].values[0])
seeds['TeamName'] = names

# returns team name based on teamID and season
def get_name(team, season):
    return seeds['TeamName'][(seeds['Seed'] == team)
           & (seeds['Season'] == season)].values[0]


# returns team ID based on seed number in tournament
def get_teamID(team, season):
    return seeds['TeamID'][(seeds['Seed'] == team)
           & (seeds['Season'] == season)].values[0]  


# returns specific stat based on the team, season, and stat column/indicator
def get_stat(team, season, indicator):
    return regular_season[(regular_season['TeamID'] == team)
           & (regular_season['Season'] == season)][indicator].values[0]


# makes a prediction on who will win given set of indicators and weights
def prediction(team1, team2, indicators, season, weights = 0):
    t1 = get_teamID(team1, season)
    t2 = get_teamID(team2, season)
    
    t1_stats, t2_stats, t1_weighted, t2_weighted = [], [], 0, 0 
    
    
    for i in indicators:
        t1_stats.append(get_stat(t1, season, i))
        t2_stats.append(get_stat(t2, season, i))
    
    # if there is no weights given, assigns each stat the same weight 
    if weights == 0:
        weights = []        
        for i in range(len(indicators)):
            weights.append(1 / len(indicators))
    
    # calculates weighted stat for each team 
    for i in range(len(weights)):
        t1_weighted += weights[i] * t1_stats[i]
        t2_weighted += weights[i] * t2_stats[i]
    
    if t1_weighted > t2_weighted:
        return team1, team2, 0
    else:
        return team2, team1, 1


# returns actual results of tournament from that season
def get_actual_results(season):
    actual_results = [[], [], [], [], [], []]
    
    season_outcome = outcomes[season - 2014]
    
    for round_num in range(0, 6):
        num_teams = 2 ** (5 - round_num)
        for i in range(num_teams):
            actual_results[round_num].append(season_outcome.iloc[0:num_teams, round_num + 1].values[i])
    return actual_results

def get_tourney_order(season):
    tourney_order = []
    for x in open('..\\django\\static\\app\\content\\order.txt', 'r'):
        tourney_order.append(get_name(x.strip(),season))
    return tourney_order

# returns results from tournament given a set of indicators
def get_tourney_results(season, indicators):
    tourney_order = []
    for x in open('..\\django\\static\\app\\content\\order.txt', 'r'):
        tourney_order.append(x.strip())

    #resets array in format [roundof32, sweet16, elite8, final4, finals, ncaa_winner]
    tourney_results = [[], [], [], [], [], []]
    next_round = tourney_order[:]

    for round_num in range(0, 6):        
        num_teams = 2 ** (6 - round_num)
        for i in range(0, num_teams, 2):

            team1 = next_round[i]
            team2 = next_round[i + 1]

            # which represents which team to append to the next_round
            # which 0 means team1 and which 2 means team2
            winner, loser, which = prediction(team1, team2, indicators, season)
            next_round.append(next_round[i + which])
            
            tourney_results[round_num].append(get_name(winner, season))

        del next_round[0:num_teams]

    return tourney_results


# calculates how many points the predicted got compared to actual
def get_points(tourney_results, actual_results):
    # initializes points and the amount of games correct
    points, games_correct = 0, 0
    
    # calculates how many points our algorithem predicts
    for round_num in range(0, 6):        
        num_teams = 2 ** (5 - round_num)
        for i in range(num_teams):
            if tourney_results[round_num][i] == actual_results[round_num][i]:
                points += round_num + 1
                games_correct += 1
    return points, games_correct

season = 2014
best_points = 0
best_games = 0
best_indicator = 'n/a'
actual_results = get_actual_results(season)


# nested loop to check every combination of two indicators
# this code is easily changed to simulate different situations
# change to [:, 3:] for regular use but takes long time
