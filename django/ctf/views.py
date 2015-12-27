import inspect

from django.http.response import HttpResponseNotAllowed, HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, render_to_response, redirect
from django.contrib import messages
from django.views.generic import DetailView
from django.conf import settings

from . import models


# region Helpers

def get_default_dict(request):
    result = {}
    result['production'] = not settings.DEBUG
    # TODO(Yatharth): Add current team ID so can link to team detail view
    return result


def http_method(method):
    """Decorates views to check for HTTP method"""
    assert method in ('GET', 'POST', 'PUT', 'DELETE')
    # TODO(Yatharth): Show custom page per http://stackoverflow.com/questions/4614294
    error = HttpResponseNotAllowed('Only {} requests allowed here'.format(method))

    def decorator(view):

        # If view is a class
        if inspect.isclass(view):
            old_get = view.get

            def new_get(self, request, *args, **kwargs):
                if request.method != method:
                    return error
                return old_get(self, request, *args, **kwargs)

            view.get = new_get

            return view

        # if view is a function
        else:
            def decorated(request, *args, **kwargs):
                if request.method != method:
                    return error
                return view(request, *args, **kwargs)

            return decorated

    return decorator


# endregion


# region GETs

@http_method('GET')
def index(request):
    if request.META.get('REQUEST_METHOD') != 'GET':
        return HttpResponseNotAllowed('Only GET allowed')

    return render(request, 'ctf/index.html')


@http_method('GET')
def game(request):
    params = get_default_dict(request)
    params['prob_list'] = models.CtfProblem.objects.all
    # TODO(yatharth): return from session or whatever shit
    params['team'] = models.Team.objects.get(id=1)
    return render(request, 'ctf/game.html', params)


# TODO: should it just be '/team' to go to logged in one and disallow viewing other teams' pages?
# Cam: I think we should have /team always display your team's page, but /team/<t_id> should let you view another team's page
@http_method('GET')
class TeamDetailView(DetailView):
    model = models.Team
    template_name = 'ctf/team.html'

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context.update(get_default_dict(self.request))
        return context


# endregion


# region POSTs

@http_method('POST')
def submit_flag(request, problem_id):
    # TODO(Yatharth): Record in db
    flag = request.POST.get('flag', '')
    # TODO(Cam): Calculate team from session
    team = models.Team.objects.get(id=1)

    try:
        problem = models.CtfProblem.objects.get(id=problem_id)
    except models.CtfProblem.DoesNotExist:
        return HttpResponseNotFound("Problem with id {} not found".format(problem_id))
    else:
        correct, message = problem.grade(flag)
        if problem_id not in team.submissions:
            team.submissions[problem_id] = []
        if flag in team.submissions[problem_id]:
            messager = messages.error
            message = "You or someone on your team has already tried this!"
        else:
            if correct:
                messager = messages.success
                team.score += problem.points
            else:
                messager = messages.error
            team.submissions[problem_id].append(flag)
            team.save()
        messager(request, message)
        return redirect('ctf:game')

# endregion
