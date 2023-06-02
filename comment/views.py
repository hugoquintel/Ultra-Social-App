# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from django.template import loader
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# # Create your views here.
# from post.models import Post
# from comment.forms import CommentForm

# def Comment(request, post_id):

#     post = get_object_or_404(Post, id=post_id)
#     user = request.user

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comments = form.save(commit=False)
#             comments.post = post
#             comments.user = user
#             comments.save()
#             return redirect(reverse('postdetails', args=[post_id]))
#     else:
#         form = CommentForm()

#     template = loader.get_template('post_detail.html')
    
#     context = {
#         'form': form,
#     }

#     return HttpResponse(template.render(context, request))
