"""projectA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name='blog'

urlpatterns = [
    path('',views.post_list, name ='home'),
    path('tag/<slug:tag_slug>/',views.post_list,name='home_by_tag'),                                    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html', extra_context={'title':'Login'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html', extra_context={'title':'Logout'}), name='logout'),
    path('<int:year>/<int:month>/<int:day>/<slug:Post>/',views.post_detail,name='post_detail'),
    path('Post/',views.addPost,name='add_Post'),
    path('account/<str:username>',views.account,name='account'),
    path('<int:year>/<int:month>/<int:day>/<slug:Post>/edit/',views.editPost,name='post_edit'),
    path('<int:year>/<int:month>/<int:day>/<slug:Post>/delete/',views.deletePost,name='post_delete'),
    ]