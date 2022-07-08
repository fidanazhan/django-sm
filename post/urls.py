from django.urls import path 
from . views import (PostListView, PostDetailView, PostLikeView,
                     PostCommentView, PostShareView, 

                     CommentShareView, CommentLikeView, 
                     CommentReplyView, CommentReplySubmitView,
                     
                     BookmarkView, BookmarkPostView, BookmarkCommentView)

urlpatterns = [
    path('home/', PostListView.as_view(), name='post-list'),
    path('status/<str:user>/<uuid:pk>', PostDetailView.as_view(), name='post-detail'),
    path('status/<str:user>/<int:pk>/', CommentReplyView.as_view(), name='comment-detail'),
    path('i/bookmark/', BookmarkView.as_view(), name='bookmark-detail'),
    # path('i/notification/', NotificationView.as_view(), name='notification-detail'),

    path('<uuid:pk>/post/like', PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/comment/like', CommentLikeView.as_view(), name='comment-like'),

    path('<uuid:pk>/post/share', PostShareView.as_view(), name='post-share'),
    path('<int:pk>/comment/share', CommentShareView.as_view(), name='comment-share'),

    path('<uuid:pk>/post/comment', PostCommentView.as_view(), name='post-comment-api'),
    path('<int:pk>/comment/reply', CommentReplySubmitView.as_view(), name='comment-reply'),

    path('<uuid:pk>/post/bookmark', BookmarkPostView.as_view(), name='bookmark-post'),
    path('<int:pk>/comment/bookmark', BookmarkCommentView.as_view(), name='bookmark-comment'),


    
]