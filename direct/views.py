from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from direct.models import Message
from post.models import Tag


from django.db.models import Q # query ultility
from django.core.paginator import Paginator
# Create your views here.

@login_required
def Inbox(request):
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
	}

	template = loader.get_template('direct/direct.html')

	return HttpResponse(template.render(context, request))

@login_required
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)

	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
	}

	template = loader.get_template('direct/direct.html')

	return HttpResponse(template.render(context, request))

@login_required
def SendDirect(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')

	if body.strip() == "":
		return redirect(reverse('directs', args=[to_user_username]))

	if request.method == 'POST':
		try:
			to_user = User.objects.get(username=to_user_username)
		except User.DoesNotExist:
			return redirect('inbox')
		Message.send_message(from_user, to_user, body)
		return redirect('inbox')
	
	else:
		HttpResponseBadRequest()

@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query)).exclude(username=request.user.username)

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('direct/search_user.html')
	
	return HttpResponse(template.render(context, request))


@login_required
def NewConversation(request, username):
	from_user = request.user
	body = 'Hello!'

	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('usersearch')
	
	# Prevent the user from DMing themselves
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	else:
		pass
	
	return redirect('inbox')

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count': directs_count}

