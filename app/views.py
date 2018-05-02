"""
Definition of views.
"""

from django.shortcuts import render
from app import generate_bracket
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import urllib
import boto3

listResults = []
listIndicator = []
listOrder = []


scores_2014_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2014.txt"
scores_2015_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2015.txt"
scores_2016_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2016.txt"
scores_2017_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2017.txt"
scores_2018_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2018.txt"


url2014 = urllib.urlopen(scores_2014_file)
scores_14 = sorted(url2014.read().split("|"))
url2015 = urllib.urlopen(scores_2015_file)
scores_15 = sorted(url2015.read().split("|"))
url2016 = urllib.urlopen(scores_2016_file)
scores_16 = sorted(url2016.read().split("|"))
url2017 = urllib.urlopen(scores_2017_file)
scores_17 = sorted(url2017.read().split("|"))
url2018 = urllib.urlopen(scores_2018_file)
scores_18 = sorted(url2018.read().split("|"))



def home(request): #home page request
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'html/index.html',
        {
        }
    )




def bracket(request): #bracket page request
    # get year from dropdown
    year_Val = request.GET.get('yearSelect','This is a default value')
    year = int(year_Val)

    # list of all indicators used in loop below
    all_indicators = ['Seed','G','W','L','Eff','FGM','FG%','eFG%','FGA','FGM3','FG3%',
                      'FGA3','FTM','FT%','FTA','OR','ORB%','DR','DRB%','Ast','TO',
                      'TOV%','Stl','Blk','PF','OFGM','OFGA','OFG%','OeFG%','OFGM3',
                      'OFGA3','OFG3%','OFTM','OFTA','OFT%','OOR','OORB%','ODR',
                      'ODRB%','OAst','OTO','OTOV%','OStl','OBlk','OPF']      
    indicators = []
    weights = []

    # get list of selected indicators and their weights
    for i in range(0, len(all_indicators)):
        indicator = request.GET.get('i' + str(i), 'off')
        if (indicator == 'on'):
            weight = int(request.GET.get('w' + str(i), '50'))
            weights.append(weight)
            indicators.append(all_indicators[i])

    # if no indicators are checked, use seed by default
    if len(indicators) == 0:
        indicators.append('Seed')
        weights.append('1.0')

    # get tourney actual predicted results and points from generate_bracket.py
    listResults = generate_bracket.get_tourney_results(year, indicators, weights)
    listOrder = generate_bracket.get_tourney_order(year)
    predicted_results_no_names = generate_bracket.get_tourney_results_no_names(year, indicators, weights)
    actual_results = generate_bracket.get_actual_results(year)
    
    points = generate_bracket.get_points(predicted_results_no_names, actual_results)
    percentage = points[1] * 100 / 63

    # get loser of final game
    if listResults[5][0] == listResults[4][1]:
        loser = listResults[4][0]
        loser_no_name = predicted_results_no_names[4][0]
        actual_loser = actual_results[4][0]
    else:
        loser = listResults[4][1]
        loser_no_name = predicted_results_no_names[4][1]
        actual_loser = actual_results[4][1]

    # get list of colors to color the team names
    # green means you predicted correctly
    # red means you predicted incorrectly
    green = "#0aaa0a"
    red = "#ff0000"
    colors = []
    finalcolors = []
    if actual_loser == loser_no_name:
        finalcolors.append(green)
    else:
        finalcolors.append(red)

    if predicted_results_no_names[5][0]==actual_results[5][0]:
        finalcolors.append(green)
    else:
        finalcolors.append(red)

    for i in range(len(actual_results)):
        for j in range(len(actual_results[i])):
            if actual_results[i][j] == predicted_results_no_names[i][j] :
                colors.append(green)
            else:
                colors.append(red)

    # get string for formula
    percentages = [1.0 * weight / sum(weights) for weight in weights]
    formula_string = ""
    for i in range(len(indicators)):
        if percentages[i] < 0.01:
            percent = '{:.3f}'.format(percentages[i])
        else:
            percent = '{:.2f}'.format(percentages[i])
        formula_string += str(indicators[i]) + " * " + percent + " + "
    formula_string = formula_string[:-3]

    output_string = str(points[0]) + " " + ','.join(str(x) for x in indicators)+ " " + ','.join(str(x) for x in weights)

    if int(year_Val) == 2014:
            index = 0
            for i in scores_14:
                tempScore = scores_14[index].split();
                if int(points[0]) > int(tempScore[0]):

                    scores_14[index]=output_string
                    s3 = boto3.resource('s3')
                    bucket = 'predictorbucket' 
                    file_name = "static/app/content/Score_" + year_Val + ".txt"
                    object = s3.Object(bucket, file_name)
                    scores_14.sort()
                    output = '|'.join(scores_14)

                    object.put(Body=output)
                    break
                index = index + 1

    elif int(year_Val) == 2015:
            index = 0
            for i in scores_15:
                tempScore = scores_15[index].split();
                if int(points[0]) > int(tempScore[0]):
                    scores_15[index]=output_string
                    s3 = boto3.resource('s3')
                    bucket = 'predictorbucket' 
                    file_name = "static/app/content/Score_" + year_Val + ".txt"
                    object = s3.Object(bucket, file_name)
                    scores_15.sort()
                    output = '|'.join(scores_15)
                    object.put(Body=output)
                    break
                index = index + 1
    elif int(year_Val) == 2016:
            index = 0
            for i in scores_16:
                    
                    tempScore = scores_16[index].split();
                    if int(points[0]) > int(tempScore[0]):
                        scores_16[index]=output_string
                        s3 = boto3.resource('s3')
                        bucket = 'predictorbucket' 
                        file_name = "static/app/content/Score_" + year_Val + ".txt"
                        object = s3.Object(bucket, file_name)
                        scores_16.sort()
                        output ='|'.join(scores_16)
                        object.put(Body=output)
                        break
                    index = index + 1
    elif int(year_Val) == 2017:
            index = 0
            for i in scores_17:
                tempScore = scores_17[index].split();
                if int(points[0]) > int(tempScore[0]):
                    scores_17[index]=output_string
                    s3 = boto3.resource('s3')
                    bucket = 'predictorbucket' 
                    file_name = "static/app/content/Score_" + year_Val + ".txt"
                    object = s3.Object(bucket, file_name)
                    scores_17.sort()
                    output ='|'.join(scores_17)
                    object.put(Body=output)
                    break
                index = index + 1
    else:
            index = 0
            for i in scores_18:
                tempScore = scores_18[index].split();
                if int(points[0]) > int(tempScore[0]):
                    scores_18[index]=output_string
                    s3 = boto3.resource('s3')
                    bucket = 'predictorbucket' 
                    file_name = "static/app/content/Score_" + year_Val + ".txt"
                    object = s3.Object(bucket, file_name)
                    scores_18.sort()
                    output = '|'.join(scores_18)
                    object.put(Body=output)
                    break
                index = index + 1


        
    return render(
        request,
        'html/bracket.html',
        {
            'round1':listOrder,
            'roundOthers':listResults,
            'loser':loser,
            'points':points[0],
            'games_correct':points[1],
            'percent_right':percentage,
            'colors':colors,
            'finalcolors':finalcolors,
            'formula_string':formula_string
        }
    )

    
def highscore(request): #high score page request
    score14 = []
    score15 = []
    score16 = []
    score17 = []
    score18 = []
    for score in scores_14:
        score14.append(score.split(" "))
    for score in scores_15:
        score15.append(score.split(" "))
    for score in scores_16:
        score16.append(score.split(" "))
    for score in scores_17:
        score17.append(score.split(" "))
    for score in scores_18:
        score18.append(score.split(" "))

    return render(
        request,
        'html/highscore.html',
        {
            'score14' : score14,
            'score15' : score15,
            'score16' : score16,
            'score17' : score17,
            'score18' : score18
        }
    )