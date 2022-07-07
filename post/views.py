from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.views import View
#from django.views.generic.edit 

from .forms import PostForm, CommentForm

from . models import Post, Like, Comment, Share

from itertools import chain

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        posts = Post.objects.all()
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

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, user, pk, *args, **kwargs):

        post = Post.objects.get(pk=pk)
                
        comment_form = CommentForm()
        comments = Comment.objects.filter(commented_post=post, level=0)
        comments_next_level = comments.count()
        
        comment_list = list(comments.order_by('-created_on'))

        comment_counts_list = []

        for comment in comments:
            comment_counts_list.append(comment.get_descendants().filter(level=1).count())

        mylist = zip(comment_list, comment_counts_list)

        context = {
            'post' : post, 
            'mylist' : mylist,
            'comments_level_1_count' : comments_next_level,
            'form' : comment_form
        }

        return render(request, 'post_detail.html', context)

class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post_pk = post.pk

        comment_form = CommentForm(request.POST)
        print(post_pk)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commented_post = post
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
       
        return redirect('post-detail', user=post.user.username, pk=post_pk)

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
            
            if liked:
                liked_post = Like.objects.filter(user=user, liked_post=post)
                liked_post.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next)

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
            
            if shared:
                shared_post = Share.objects.filter(user=user, shared_post=post)
                shared_post.delete()

        next = request.POST.get('next', '')
        return HttpResponseRedirect(next) 

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
            
            if liked:
                liked_comment = Like.objects.filter(user=user, liked_comment=comment)
                liked_comment.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next)

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
            
            if shared:
                shared_comment = Share.objects.filter(user=user, shared_comment=comment)
                shared_comment.delete()

        next = request.POST.get('next', '')
        print(next)
        return HttpResponseRedirect(next) 

















