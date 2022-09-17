from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Answers
from django.shortcuts import render, get_object_or_404, reverse


def index(request):
    questions = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': questions}
    return HttpResponse(render(request, 'polls/index.html', context))


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist():
    #     raise Http404("Page Not Found")
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return HttpResponse(render(request, 'polls/detail.html', context))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
        selected = question.answers_set.get(pk=request.POST['choice'])
    except (KeyError, Answers.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You Did not choose any Answer"
        })
    else:
        selected.vote += 1
        selected.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
