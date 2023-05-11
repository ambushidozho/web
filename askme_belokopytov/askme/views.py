from django.contrib import auth
from django.http import Http404
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from askme.forms import AnswerForm, AskQuestionForm, LoginForm, ProfileEditForm, RegistrationForm, UserEditForm
from . import models
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def index(request):
    context = {
               'page': paginate(models.Question.objects.get_new(), request)[1],
               'title': "New questions"
               }
    return render(request, 'index.html', context)

def question(request, question_id):
    
    #try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                answer_form = AnswerForm(request.POST)
                if answer_form.is_valid():
                    answer_form.save(request, models.Question.objects.get(pk=question_id))
            else:
                return redirect(reverse('login'))
        else:
            answer_form = AnswerForm()
        context =   {
                    'question': models.Question.objects.get(pk=question_id),
                    'page': paginate(models.Answer.objects.get_ans_by_id(models.Question.objects.get(pk=question_id)), request)[1],
                    'form' : answer_form
                  }
        return render(request, 'question.html', context)
    #except:
     #   raise Http404("No such question")
    
@login_required(login_url="/login/", redirect_field_name='continue')
def ask(request):
    if request.method == 'GET':
        ask_form = AskQuestionForm()
    elif request.method == 'POST':
        ask_form = AskQuestionForm(request.POST)
        if ask_form.is_valid():
            question = ask_form.save(request)
            return redirect('question', question_id=question.id)
            
    return render(request, 'ask.html', {'form': ask_form})


def log_in(request):
    if request.method == 'GET':
        Login_form = LoginForm()
    elif request.method == 'POST':
        Login_form = LoginForm(request.POST)
        if Login_form.is_valid():
            user = auth.authenticate(request=request, **Login_form.cleaned_data)
            if user:
                login(request, user)
                if(request.GET.get('continue')):
                    return redirect(request.GET.get('continue'))
                else:
                    return redirect(reverse('index'))
            Login_form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', context= {'form': Login_form})

def signup(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error")
    return render(request, 'signup.html', context={'form': user_form})



                    


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
    return (request, page_obj)


def log_out(request):
    logout(request)
    return redirect(reverse('index'))


@login_required(login_url="/login/", redirect_field_name='continue')
def settings(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                    'settings.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})
    