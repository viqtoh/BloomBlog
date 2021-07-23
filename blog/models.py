from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import auth
from taggit.managers import TaggableManager
from taggit.models import Tag

# Create your models here.

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
	STATUS_CHOICES =(('draft','Draft'),('published','Published'),)
	title=models.CharField(max_length = 250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_poosts')
	body = models.TextField()
	html = models.TextField(default=body)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
	objects = models.Manager()
	edited = models.BooleanField(default=0)
	published = PublishedManager()
	tags = TaggableManager()

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return (str(self.title)+' '+str(self.publish))

	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

	def get_absolute_url_edit(self):
		return reverse('blog:post_edit',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

	def get_absolute_url_delete(self):
		return reverse('blog:post_delete',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])


class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return f'Comment by { self.name } on { self.post }'

def get_url_user(self):
	return reverse('blog:account',args=[self.username])

def getName(self):
	return (self.name)

User.add_to_class('get_url_user',get_url_user)
Tag.add_to_class('getName',getName)
