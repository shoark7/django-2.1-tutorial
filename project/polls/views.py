from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


## Class-based generic views
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_ones'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


## Function views
def index(request):
    latest_ones = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_ones': latest_ones
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def say_hi(request):
    return HttpResponse("<i>Fuck it up!!</i>")


def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': q})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
                        'question': question,
                        'error_message': "You didn't select a chocie!"})
    choice.votes += 1
    choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
