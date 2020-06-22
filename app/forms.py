from django.forms import ModelForm
from app.models import Answer, Question, User
from django.forms.widgets import SelectMultiple, TextInput, Textarea
from django.forms.fields import CharField

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name','upload']
