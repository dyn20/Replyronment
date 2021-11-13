from django.urls import path
from django.urls.resolvers import URLPattern
from django.contrib.auth import views as auth_views
from . import views
urlpatterns =[
    path('',views.index),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name="html/login.html"), name="login"),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('Profile/',views.profile,name='profile'),
    path('LandingPage/',views.landingpage,name='LandingPage'),
    path('Post', views.postlist, name='postlist'),
    path('Post/<slug:slug>/', views.postdetail, name='post_detail'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('Forum/',views.post_forum,name='forum'),
    path('Forum/createpost/',views.createpost,name='createpost'),
    path('Forum/<slug:slug>/', views.forum_postdetail, name='forumpostdetail'),
    path('Forum/comment/reply',views.reply_pageforum,name='reply_page_forum'),
]