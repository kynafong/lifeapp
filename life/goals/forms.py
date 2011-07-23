from django import forms
from django.forms import ModelForm

from life.goals.models import Goal, GoalCategory, DidIt

class GoalCategoryForm(ModelForm):
    class Meta:
        model = GoalCategory
        exclude = ('user', )

class GoalForm(ModelForm):
    class Meta:
        model = Goal
        exclude = ('user', )


