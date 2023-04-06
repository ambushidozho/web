from django.core.management.base import BaseCommand
from askme import models
import random
import string

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('[ratio]')

    def handle(self, *args, **options):
        ratio = (int)(options['[ratio]'][1 : -1])
        letters = string.ascii_lowercase  
 
        # for i in range(ratio):
        #     _user = models.User(password="ambush", username=''.join(random.choice(letters) for i in range(8)))
        #     _user.save()
        #     _profile = models.Profile(pk=_user.pk,nickname = _user.username)
        #     _profile.save()
        #     _tag = models.Tag(name = ''.join(random.choice(letters) for i in range(8)))
        #     _tag.save()
        #     for i in range(10):
        #         _question = models.Question(title = ''.join(random.choice(letters) for i in range(8)),
        #                                    text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolores, minima ut molestias aspernatur magni etquo sunt quidem harum ad eligen",
        #                                    profile = _profile,
        #                                    )
        #         _question.save()
        #         _question.tag.add(_tag)
        #         for i in range(10):
        #             _answer = models.Answer(text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolores, minima ut molestias aspernatur magni etquo sunt quidem harum ad eligen",
        #                                     question = _question)
        #             _answer.save()

        users = [models.User(password="ambush", username=''.join(random.choice(letters) for i in range(8))) for i in range(ratio)]
        models.User.objects.bulk_create(users)
        profiles = [models.Profile(pk=users[i].pk, nickname = users[i].username) for i in range(ratio)]
        models.Profile.objects.bulk_create(profiles)
        tags = [models.Tag(name = ''.join(random.choice(letters) for i in range(8))) for i in range(ratio)]
        models.Tag.objects.bulk_create(tags)
        
        questions = [models.Question(title = ''.join(random.choice(letters) for i in range(8)),
                                     text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolores, minima ut molestias aspernatur magni etquo sunt quidem harum ad eligen",
                                     profile = profiles[i % ratio],
                                     ) 
                                     for i in range(ratio * 10)]
        
        models.Question.objects.bulk_create(questions)
        # problems with avatars in db   FIX THIS!!!!
        for i in range(ratio * 10):
            questions[i].tag.add(tags[i % ratio])

        answers = [models.Answer(question = questions[i % (ratio * 10)],
                                 text = "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolores, minima ut molestias aspernatur magni etquo sunt quidem harum ad eligen") 
                                 for i in range(ratio * 100)]
       

        models.Answer.objects.bulk_create(answers)



        

