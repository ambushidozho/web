# Generated by Django 4.2 on 2023-05-21 21:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0009_remove_question_pubdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='question',
            name='pubdate',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]