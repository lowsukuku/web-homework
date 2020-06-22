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
from app.forms import AnswerForm, AuthorisationForm, QuestionForm, RegistrationForm

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
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author = request.user
                answer.question = question
                answer.save()
                page, pages = paginate(Answer.objects.filter(question=question_id), request, 10)
                page = page.paginator.page(page.paginator.num_pages)
        else:
            page, pages = paginate(Answer.objects.filter(question=question_id), request, 10)
        form = AnswerForm()
        return render(request, 'question.html', {
            'question': question,
            'answers': page,
            'pages': pages,
            'form' : form
        })
    page, pages = paginate(Answer.objects.filter(question=question_id), request, 10)
    return render(request, 'question.html', {
        'question': question,
        'answers': page,
        'pages': pages
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect(newQuestions)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(newQuestions)
    form = RegistrationForm()  
    return render(request, 'signup.html', {'form':form})

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST) 
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_by_id', question_id=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})

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
