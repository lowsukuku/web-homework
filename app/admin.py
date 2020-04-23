from django.contrib import admin

# Register your models here.
from app.models import Question, Answer, User, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(User)
admin.site.register(Tag)
