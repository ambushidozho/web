"""askme_belokopytov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from askme import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index , name = "index"),
    path('admin/', admin.site.urls),
    path('question/<int:question_id>/', views.question, name = "question"),
    path('ask/', views.ask , name = "ask"),
    path('login/', views.log_in,name = "login"),
    path('signup/', views.signup, name = "signup"),
    path('hot/', views.hot, name = "hot"),
    path('tag/<slug:tagname>/', views.tag, name = "tag"),
    path('logout/', views.log_out, name = "log_out"),
    path('profile/edit/', views.settings, name = "edit"),
    path("vote_up/", views.vote_up, name = "vote_up"),
    path("vote_up_for_answer/", views.vote_up_for_answer, name = "vote_up_for_answer"),
    path("correct/", views.correct, name = "correct")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
