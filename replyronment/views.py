from django.contrib.auth.models import User
from django.db.models import Count, query
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UpdateUserForm, UpdateProfileForm, CommentForm, ForumPostForm, CommentForumForm, addQuestionFor
from django.views import generic
from .models import Post, Comment, ForumPost, CommentForum, Profile, QuesModel
from taggit.models import Tag
from django.db.models import Count, Q

# Create your views here.
def index(request):
    return render(request,'html/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username') 
            messages.success(request, f'Account created for {username}!') 
            return HttpResponseRedirect('/login') 
    else:
       form = RegistrationForm()
    return render(request, 'html/register.html', {'form': form})

@login_required(login_url='/login')
def profile(request):
    return render(request, 'html/profile.html')   

@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            #messages.success(request, f'Your account has been updated!')
            return HttpResponseRedirect('/Profile') 

    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'html/profilefake.html', context)

def landingpage(request):
    user = request.user
    return render(request,'html/LandingPage.html',{'user':user})
def aboutus(request):
    return render(request,'html/about.html')
#generic.ListView
def postlist(request):
    query = request.GET.get("q")
    if query:
        data ={'Posts':Post.objects.filter(Q(title__icontains=query) | Q(tag__name__icontains=query)).distinct().order_by("-date")}
    else:
        data ={'Posts':Post.objects.all().order_by("-date")}
    return render(request,'html/postlist.html',data)

def postdetail(request,slug):
    post = Post.objects.get(slug=slug)
    post_tags_ids = post.tag.values_list('id', flat=True)
    similar_posts = Post.published.filter(tag__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags','-date')[:6]
    comments = post.comments.filter(active=True)
    cmt_form = CommentForm(request.POST)
    new_cmt=None
    if cmt_form.is_valid():
        new_cmt=cmt_form.save(commit=False)
        new_cmt.post = post
        new_cmt.name = request.user
        new_cmt.save()
    else:
        cmt_form = CommentForm()
    return render(request, 'html/postdetail.html',{'post':post,'comments':comments,'comment_form':cmt_form,'similar_posts':similar_posts})

# handling reply, reply view
def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)
    
            reply.post = Post(id=post_id)
            reply.name = request.user
            reply.parent = Comment(id=parent_id)
            reply.save()

            return HttpResponseRedirect(post_url+'#'+str(reply.id))
    return HttpResponseRedirect("/")
    
@login_required(login_url='/login')
def post_forum(request):
    query = request.GET.get("q")
    if query:
        data ={'Posts':ForumPost.objects.filter(Q(title__icontains=query) | Q(tag__name__icontains=query)).distinct().order_by("-date")}
    else:
        data ={'Posts':ForumPost.objects.all().order_by("-date")}
    return render(request,'html/forum.html',data)

@login_required(login_url='/login')
def createpost(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            #new_post.tag.add(request.POST['tag'])
            #new_post.save()
            #
        form = ForumPostForm(instance=new_post,data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/Forum')
    else:
        form = ForumPostForm()
    return render(request,'html/forum_post.html',{'post_form':form})

@login_required(login_url='/login')
def forum_postdetail(request,slug):
    post_forum = ForumPost.objects.get(slug=slug)
    comments = post_forum.forum_comments.filter(active=True)
    cmt_form = CommentForumForm(request.POST)
    new_cmt=None
    if cmt_form.is_valid():
        new_cmt=cmt_form.save(commit=False)
        new_cmt.forum_post = post_forum
        new_cmt.owner = request.user
        new_cmt.save()
    else:
        cmt_form = CommentForumForm()
    return render(request, 'html/forum_postdetail.html',{'post':post_forum,'comments':comments,'comment_form':cmt_form})

@login_required(login_url='/login')
def reply_pageforum(request):
    if request.method == "POST":
        form = CommentForumForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            reply = form.save(commit=False)
    
            reply.forum_post = ForumPost(id=post_id)
            reply.owner = request.user
            reply.parent = CommentForum(id=parent_id)
            reply.save()

            return HttpResponseRedirect(post_url+'#'+str(reply.id))
    return HttpResponseRedirect("/")

@login_required(login_url='/login')
def mypost(request):
    Posts = ForumPost.objects.all().filter(author=request.user).order_by("-date")
    return render(request,'html/mypost.html',{'Posts':Posts})

@login_required(login_url='/login')
def editpost(request,slug):
    post = ForumPost.objects.get(slug=slug)
    if(post.author==request.user or request.user.is_staff):
        if request.method == 'POST':
            form = ForumPostForm(instance=post,data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/Forum/'+slug)
        else:
            form = ForumPostForm(instance=post)
        return render(request,'html/editpost.html',{'post':post,'form':form}) 
    else:
        return HttpResponseRedirect('/Forum/'+slug)

@login_required(login_url='/login')
def deletepost(request,slug):
    post_to_delete = ForumPost.objects.get(slug=slug)
    if post_to_delete != None:
        post_to_delete.delete()
    return HttpResponseRedirect('/Forum')

@login_required(login_url='/login')
def playquiz(request):
    profile = Profile.objects.get(user=request.user)
    incorrectques = profile.Incorrect_ques.all()
    correctques = profile.Correct_ques.all()
    answeredques = profile.answered_ques.all()
    allquestions = QuesModel.objects.all()
    correctidlist = list()
    for ques in correctques:
        correctidlist.append(ques.id)
    startquestions = QuesModel.objects.filter(~Q(id__in=correctidlist))
    questions = startquestions
    query = request.GET.get("q")
    if query=='tat-ca-cau-hoi':
        questions=allquestions
    if query=="tra-loi-dung":
        questions =correctques
    if query=='tra-loi-sai':
        questions=incorrectques
    if query=='bat-dau-quiz':
        questions = startquestions
    if request.method == 'POST':
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            profile.answered_ques.add(q)
            total +=1
            print("cau hoi",request.POST.get(q.question))
            if q.ans == request.POST.get(q.question):
                score += q.point
                correct +=1
                profile.Correct_ques.add(q)
            else:
                wrong +=1
                profile.Incorrect_ques.add(q)
        profile.score += score
        profile.save()
        context = {
            'score':score,
            'correct': correct,
            'wrong': wrong,
            'total': total
        }
        return render(request,'html/quizresult.html',context)
    else:
        query = request.GET.get("q")
        if query=='tat-ca-cau-hoi':
            questions=allquestions
        if query=="tra-loi-dung":
            questions =correctques
        if query=='tra-loi-sai':
            questions=incorrectques
        if query=='bat-dau-quiz':
            questions = startquestions
        return render(request,'html/quizhome.html', {'questions': questions})

def scoreboard(request):
    users = Profile.objects.all().order_by("-score")
    return render(request,'html/scoreboard.html',{'users':users})


