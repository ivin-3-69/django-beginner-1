from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from .models import Question,Choice
# Create your views here.
   
def index(request):
    latest_question_list = Question.objects.all()
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,'polls/index.html',context)

def detail(request ,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

def results(request , question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

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