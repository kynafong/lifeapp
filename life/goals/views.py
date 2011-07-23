from life.goals.models import Goal, GoalCategory, DidIt, DidItGroup
from life.goals.forms import GoalCategoryForm, GoalForm
from datetime import datetime, date, timedelta

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required


def gather_goals():
    daily_goals = Goal.objects.filter(interval=1)
    weekly_goals = Goal.objects.filter(interval=2)
    monthly_goals = Goal.objects.filter(interval=3)
    return {
        'daily_goals': daily_goals,
        'monthly_goals': monthly_goals,
        'weekly_goals': weekly_goals,
    }


@login_required
def dun_did_it(request):
    data = {}
    if request.method == 'POST':
        submitted = request.POST
        yup_diditall = None
        try:
            for key in submitted:
                if key.split('-')[0] == 'goal':
                    if not yup_diditall:
                        yup_diditall = DidItGroup(user=request.user)
                        yup_diditall.save()
                    goal_id = int(key.split('-')[-1])
                    goal = Goal.objects.get(id=goal_id)
                    if goal.input_type == 'checkbox':
                        value = 1
                    elif goal.input_type == 'input':
                        value = float(submitted[key]) if submitted[key] else 0
                    if value:
                        yup_didit = DidIt(
                            group=yup_diditall,
                            goal=goal,
                            value=value
                        )
                        yup_didit.save()
            data['success'] = True
            if not yup_diditall:
                data['empty'] = True
        except ValueError:
            data['fail'] = True

    data.update(gather_goals())
    return render_to_response('dun-did-it.html', data, context_instance=RequestContext(request))



@login_required
def add_goal(request):

    if request.method == 'GET':
        data = {'form': GoalForm()}
        data['all_goals'] = Goal.objects.all()
        return render_to_response('manage-goals.html', data, context_instance=RequestContext(request))

    elif request.method == 'POST':
        submitted_form = GoalForm(request.POST)
        data = {}
        if submitted_form.is_valid():
            goal = submitted_form.save(commit=False)
            goal.user = request.user
            goal.save()
            data['success'] = True
            data['goal'] = goal.name
        else:
            data['fail'] = True 
        data['form'] = GoalForm()
        data['all_goals'] = Goal.objects.all()
        return render_to_response('manage-goals.html', data, context_instance=RequestContext(request))

@login_required
def add_category(request):

    if request.method == 'GET':
        data = {'form': GoalCategoryForm()}
        data['all_categories'] = GoalCategory.objects.all()
        return render_to_response('manage-categories.html', data, context_instance=RequestContext(request))

    elif request.method == 'POST':
        submitted_form = GoalCategoryForm(request.POST)
        data = {}
        if submitted_form.is_valid():
            category = submitted_form.save(commit=False)
            category.user = request.user
            category.save()
            data['success_save'] = True
            data['category'] = category.name
        else:
            data['fail'] = True
        data['form'] = GoalCategoryForm()
        data['all_categories'] = GoalCategory.objects.all()
        return render_to_response('manage-categories.html', data, context_instance=RequestContext(request))


@login_required
def delete_goal(request, goal_id):
    if request.method == 'GET':
        goal = Goal.objects.get(id=goal_id)
        goal.delete()
        return HttpResponseRedirect('/goals/')

    return HttpResponseBadRequest("Whoops")


@login_required
def delete_category(request, category_id):
    if request.method == 'GET':
        category = GoalCategory.objects.get(id=category_id)
        if Goal.objects.filter(category=category).exists():
            return HttpResponseBadRequest("Sorry, we cannot delete a category that has existing goals. Please delete those associated goals first.")
        category.delete()
        return HttpResponseRedirect('/categories/')

    return HttpResponseBadRequest("Whoops")


@login_required
def recent_didits(request):
    # 100 most recent
    dun_did_its = DidItGroup.objects.all().filter(didit__goal__is_public=True).order_by('-didit_date')[:100]
    data = {
        'dun_did_its': dun_did_its
    }
    return render_to_response('activity.html', data, context_instance=RequestContext(request))


@login_required
def toggle_goal_is_public(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    is_public = goal.is_public
    goal.is_public = not is_public
    goal.save()
    return HttpResponseRedirect('/goals/')


