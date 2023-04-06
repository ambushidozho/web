from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def get_new(self):
        return self.filter().order_by('pubdate')
    
    def get_tag(self, _tag):
        return self.filter(tag__name=_tag)
    
    def get_best(self):
        return self.filter().order_by('-likes')
    
    def get_num_of_answers(self):
       try:
        return Question.objects.annotate(Count('answer'))[1].answer__count
       except:
           pass
    
class Question(models.Model):
    likes = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=10000)
    profile = models.ForeignKey('Profile', 
                                on_delete=models.CASCADE,
                                related_name='questions')
    tag = models.ManyToManyField('Tag', default="")
    pubdate = models.DateField(auto_now = True)
    objects = QuestionManager()

class AnswerManager(models.Manager):
    def get_ans_by_id(self, _question):
        return self.filter(question=_question)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    likes = models.IntegerField(default=0)
    objects = AnswerManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to ='../uploads/', default = '../static/img/ava.png')

    #не работает аватар
    


class Tag(models.Model):
    name = models.CharField(max_length=255)

