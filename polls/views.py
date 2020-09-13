from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone

from .models import Question,Choice
   
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.localtime()).order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request ,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        context = {
            'question' : question ,
            'error_message' : "you didnt select anything yet",
        }
        return render(request,"polls/details.html",context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
