from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required

# Create your views here.
from post.models import Post, Stream, Tag, Likes, PostFileContent, Follow
from authy.models import Profile
from comment.models import Comment
from stories.models import Story, StoryStream

from post.forms import NewPostForm
from comment.forms import CommentForm
import json

@login_required
def index(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Stream.objects.filter(user=user)
    stories = StoryStream.objects.filter(user=user)
    

    user_likes = Likes.objects.filter(user=user)
    user_favorites = Profile.objects.get(user=user).favorites.all()
    user_liked_post_id = [user_like.post.id for user_like in user_likes]
    user_favorites_post_id = [user_favorite.id for user_favorite in user_favorites]
    
    group_ids = [post.post_id for post in posts]

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('index.html')

    followings = Follow.objects.filter(follower=user).exclude(following=user)
    users_following_id = [following.following.id for following in followings]
    users_following = Profile.objects.filter(id__in=users_following_id).all()


    context = {
        'users_following': users_following,
        'profile': profile,
        'stories': stories,
        'post_items': post_items,
        'user_liked_post_id': user_liked_post_id,
        'user_favorites_post_id': user_favorites_post_id
    }

    return HttpResponse(template.render(context, request))

@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    favorited = False
    liked = Likes.objects.filter(user=user, post=post).count() # kiểm tra xem user có like 1 post và đổi màu nút like

    # comment
    comments = Comment.objects.filter(post=post).order_by('date')


    # comment form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.post = post
            comments.user = user
            comments.save()

            # return JsonResponse({'post': comments.body})
            return redirect(reverse('postdetails', args=[post_id]))
    else:
        form = CommentForm()

    # đổi màu nút favorite
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        if profile.favorites.filter(id=post_id).exists():
            favorited = True

            


    template = loader.get_template('post_detail.html')

    context = {
        'post': post,
        'favorited': favorited,
        'liked': liked,
        'form': form,
        'comments': comments,
    }

    return HttpResponse(template.render(context, request))


@login_required
def DeletePost(request, post_id):
    user = request.user
    PostFileContent.objects.filter(user=user, post_id=post_id).delete()
    Post.objects.filter(id=post_id, user=user).delete()
    return redirect(reverse('profile', args=[user]))


@login_required
def NewPost(request):
    user = request.user
    tags_objs = []
    files_objs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag) # Tự tạo title hoặc tự tạo (cách tags hoạt động)
                tags_objs.append(t)

            p = Post.objects.create(caption=caption, user=user)
            for file in files:
                file_instance = PostFileContent(file=file, user=user, post = p)
                file_instance.save()
                files_objs.append(file_instance)

            p.picture = files[0]
            p.tags.set(tags_objs)
            p.content.set(files_objs)
            p.save()
            return redirect('index')   
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)
    

@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('tag.html')

    context = {
        'posts': posts,
        'tag': tag
    }

    return HttpResponse(template.render(context, request))

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

     
    liked = Likes.objects.filter(user=user, post=post).count()
    # like 1 post
    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes += 1

    # bỏ like 1 post
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
        
    liked = Likes.objects.filter(user=user, post=post).count()
    post.likes = current_likes
    post.save()

    return JsonResponse({"current_likes": current_likes, "liked": liked})
    # return redirect(reverse('postdetails', args=[post_id]))

@login_required
def likeIndex(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post).count() 

    # like 1 post
    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes += 1

    # bỏ like 1 post
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1

    post.likes = current_likes
    post.save()
    
    return JsonResponse({"current_likes": current_likes, "liked": liked})
    # return redirect(reverse('index'))


@login_required
def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    

    #giống logic like phía trên
    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    
    else:
        profile.favorites.add(post)

    favorited = profile.favorites.filter(id=post_id).exists()

    return JsonResponse({"favorited": favorited})

@login_required
def favoriteIndex(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    #giống logic like phía trên
    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    
    else:
        profile.favorites.add(post)

    favorited = profile.favorites.filter(id=post_id).exists()

    return JsonResponse({"favorited": favorited})
    # return redirect(reverse('index'))

# @login_required
# def CommentPost(request, post_id):

#     post = get_object_or_404(Post, id=post_id)
#     user = request.user

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comments = form.save(commit=False)
#             comments.post = post
#             comments.user = user
#             comments.save()
#             return JsonResponse({'post': 1})
#             return redirect(reverse('postdetails', args=[post_id]))
#     else:
#         form = CommentForm()
        


#     return JsonResponse({"favorited": form})
