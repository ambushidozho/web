from django.shortcuts import render
from . import models
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    page = paginate(models.QUESTIONS, request)[1]
    context = {
               'page': page
               }
    return render(request, 'index.html', context)

def question(request, question_id):
    page = paginate(models.ANSWERS, request)[1]
    context =   {
                'question': models.QUESTIONS[question_id],
                'page': page,
                'questions': models.QUESTIONS
                }
    
    return render(request, 'question.html', context)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def hot(request):
    return render(request, ' ')

def tag(request):
    page = paginate(models.QUESTIONS, request)[1]
    return render(request, 'tag.html', page)

def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return (request,page_obj)