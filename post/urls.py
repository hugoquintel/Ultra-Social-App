from post.views import index, NewPost, PostDetails, tags, like, favorite, DeletePost, likeIndex, favoriteIndex
# from comment.views import Comment
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', NewPost, name='newpost'),
    path('<uuid:post_id>/', PostDetails, name='postdetails'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    # path('<uuid:post_id>/comment', CommentPost, name='comment'),
    path('<uuid:post_id>/like', like, name='postlike'),
    path('<uuid:post_id>/likeindex', likeIndex, name='like-index'),
    path('<uuid:post_id>/favorite',favorite, name='postfavorite'),
    path('<uuid:post_id>/favoriteindex',favoriteIndex, name='favorite-index'),
    path('<uuid:post_id>/delete', DeletePost, name='delete-post'),
]