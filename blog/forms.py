from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Comment, Post

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password1','password2']

	def __init__(self,*args, **kwargs):
		super(UserRegisterForm, self).__init__(*args,**kwargs)
		for fieldname in ['username','first_name','last_name','email','password1','password2']:
			self.fields[fieldname].help_text = None



class UserLoginForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields =['name','email','body']

class PostForm(forms.Form):
	title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'id':'titleField','placeholder':'Title of the Post...'}))
	body = forms.CharField(widget=forms.Textarea(attrs={'id':'bodyField'}))
	html = forms.CharField(widget=forms.Textarea(attrs={'id':'htmlField'}))
	tags = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'id':'maintag'}))
	rtags = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'id':'rtag'}))