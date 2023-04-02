from django.shortcuts import render
from . import models
# Create your views here.
def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)

def question(request, question_id):
    context = {'questions': models.QUESTIONS[question_id]}
    return render(request, 'question.html', context)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')