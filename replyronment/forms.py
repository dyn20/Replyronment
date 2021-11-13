from typing import Generic
from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import CommentForum, Profile, Comment, ForumPost
from replyronment import models

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30,required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Tên đăng nhập'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'Nhập lại mật khẩu'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields=['title','body','tag']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-cmt', 'rows': 5,'Placeholder':'Nhập bình luận...'}))
    class Meta:
        model = Comment
        fields = ['body']

class CommentForumForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-cmt', 'rows': 5,'Placeholder':'Nhập bình luận...'}))
    class Meta:
        model = CommentForum
        fields = ['body']
