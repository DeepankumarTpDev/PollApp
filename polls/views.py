from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.db.models import F
from django.urls import reverse
from .models import Question,Choice
from django.views import generic


class IndexView(generic.ListView):
    model = Question
    context_object_name = "latest_question_list"
    template_name = "polls/index.html"


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        return render(request, "polls/detail.html", {'question':question,'error_message' : "You didn't select a choice.",})
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save() 
        #It is always a good practice to return responserdirect after submiting a post http
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))