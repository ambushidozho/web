# Generated by Django 4.2 on 2023-05-21 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0008_answer_correct_answer_pub_date_alter_answer_profile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='pubdate',
        ),
    ]