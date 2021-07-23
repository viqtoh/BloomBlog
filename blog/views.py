from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm,UserLoginForm, CommentForm, PostForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import inspect, json
from taggit.models import Tag
from django.db.models import Count



# Create yout functions here

def getPostFromUrl(PostUrl):
	Inipost=PostUrl
	postNum=len(Inipost)
	a=0
	b=0
	c=0
	date=''
	while(b<4):
		if(Inipost[a]!='/'):
			if(a>0):
				date+=Inipost[a]
				c+=1
			a+=1

		else:
			if(c<2 and c>0):
				datenum=len(date)-1
				iniDate=date[datenum]
				ini=''
				d=0
				while(d<datenum):
					ini+=date[d]
					d+=1
				date=ini
				date+='0'
				date+=iniDate
			if(a>0 and b<3):
				date+='-'
			b+=1
			a+=1
			c=0
	post=str(Inipost[a])
	a+=1
	while (a<postNum-1):
			post+=str(Inipost[a])
			a+=1
	return(Post.objects.filter(slug=post,publish__startswith=date).first())

def getSlug(test):
    initest=''
    lnTest= len(test)
    a=0
    while(a<lnTest):
        ini=test[a]
        if(ini==' '):
        	initest+='-'
        	a+=1
        else:
            initest+=ini
            a+=1
    return(initest)


# Create your views here.



def register(request):
	if request.method == 'POST':
		form= UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}! Please login...')
			return redirect('blog:login')

	else:
	    form = UserRegisterForm()
	return render(request, 'blog/register.html',{'form':form,'title':'Register'})

def login(request):
	form = UserLoginForm()
	return render(request,'blog/login.html',{'form':form,'title':'Login'})


def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts= paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,'blog/Post/list.html',{'page': page,'posts':posts,'title':'Home','comment':Comment,'tag': tag})

def post_detail(request, *args, **kwargs):
    pathUrl=request.path
    post=getPostFromUrl(pathUrl)
    Tcomments = Comment.objects.filter(post=post,active=True).all()
    object_list = Comment.objects.filter(post=post,active=True).all()
    paginator = Paginator(object_list, 1)
    page = request.GET.get('page')
    try:
    	comments= paginator.page(page)
    except PageNotAnInteger:
    	comments = paginator.page(1)
    except EmptyPage:
    	comments = paginator.page(paginator.num_pages)
    #Creating the comment form
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.save()
    else:
    	comment_form=CommentForm()
    #list of similar posts
    post_tags_ids = Post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts =similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'blog/Post/detail.html',{'post': post,'comments': comments,'Tcomments':Tcomments,'page':page, 'new_comment':new_comment,'comment_form':comment_form,'PostUrl': pathUrl,'similar_posts': similar_posts})



def addPost(request):
	form = PostForm(request.POST)
	tagsq = []
	for tag in Tag.objects.all():
		tagsq=tagsq+[str(tag.getName()),]
	tags=''
	for i in tagsq:
		tags = tags + i +'*'
	print(tags)
	tags = json.dumps(tags)
	if form.is_valid():
		nwtitle=form.cleaned_data.get('title')
		nwbody=form.cleaned_data.get('body')
		nwhtml=form.cleaned_data.get('html')
		nwtags=form.cleaned_data.get('tags')
		nwauthor= request.user
		post = Post(title=nwtitle,body=nwbody,html=nwhtml,author=nwauthor)
		post.slug=getSlug(post.title)
		postTags = nwtags.split(',')
		post.edited = 0
		post.save()
		if (postTags != ['']):
			for ptag in postTags:
				post.tags.add(ptag)
		post.save()
		messages.success(request,f'New Post Added successfully')
		form=PostForm()
		return redirect(post)
	else:
		form = PostForm()
	return render(request,'blog/addPost.html',{'title':'Add Post','form':form,'tags':tags,'tagsq':tagsq})

def deletePost(request, *args, **kwargs):
	inipath = request.path
	#Getting Path from url
	path=''
	i=0
	j=len(inipath)-7
	while(i<j):
		path+=inipath[i]
		i+=1
	post = getPostFromUrl(path)
	if request.user == post.author:
		messages.success(request,f'Post: \'{post.title}\' has been successfully deleted...')
		post.delete()
		return redirect('blog:home')
	else:
		messages.warning(request,f'You are not authorised to delete this post...')
		return redirect(post)


def editPost(request, *args, **kwargs):
	form = PostForm(request.POST)
	tagsq = []
	for tag in Tag.objects.all():
		tagsq=tagsq+[str(tag.getName()),]
	tags=''
	for i in tagsq:
		tags = tags + i +'*'
	tags = json.dumps(tags)
	inipath = request.path
	#Getting Path from url
	path=''
	i=0
	j=len(inipath)-5
	while(i<j):
		path+=inipath[i]
		i+=1
	
	post = getPostFromUrl(path)
	if (request.user == post.author):
		postBody=json.dumps(post.body)
		postTitle=json.dumps(post.title)
		postTags=post.tags.all()
		postT= []
		for tag in postTags:
			postT = postT +[str(tag.getName()),]
		ptags=''
		for i in postT:
			ptags = ptags + i + '*'
		ptags=json.dumps(ptags)
		if form.is_valid():
			nwtitle=form.cleaned_data.get('title')
			nwbody=form.cleaned_data.get('body')
			nwhtml=form.cleaned_data.get('html')
			nwtags=form.cleaned_data.get('tags')
			nwrtags=form.cleaned_data.get('rtags')
			nwauthor= request.user
			post.title = nwtitle
			post.body = nwbody
			post.html =nwhtml
			post.slug=getSlug(post.title)
			postTags = nwtags.split(',')
			postRtags=nwrtags.split(',')
			post.edited = 1
			if (postTags != ['']):
				for ptag in postTags:
					post.tags.add(ptag)
			print (nwrtags)
			if (postRtags != ['']):
				for ptag in postRtags:
					post.tags.remove(ptag)
			post.save()
			messages.success(request,f'Post Successfully Edited')
			form=PostForm()
			posturl = post.get_absolute_url
			return redirect(post)
		else:
			form = PostForm()

		context = {
		'title':'Add Post',
		'form':form,
		'tags':tags,
		'ptags':ptags,
		'tagsq':tagsq,
		'postBody':postBody,
		'postTitle':postTitle,
		'post':post
		}
		return render(request,'blog/editPost.html',context)
	else:
		messages.warning(request,f'You are not authorised to edit this post...')
		return redirect(post)


def account(request, username):
	Inipost=request.path
	pathUrl=Inipost
	user2 = User.objects.filter(username=username).first()
	#setting up pagination
	object_list = Post.published.filter(author=user2).all()
	paginator = Paginator(object_list, 2)
	page = request.GET.get('page')
	try:
		posts= paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	usrpost = Post.published.filter(author=user2)
	noP= len(usrpost)
	return render(request,'blog/account.html',{'user2':user2,'title':'Account','noP':noP,'page':page,'posts':posts,'PostUrl':pathUrl})