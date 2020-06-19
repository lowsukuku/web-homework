from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class User(AbstractUser):
    upload = models.ImageField(upload_to='avatars', blank=True)
    

class Tag(models.Model):
    title = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    VOTES = ((+1, 'like'),(-1, 'dislike'))

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    objects = LikesManager()
    
class Contribution(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    likes = GenericRelation(Like, related_query_name='contrib')
    create_date = models.DateTimeField(
    default=timezone.now)

    class Meta:
        abstract = True

class Question(Contribution):
    title = models.CharField(max_length=128)
    is_active = models.BooleanField(
        default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-create_date']

class Answer(Contribution):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

