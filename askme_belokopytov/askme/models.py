from django.db import models

QUESTIONS = [
    {
    'id': i,
    'title': f'Question {i}',
    'text': f'Text {i}',
    'likes' : f'Likes {i}',
    'tags' : [i,i,i,i]
    }for i in range(15)
]


ANSWERS = [
    {
    'id': i,
    'text': f'Text {i}',
    'likes' : f'Likes {i}',
    }for i in range(25)
]
