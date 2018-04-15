"""
Definition of views.
"""

from django.shortcuts import render
from app import generate_bracket
from win32timezone import now
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
listResults = []
listIndicator = []
listOrder = []
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'html/index.html',
        {
        }
    )



def bracket(request):
    inp_value = request.GET.get('results', 'This is a default value')
    context = {'inp_value': inp_value}
    year_Val = request.GET.get('yearSelect','This is a default value')
    context = {'year_Val': year_Val}
    year = int(year_Val)
    listResults = generate_bracket.get_tourney_results(year, [inp_value])
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
