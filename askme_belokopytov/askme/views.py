import time
from uuid import uuid4
from django.contrib import auth
from django.forms import model_to_dict
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
import jwt
from askme.forms import AnswerForm, AskQuestionForm, LoginForm, ProfileEditForm, RegistrationForm, UserEditForm

from . import models
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_GET, require_POST
from cent import Client

# Create your views here.

def index(request):
    context = {
               'page': paginate(models.Question.objects.get_new(), request)[1],
               'title': "New questions"
               }
    return render(request, 'index.html', context)

client = Client("http://localhost:8082/api", api_key="fbe87e0e-a41e-476a-abd6-8690b1e836b5", timeout=1)

def question(request, question_id): 
    try:
        if request.method == 'POST':
            if request.user.is_authenticated:
                answer_form = AnswerForm(request.POST)
                if answer_form.is_valid():
                    answer = answer_form.save(request, models.Question.objects.get(pk=question_id))
                    #client.publish(f'question_{question_id}', model_to_dict(answer))
                    answer_form = AnswerForm()
                    context =  {
                        'question': models.Question.objects.get(pk=question_id),
                        'page': paginate(models.Answer.objects.get_ans_by_id(models.Question.objects.get(pk=question_id)), request)[1],
                        'form' : answer_form,
                        'user': request.user,
                    }
                if request.user.is_authenticated:
                    context.update(
                        {
                            'server_address' : 'ws://127.0.0.1:8082/connection/websocket',
                            'cent_channel' : f'question_{question_id}',
                            'secret_token': jwt.encode({"sub": str(request.user.pk), "exp": int(time.time() + 10*60)}, "8b6c0d20-0cd0-46a2-957d-92b0d625daf4")
                        }
                    )
                return redirect('question',question_id=question_id)
            else:
                return redirect(reverse('login'))
        else:
            answer_form = AnswerForm()
            context =  {
                        'question': models.Question.objects.get(pk=question_id),
                        'page': paginate(models.Answer.objects.get_ans_by_id(models.Question.objects.get(pk=question_id)), request)[1],
                        'form' : answer_form,
                        'user': request.user,
                    }
            # if request.user.is_authenticated:
            #     context.update(
            #         {
            #             'server_address' : 'ws://127.0.0.1:8082/connection/websocket',
            #             'cent_channel' : f'question_{question_id}',
            #             'secret_token': jwt.encode({"sub": str(request.user.pk), "exp": int(time.time() + 10*60)}, "8b6c0d20-0cd0-46a2-957d-92b0d625daf4")
            #         }
            #     )
            return render(request, 'question.html', context)
    except:
      raise Http404("No such question")
    

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


@login_required()
@require_POST
def vote_up(request):
    question_id = request.POST['question_id']
    question = models.Question.objects.get(id=question_id)
    likes = models.LikeQuestion.objects.filter(question=question)
    for like in likes:
        if(like.profile == request.user.profile):
            question.likes -= 1
            question.save()
            like.delete()
            return JsonResponse(
            {
                'new_rating': question.likes
            })
    question.likes += 1
    question.save()
    like = models.LikeQuestion.objects.create(question=question, profile=request.user.profile)
    like.save()
    return JsonResponse(
        {
            'new_rating': question.likes
        }
    )


@login_required()
@require_POST
def vote_up_for_answer(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    likes = models.LikeAnswer.objects.filter(answer=answer)
    for like in likes:
        if(like.profile == request.user.profile):
            answer.likes -= 1
            answer.save()
            like.delete()
            return JsonResponse(
            {
                'new_rating': answer.likes
            })
    answer.likes += 1
    answer.save()
    like = models.LikeAnswer.objects.create(answer=answer, profile=request.user.profile)
    like.save()
    return JsonResponse(
        {
            'new_rating': answer.likes
        }
    )



@login_required()
@require_POST
def correct(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if(answer.correct):
        answer.correct = False;
    else:
        answer.correct = True;
    print(answer.correct)
    answer.save()
    return JsonResponse(
        {
            'correct': answer.correct
        }
    )



    