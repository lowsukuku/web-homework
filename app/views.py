from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from app.models import Question, Answer, Tag, User
from random import randint
from datetime import datetime
from time import time
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

tags = [
    f'tag {i}'
    for i in range(100)
]

user = {
    'name': 'nibba'
}

answers = {
    i: {'id': i, 'text': f'Hello world! This is my answer {i}',
        'rating': randint(-100, 100), 'creator': user, 'creationTime': datetime.now()}
    for i in range(100)
}

def newQuestions(request):
    page, pages = paginate(
        Question.objects.filter(is_active=True), request, 10)
    return render(request, 'index.html', {
        'questions': page,
        'pages': pages,
    })


def hotQuestions(request):
    page, pages = paginate(
        Question.objects.filter(is_active=True).order_by('-rating'), request, 10)
    return render(request, 'index.html', {
        'questions': page,
        'pages': pages,
    })


def listByTag(request, tag):
    tag = Tag.objects.get(title=tag)
    page, pages = paginate(
        Question.objects.filter(is_active=True).filter(tags=tag), request, 10)
    return render(request, 'index.html', {
        'questions': page,
        'pages': pages
    })


def questionById(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    page, pages = paginate(Answer.objects.filter(question=question_id), request, 10)
    return render(request, 'question.html', {
        'question': question,
        'answers': page,
        'pages': pages
    })


def user_login(request):
    return render(request, 'login.html', {})

def user_authenticate(request):
    username = request.POST.get('username',None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        raise(Http404)
        # Return an 'invalid login' error message.
    return redirect(newQuestions)

def user_register(request):
    username = request.POST.get('username',None)
    email = request.POST.get('email',None)
    real_name = request.POST.get('real_name',None)
    password = request.POST.get('password',None)
    password_repeat = request.POST.get('password_repeat',None)
    if password != password_repeat:
        pass
    avatar = request.POST.get('avatar',None)
    user = User.objects.create_user(username, email, password)
    user.first_name = real_name
    user.upload = avatar
    user.save()
    login(request,user)
    return redirect(newQuestions)

def user_logout(request):
    logout(request)
    return redirect(user_login)

def signup(request):
    return render(request, 'signup.html', {})


def ask(request):
    return render(request, 'ask.html', {})

@login_required
def submit_question(request):
    question = Question(title = request.POST.get('title', None))
    question.author = request.user
    question.text = request.POST.get('text',None)
    question.save()
    tags = request.POST.get('tags',None).split(",")
    for tag_title in tags:
        try:
            tag = Tag.objects.get(title=tag_title)
        except Tag.DoesNotExist:
            tag = Tag(title=tag_title)
            tag.save()
        question.tags.add(tag)
    return redirect('question_by_id', question_id=question.pk)

@login_required
def submit_answer(request):
    answer = Answer(text = request.POST.get('text', None), author = request.user, question = Question.objects.get(pk=request.POST.get('question')))
    answer.save()
    return redirect('question_by_id',question_id=answer.question.pk)

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    pageNumber = request.GET.get('page')

    try:
        page = paginator.page(pageNumber)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    start = max(1, page.number - 3)
    end = min(page.paginator.num_pages + 1, start + 6)
    start = end - 6 - 1
    pages = range(1, page.paginator.num_pages + 1)[start:end]
    return page, pages
