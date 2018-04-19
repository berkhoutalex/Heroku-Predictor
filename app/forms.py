"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class TextForm(forms.Form): #input for text field

    text_search = forms.CharField(label='Text Search', max_length=100)

class SelectYear(forms.Form):# drop down menu
           year = forms.CharField(widget=forms.Select)

class IndicatorForm(forms.Form):
        OPTIONS = (
("G", "Games"),
("W", "Wins"),
("L" , "Losses"),
("FGM", "Field Goals Made"),
("FGA", "Field Goals Attempted"),
("FG%","Field Goal Percentage"),
("FGM3", "Three Point Field Goals Made"),
("FGA3", "Three Point Field Goals Attempted"),
("FG3%", "Three Point Field Goal Percentage"),
("FTM" , "Free Throws Made"),
("FTA" , "Free Throws Attempted"),
("FT%" , "Free Throw Percentage"),
("OR" , "Offensive Rating"),
("DR" , "Defensive Rating"),
("Ast" , "Assists"),
("TO", "Turnovers"),
("Stl", "Steals"),
("Blk", "Blocks"),
("PF", "Points For"),
("OFGM", "Opponent Field Goals Made"),
("OFGA", "Opponent Field Goals Attempted"),
("OFGM3", "Opponent Three Point Field Goals Made"),
("OFGA3", "Opponent Three Point Field Goals Attempted"),
("OFTM", "Opponent Free Throws Made"),
("OFTA", "Opponent Free Throws Attempted"),
("OOR", "Opponent Offensive Rating"),
("ODR", "Opponent Defensive Rating"),
("OAst", "Opponent Assists"),
("OTO", "Opponent Turnovers"),
("OStl", "Opponent Steals"),
("OBlk", "Opponent Blocks"),
("OPF", "Opponent Points For")
                )
        Indicators = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=OPTIONS)


