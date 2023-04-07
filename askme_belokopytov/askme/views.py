from django.http import Http404
from django.shortcuts import render
from . import models
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    context = {
               'page': paginate(models.Question.objects.get_new(), request)[1],
               'page_range' : paginate(models.Question.objects.get_new(), request)[2],
               'title': "New questions"
               }
    return render(request, 'index.html', context)

def question(request, question_id):
    
    try:
        context =   {
                   'question': models.Question.objects.all()[question_id - 1],
                  'page': paginate(models.Answer.objects.get_ans_by_id(models.Question.objects.all()[question_id - 1]), request)[1],
                  }
        return render(request, 'question.html', context)
    except:
        raise Http404("No such question")

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def hot(request):
    context = {
               'page': paginate(models.Question.objects.get_best(), request)[1],
               'title': "Hot questions"
               }
    return render(request, 'index.html', context)

def tag(request, tagname):
    context = {
               'page': paginate(models.Question.objects.get_tag(tagname), request)[1],
               'title': tagname
               }
    return render(request, 'index.html', context)

def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    page_obj.number
    page_range = p.get_elided_page_range(number=page_number)
    return (request, page_obj, page_range)