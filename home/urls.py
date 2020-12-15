from django.contrib import admin
from django.urls import path
from home import views
from blog.views import blogPost


urlpatterns = [
    path('', views.home,name="home"),
    path('contact', views.contact,name="contact"),
    path('about', views.about,name="about"),
    path('search',views.search,name="search"),
    path('signup',views.handleSignup,name="signup"),
    path('login',views.handleLogin,name="handleLogin"),
    path('logout',views.handleLogout,name="handleLogout"),
    path('<str:slug>',blogPost,name="blogPost"),
    path('delete/<int:id>',views.delete,name='delete'),
    path('update/<int:id>',views.update,name='update'),
    
]
