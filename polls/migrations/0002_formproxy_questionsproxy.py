# Generated by Django 4.1.2 on 2022-12-10 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('polls.form_questions',),
        ),
        migrations.CreateModel(
            name='QuestionsProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('polls.questions_choices',),
        ),
    ]
