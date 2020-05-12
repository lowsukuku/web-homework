from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from app.models import Question, Answer, User, Tag
from faker import Faker
from faker.providers import profile, lorem
from datetime import datetime
from random import random, randrange, randint

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-t', nargs=1, type=int)
        parser.add_argument('-u', nargs=1, type=int)
        parser.add_argument('-q', nargs=1, type=int)
        parser.add_argument('-a', nargs=1, type=int)

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(datetime.now())
        if (options['t'] != None):
            for i in range(options['t'][0]):
                tag = Tag()
                tag.title = fake.word()
                try:
                    tag.validate_unique()
                except ValidationError:
                    tag.title+=fake.word()
                tag.save()
                self.stdout.write(f'tag {i}')
        tags_qs = Tag.objects.all()
        if (options['u'] != None):
            for i in range(options['u'][0]):
                user = User()
                user.username = fake.simple_profile().get('username')
                try:
                    user.validate_unique()
                except ValidationError:
                    user.username += fake.simple_profile().get('username')
                user.save()
                self.stdout.write(f'user {i}')
        users_qs = User.objects.all()
        users_count = User.objects.count()
        if (options['q'] != None):
            for i in range(options['q'][0]):
                question = Question()
                question.author = users_qs[randint(0, users_count-1)]
                question.rating = randint(-1000, 1000)
                question.title = fake.sentence(nb_words=5)
                question.text = fake.text(max_nb_chars=256)
                question.save()
                for j in range(randint(1, 5)):
                    question.tags.add(tags_qs[randint(0, 99)])
                self.stdout.write(f'question {i}')
        questions_qs = Question.objects.all()
        questions_count = Question.objects.count()
        if (options['a'] != None):
            for i in range(options['a'][0]):
                answer = Answer()
                answer.text = fake.text(max_nb_chars=256)
                answer.author = users_qs[randint(0, users_count-1)]
                answer.question = questions_qs[randint(0, questions_count-1)]
                answer.save()
                self.stdout.write(f'answer {i}')

            


        
