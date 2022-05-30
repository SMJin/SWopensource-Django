from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone

from .models import Question

def new(request):
    return render(request, 'polls/new.html')

def create(request):
    new_poll = Question()
    new_poll.question_text = request.POST['title']
    new_poll.pub_date = timezone.now()
    new_poll.save()

    new_choice_one = Choice()
    new_choice_one.question = new_poll
    new_choice_one.choice_text = request.POST['select_one']
    new_choice_one.votes = 0
    new_choice_one.save()

    new_choice_two = Choice()
    new_choice_two.question = new_poll
    new_choice_two.choice_text = request.POST['select_two']
    new_choice_two.votes = 0
    new_choice_two.save()

    return redirect('polls:detail', new_poll.id)



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExixt):
        return render(reqeust, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
