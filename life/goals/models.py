from django.db import models
from datetime import datetime, date, timedelta

from django.contrib.auth.models import User

GOAL_INTERVALS = (
    (1, 'daily'),
    (2, 'weekly'),
    (3, 'monthly'),
)

GOAL_INPUT_TYPES = (
    ('checkbox', 'checkbox'),
    ('input', 'input'),
)

class GoalCategory(models.Model):
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1024)

    def __unicode__(self):
        return '%s' %self.name

class Goal(models.Model):
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1024)
    category = models.ForeignKey(GoalCategory)
    input_type = models.CharField(max_length=200,choices=GOAL_INPUT_TYPES)
    interval = models.PositiveSmallIntegerField(choices=GOAL_INTERVALS)
    target_total = models.IntegerField()
    is_public = models.BooleanField(default=True)

    def done_today(self):
        today = date.today()
        start_today = datetime(today.year, today.month, today.day)
        return DidIt.objects.filter(goal=self,group__didit_date__gte=start_today).exists()

    def progress_summary(self):
        today = date.today()

        if self.interval == 1: # daily

            NUM_DAYS_INCLUDE = 7
            x_days_ago = datetime(today.year, today.month, today.day) - timedelta(days=NUM_DAYS_INCLUDE)
            total_so_far = DidIt.objects.filter(goal=self,group__didit_date__gte=x_days_ago).count()

            return 'Dun %s times in last %s days. Target %sx daily.' \
                %(total_so_far, NUM_DAYS_INCLUDE, self.target_total)

        elif self.interval == 2: # weekly
            num_days_passed = today.weekday() # 0 is Monday (num days passed this week)
            start_of_week = datetime(today.year, today.month, today.day) - timedelta(days=num_days_passed)
            total_so_far = DidIt.objects.filter(goal=self,group__didit_date__gte=start_of_week).count()
            num_days_remaining = 7 - num_days_passed
            interval = 'week'

            return 'Dun %s times this %s. Target %sx %s. %s days left.' \
                %(total_so_far, interval, self.target_total, self.get_interval_display(), num_days_remaining)

        elif self.interval == 3: #monthly
            start_of_month = datetime(today.year, today.month, 1)
            num_days_passed = today.day - 1  # num days passed this month (excluding today)
            total_so_far = DidIt.objects.filter(goal=self,group__didit_date__gte=start_of_month).count()
            interval = 'month'
            if today.month in (1, 3, 5, 7, 8, 10, 12):
                num_days_remaining = 31 - num_days_passed - 1 # (exclude today)
            elif today.month in (4, 6, 9, 11):
                num_days_remaining = 30 - num_days_passed - 1
            elif today.year % 4: # februrary not leap year
                num_days_remaining = 28 - num_days_passed - 1
            else: # februrary leap year
                num_days_remaining = 28 - num_days_passed - 1

            return 'Dun %s times this %s. Target %sx %s. %s days left.' \
                %(total_so_far, interval, self.target_total, self.get_interval_display(), num_days_remaining)

    def __unicode__(self):
        return '%s' %self.name


class DidItGroup(models.Model):
    user = models.ForeignKey(User)
    didit_date = models.DateTimeField(auto_now_add=True)

    def summary(self):
        return DidIt.objects.filter(group=self,goal__is_public=True)


class DidIt(models.Model):
    group = models.ForeignKey(DidItGroup)
    goal = models.ForeignKey(Goal)
    value = models.FloatField()

    def __unicode__(self):
        return '%s' %self.name


