"""
Definition of views.
"""

from django.shortcuts import render
from app import generate_bracket
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
listResults = []
listIndicator = []
listOrder = []
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
    #inp_value = request.GET.getlist('selectInd', 'W')
    year_Val = request.GET.get('yearSelect','This is a default value')

    # get checkbox values
    indicators = []
    for i in range(1, 33):
        indicator = request.GET.get('i' + str(i), 'default')
        if (indicator is not 'default'):
            indicators.append(indicator)

    year = int(year_Val)
    listResults = generate_bracket.get_tourney_results(year, indicators)
    listOrder = generate_bracket.get_tourney_order(year)

    if listResults[5][0] == listResults[4][1]:
        loser = listResults[4][0]
    else:
        loser = listResults[4][1]

    return render(
        request,
        'html/bracket.html',
        {
            'round1':listOrder,
            'roundOthers':listResults,
            'loser':loser
        }
    )


# def bracket(request):
#    listResults = generateBracket.get_tourney_results(2015, ['OPF'])
#    listOrder = generateBracket.get_tourney_order(2015)
#    """Renders the home page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'html/bracket.html',
#        {
#            'round1':listOrder,
#            'roundOthers':listResults
#
#        }
