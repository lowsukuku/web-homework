"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from app import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.newQuestions, name='new_questions'),
    path('hot/', views.hotQuestions, name='hot_questions'),
    path('tag/<tag>/', views.listByTag, name='list_by_tag'),
    path('question/<int:question_id>/',
         views.questionById, name='question_by_id'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', LoginView.as_view(template_name='login.html',redirect_authenticated_user=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ask/', views.ask, name='ask'),
    path('admin/', admin.site.urls)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
