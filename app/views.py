from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from random import randint
from datetime import datetime
from time import time

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

questions = {
    i: {'id': i, 'title': f'question {i}',
        'text': f'Hello world! This is my question {i}', 'rating': randint(-100, 100), 'tags': [
            tags[randint(0, 99)]
            for j in range(randint(1, 5))
        ], 'creator': user, 'creationTime': datetime.now(), 'answers': answers, 'answersCount': len(answers)}
    for i in range(100)
}


def newQuestions(request):
    page, pages = paginate(list(questions.values()), request, 10)
    return render(request, 'index.html', {
        'questions': page,
        'pages': pages
    })


def listByTag(request, tag):
    questionsByTag = {}
    for i in range(100):
        a = questions[i].get('tags')
        if (tag in a):
            questionsByTag[i] = questions[i]
    page, pages = paginate(list(questionsByTag.values()), request, 10)
    return render(request, 'index.html', {
        'questions': page,
        'pages': pages
    })


def questionById(request, question_id):
    if (question_id not in questions):
        raise Http404
    return render(request, 'question.html', {
        'question': questions.get(question_id),
        'answers': range(10)
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
