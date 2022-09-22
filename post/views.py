from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
#from django.views.generic.edit 

from .forms import PostForm, CommentForm

from . models import Post, Like, Comment, Share, Bookmark, Notification
from accounts . models import Follow

from django.db.models import Q

from itertools import chain


# ------------------------- POSTS PART -------------------------
# Go to 'home'. Display a list of posts (original post, liked post, shared post, comment post?). 
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        user = request.user

        followers = Follow.objects.filter(follower=user)

        following_list = []

        for follower in followers:
            following_list.append(follower.following)


        # 1 ------ Following's quack ------
        following_posts = Post.objects.filter(user__username__in=following_list).all()
        print(following_posts)
        # ------------------------------------        

        # 2 ------ Following LIKES quack ------
        # 1. Show post that following like but if the post author is request.user, exclude that post
        following_liked_posts= Like.objects.filter(user__username__in=following_list).exclude(Q(liked_post__user__username__contains =
         user) |  Q(liked_comment__user__username__contains = user))
        # ------------------------------------


        # 3 ------ Following SHARE quack 
        # following_shared_posts = Share.objects.filter(user__username__in=following_list).exclude(shared_post__user__username__contains =
        #  user, shared_comment__user__username__contains = user)
        # --------------------------------------

        # 4 ------ Following reply quack/comment ------
        #following_reply_posts = Comment.objects.filter(user__username__in=following_list).all().order_by('-created_on')
        # ------------------------------------

        # 5 ------ Self quack ------
        self_posts = Post.objects.filter(user=user).all()
        # ------------------------------------


        # posts_chain = list(chain(following_posts, self_posts))
        # posts = sorted(posts_chain, key=lambda instance: instance.created_on, reverse=True)

        posts_chain = list(chain(self_posts, 
                              following_posts,
                              following_liked_posts, 
                            #   following_shared_posts
                              ))
        posts = sorted(posts_chain, key=lambda instance: instance.created_on, reverse=True)
        # # posts = sorted(result_1, key=lambda instance: instance.created_on, reverse=True)
        # for post in posts_1:
        #     print(type(post))
        #     print(post)
        #     print(post.user)
        #     print(post.created_on)
        # print(posts_1)
    
        form = PostForm()


        context = {
            'posts' : posts,
            'form' : form,
        }

        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):

        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            form = PostForm()


        return redirect('post-list')

# Go to 'post-detail'. Display a list comment according to the post.pk. The comment list is level 0. Focus on post.
# Get Method 
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, user, pk, *args, **kwargs):

        post = Post.objects.get(pk=pk)
                
        comment_form = CommentForm()
        comments = Comment.objects.filter(commented_post=post, level=0)
        comments_next_level = comments.count()
        
        comment_list = list(comments.order_by('-created_on'))

        comment_counts_list = []

        for comment in comments:
            # comment_counts_list.insert(0, comment.get_descendants().filter(level=1).count())
            comment_counts_list = [comment.get_descendants().filter(level=1).count()] + comment_counts_list

        mylist = zip(comment_list, comment_counts_list)

        context = {
            'post' : post, 
            'mylist' : mylist,
            'comments_level_1_count' : comments_next_level,
            'form' : comment_form
        }

        return render(request, 'post_detail.html', context)

# Comment a post. POST Method.
class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post_pk = post.pk

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commented_post = post
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()

        notification = Notification.objects.create(notification_types = 3, 
                                                   notification_post = post,
                                                    notification_comment = new_comment, 
                                                    sender=request.user, 
                                                    receiver=post.user)
       
        return redirect('post-detail', user=post.user.username, pk=post_pk)

# Like a post. POST Method.
class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        user = request.user
        post = Post.objects.get(pk=pk)
        liked = Like.objects.filter(user=user, liked_post=post)
        post_user = post.user

        print(post_user)

        if user not in post.likes.all():
            post.likes.add(user)
        else:
            post.likes.remove(user)

        if user.is_authenticated:
            if not liked:
                liked_post = Like.objects.create(user=user, liked_post=post)
                notification = Notification.objects.create(notification_types = 1, 
                                                    notification_post = post, 
                                                    sender=request.user, 
                                                    receiver=post.user)
            
            if liked:
                liked_post = Like.objects.filter(user=user, liked_post=post)
                liked_post.delete()

                notification = Notification.objects.filter(notification_types = 1, 
                                                    notification_post = post, 
                                                    sender=request.user, 
                                                    receiver=post.user)
                notification.delete()



        next = request.POST.get('next', '')
        return HttpResponseRedirect(next)

# Share a post. POST Method.
class PostShareView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        shared = Share.objects.filter(user=user, shared_post=post)

        if user not in post.shares.all():
            post.shares.add(user)
        else:
            post.shares.remove(user)

        if user.is_authenticated:
            if not shared:
                shared_post = Share.objects.create(user=user, shared_post=post)
                notification = Notification.objects.create(notification_types = 2, 
                                                    notification_post = post, 
                                                    sender=request.user, 
                                                    receiver=post.user)
            
            if shared:
                shared_post = Share.objects.filter(user=user, shared_post=post)
                shared_post.delete()

                notification = Notification.objects.filter(notification_types = 2, 
                                                    notification_post = post, 
                                                    sender=request.user, 
                                                    receiver=post.user)
                notification.delete()

        next = request.POST.get('next', '')
        return HttpResponseRedirect(next) 

class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    pk_url_kwargs = 'pk'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.updated = True
        new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        pk = self.kwargs["pk"]
        return reverse("post-detail", kwargs={"pk": pk, "user":user})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    pk_url_kwargs = 'pk'
    success_url = '/home/'


# ------------------------- COMMENTS PART -------------------------
# Like a comment. POST Method.
class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        user = request.user
        comment = Comment.objects.get(pk=pk)
        liked = Like.objects.filter(user=user, liked_comment=comment)

        if user not in comment.likes.all():
            comment.likes.add(user)
        else:
            comment.likes.remove(user)

        if user.is_authenticated:
            if not liked:
                liked_comment = Like.objects.create(user=user, liked_comment=comment)
                notification = Notification.objects.create(notification_types = 1, 
                                                    notification_comment = comment, 
                                                    sender=request.user, 
                                                    receiver=comment.user)
            
            if liked:
                liked_comment = Like.objects.filter(user=user, liked_comment=comment)
                liked_comment.delete()

                notification = Notification.objects.filter(notification_types = 1, 
                                                    notification_comment = comment, 
                                                    sender=request.user, 
                                                    receiver=comment.user)
                notification.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next)

# Share a comment. POST Method.
class CommentShareView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        print(pk)
        
        user = request.user
        comment = Comment.objects.get(pk=pk)
        shared = Share.objects.filter(user=user, shared_comment=comment)

        if user not in comment.shares.all():
            comment.shares.add(user)
        else:
            comment.shares.remove(user)

        if user.is_authenticated:
            if not shared:
                shared_comment = Share.objects.create(user=user, shared_comment=comment)
                notification = Notification.objects.create(notification_types = 2, 
                                                    notification_comment = comment, 
                                                    sender=request.user, 
                                                    receiver=comment.user)
            
            if shared:
                shared_comment = Share.objects.filter(user=user, shared_comment=comment)
                shared_comment.delete()

                notification = Notification.objects.filter(notification_types = 2, 
                                                    notification_comment = comment, 
                                                    sender=request.user, 
                                                    receiver=comment.user)
                notification.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next) 

# Go to 'comment-details'. Display a list of comment according to specific post. The comments list is +1 level. 
# Focus on comment. GET Method.
class CommentReplyView(LoginRequiredMixin, View):
    def get(self, request, user, pk, *args, **kwargs):
        
        comment_form = CommentForm()

        # Current comment
        current_comment = Comment.objects.get(pk=pk)
        post = Comment.objects.get(pk=pk).commented_post
        level = Comment.objects.get(pk=pk).level

        # Comment Ancestor
        comments_ancestors = current_comment.get_ancestors()


        # Comment Descendant
        comments_descendants = current_comment.get_descendants().filter(level = level + 1)        

        context = {
            'post' : post, 
            'comments_descendants' : comments_descendants,
            'comment_ancestors' : comments_ancestors,
            'current_comment': current_comment,
            'form' : comment_form
        }

        return render(request, 'comment_detail.html', context)

# Reply to a comment. POST Method.
class CommentReplySubmitView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        current_comment = Comment.objects.get(pk=pk)
        post = Comment.objects.get(pk=pk).commented_post

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment_reply = comment_form.save(commit=False)
            new_comment_reply.commented_post = post
            new_comment_reply.parent = current_comment
            new_comment_reply.user = request.user
            new_comment_reply.save()
            comment_form = CommentForm()

        notification = Notification.objects.create(notification_types = 4, 
                                                    notification_comment = new_comment_reply, 
                                                    sender=request.user, 
                                                    receiver=current_comment.user)

        # return redirect('post-detail', pk=post.pk)
        return redirect('comment-detail', user=current_comment.user.username, pk=current_comment.pk)

class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'
    pk_url_kwargs = 'pk'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.updated = True
        new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        pk = self.kwargs["pk"]

        comment = Comment.objects.get(pk=pk)

        return reverse("comment-detail", kwargs={"pk": pk, "user":user})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    pk_url_kwargs = 'pk'

    def get_success_url(self):
        user = self.request.user
        pk = self.kwargs["pk"]

        comment = Comment.objects.get(pk=pk)

        if comment.parent:
            return reverse("comment-detail", kwargs={"pk": comment.parent.pk, "user":user})
        else:
            return reverse("post-detail", kwargs={"pk": comment.commented_post.pk, "user":user})



# ------------------------- BOOKMARKS PART -------------------------
# Go to 'bookmark'. Bookmark List View. GET Method.
class BookmarkView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        user = request.user
        user_bookmark = Bookmark.objects.filter(user=user).order_by('-created_on')
        print(user_bookmark)

        context = {
            'bookmark_list' : user_bookmark
        }

        return render(request, 'bookmark.html', context)

# Bookmark A Post. POST Method.
class BookmarkPostView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        user = request.user
        post = Post.objects.get(pk=pk)
        bookmark = Bookmark.objects.filter(user=user, bookmark_post=post)

        if user not in post.bookmark.all():
            post.bookmark.add(user)
        else:
            post.bookmark.remove(user)

        if user.is_authenticated:
            if not bookmark:
                liked_post = Bookmark.objects.create(user=user, bookmark_post=post)
            
            if bookmark:
                liked_post = Bookmark.objects.filter(user=user, bookmark_post=post)
                liked_post.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next)

# Bookmark A Comment. POST Method.
class BookmarkCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        user = request.user
        comment = Comment.objects.get(pk=pk)
        bookmark = Bookmark.objects.filter(user=user, bookmark_comment=comment)

        if user not in comment.bookmark.all():
            comment.bookmark.add(user)
        else:
            comment.bookmark.remove(user)

        if user.is_authenticated:
            if not bookmark:
                bookmark_content = Bookmark.objects.create(user=user, bookmark_comment=comment)
            
            if bookmark:
                bookmark_content = Bookmark.objects.filter(user=user, bookmark_comment=comment)
                bookmark_content.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next)

# ------------------------- NOTIFICATION PART -------------------------
# Go to ' notification'. Notification list. GET Method
class NotificationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        notification = Notification.objects.filter(receiver=user).order_by('-created_on')

        context = {
            'notifications' : notification
        }

        return render(request, 'notification.html', context)









