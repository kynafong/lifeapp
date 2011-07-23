from django.contrib import admin

from life.goals.models import *

admin.site.register(GoalCategory)
admin.site.register(Goal)
admin.site.register(DidIt)
admin.site.register(DidItGroup)
