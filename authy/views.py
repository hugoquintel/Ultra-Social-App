from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login, authenticate

from authy.models import Profile
from django.template import loader
from django.http import HttpResponse, JsonResponse

from django.core.paginator import Paginator
from django.urls import resolve, reverse
from django.db import transaction

from post.models import Post, Follow, Stream, Tag, Follow
from django.db.models import Q # query ultility

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')
	else:
		posts = profile.favorites.all()

	# Profile info stats
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).exclude(following=user).count()
	followers_count = Follow.objects.filter(following=user).exclude(follower=user).count()

	# Check follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile': profile,
		'url_name': url_name,
		'posts_count': posts_count,
		'following_count': following_count,
		'followers_count': followers_count,
		'follow_status': follow_status,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = User.objects.create_user(username=username, email=email, password=password)
			Follow.objects.create(follower=user, following=user)
			new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
			login(request, new_user)
			return redirect(reverse('edit-profile'))
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)



def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)

		if form.is_valid():
			picture = form.cleaned_data.get('picture')
			background = form.cleaned_data.get('backgroundimage')

			profile.picture = profile.picture
			profile.backgroundimage = profile.backgroundimage
			if picture is not None:
				profile.picture = picture

			if background is not None:
				profile.backgroundimage = background

			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			# return redirect('index')
	else:
		form = EditProfileForm(initial={'first_name': profile.first_name,
				  						'last_name': profile.last_name,
										'location': profile.location,
										'url': profile.url,
										'profile_info': profile.profile_info})
	
	context = {
		'form':form,
		'profile': profile,
	}

	return render(request, 'edit_profile.html', context)

@login_required
def follow(request, username, option):
	user = request.user
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)
		

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:10]

			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=user, date=post.posted, following=following)
					stream.save()

		followers_count = Follow.objects.filter(following=following).exclude(follower=following).count()
		return JsonResponse({'option': option, 'followers_count': followers_count, 'user': following.username})
		# return redirect(reverse('profile', args=[username]))
	
	except User.DoesNotExist:
		return redirect(reverse('profile', args=[username]))
	
	




@login_required
def Explore(request):
	query = request.GET.get("q")
	followings = Follow.objects.filter(follower=request.user).exclude(following=request.user)

	users_following = [following.following.username for following in followings]

	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query)).exclude(username=request.user.username)
		tags = Tag.objects.filter(Q(title__icontains=query))
		

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users_following': users_following, 
				'users': users_paginator,
				'tags': tags,
			}
	
	template = loader.get_template('explore.html')
	
	return HttpResponse(template.render(context, request))


def Direct(request):
	return redirect(reverse('login'))


def About(request):
	return render(request, 'about.html', {})

def Contact(request):
	return render(request, 'contact.html', {})