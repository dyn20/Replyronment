from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils.text import slugify 

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    slug = models.SlugField(max_length=200, unique=True,default='')
    title = models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Author')
    body = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='featured_image')
    tag = TaggableManager()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager()
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.slug])
    def getmonth(self):
        return self.date.strftime('%B')
    def getday(self):
        return self.date.strftime('%d')

class ForumPost(models.Model):
    slug = models.SlugField(max_length=200, unique=True,default='',null=True)
    title = models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='anonymous')
    body = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)
    tag = TaggableManager()
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return self.title
    def get_comments(self):
        return self.forum_comments.filter(parent=None).filter(active=True)
    def get_absolute_url(self):
        return reverse('forumpostdetail',args=[self.slug])
    def save(self, *args, **kwargs):
        self.slug = slugify(self.author.username) + '-' + slugify(self.title)
        super(ForumPost, self).save(*args, **kwargs)

class UserPost(models.Model):
    user_id = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=100)
    body = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='earth.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'    

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='User')
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

class CommentForum(models.Model):
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='forum_comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='forum_comments')
    parent =models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return self.body
    def get_comments(self):
        return CommentForum.objects.filter(parent=self).filter(active=True)
