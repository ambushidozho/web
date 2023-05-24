import datetime
from django.core.management.base import BaseCommand
from askme import models
import random
import string
import sqlite3

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('[ratio]')

    def handle(self, *args, **options):
        ratio = (int)(options['[ratio]'][1 : -1])
        letters = string.ascii_lowercase  
        
        users = [models.User(password="ambush", username=''.join(random.choice(letters) for i in range(8))) for i in range(ratio)]
        models.User.objects.bulk_create(users)
        profiles = [models.Profile(pk=users[i].pk, nickname = users[i].username) for i in range(ratio)] # to upload avatar we need a form that real user will have
        models.Profile.objects.bulk_create(profiles)
        tags = [models.Tag(name = ''.join(random.choice(letters) for i in range(8))) for i in range(ratio)]
        models.Tag.objects.bulk_create(tags)
        
        questions = [models.Question(title = ''.join(random.choice(letters) for i in range(8)),
                                     text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolores, minima ut molestias aspernatur magni etquo sunt quidem harum ad eligen",
                                     profile = profiles[i % ratio],
                                     pubdate = datetime.date(year=2023, month=((i % 12) + 1), day=12),
                                     likes = random.randint(0,100)
                                     ) 
                                     for i in range(ratio * 10)]
        
        models.Question.objects.bulk_create(questions)
        for i in range(ratio * 10):
            questions[i].tag.add(tags[i % ratio])

        answers = [models.Answer(question = questions[i % (ratio * 10)],
                                 text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolores, minima ut molestias aspernatur magni etquo sunt quidem harum ad eligen",
                                 profile = profiles[i % ratio],
                                 likes = random.randint(0,100))
                                 for i in range(ratio * 100)]
       

        models.Answer.objects.bulk_create(answers)

        likesQuestions = [models.LikeQuestion(question = questions[i % (ratio * 10)],
                                 profile = profiles[i % ratio],
                                 )
                                 for i in range(ratio * 200)]
        
        models.LikeQuestion.objects.bulk_create(likesQuestions)

        likesAnswers = [models.LikeAnswer(answer = answers[i % (ratio * 100)],
                                 profile = profiles[i % ratio],
                                 )
                                 for i in range(ratio * 200)]
        
        models.LikeAnswer.objects.bulk_create(likesAnswers)



        

