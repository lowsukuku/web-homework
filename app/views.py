from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from app.models import Question, Answer, Tag
from random import randint
from datetime import datetime
from time import time
from django.urls import reverse

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


def login(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def ask(request):
    return render(request, 'ask.html', {})


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
