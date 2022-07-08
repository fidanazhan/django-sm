from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User

from accounts.models import Profile, Follow
from post.models import Post, Like

from . forms import SignUpForm

from django.contrib.auth.views import LoginView
from django.views import View

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('post-list')

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()

        context = {
            'form' :form
        }

        return render(request, 'accounts/register.html', context)

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, user, *args, **kwargs):

        requested_user_following = request.user.profile.following.all()

        user_profile = get_object_or_404(Profile, user_obj__username=user)
        user_id = user_profile.user_obj.id
        user_post = Post.objects.filter(user__pk=user_id).order_by('-created_on')
        user_post_liked = Like.objects.filter(user__pk=user_id).order_by('-created_on')

        context = {
            'requested_user_following': requested_user_following,
            'user_profile' : user_profile,
            'user_post' : user_post,
            'user_post_liked' : user_post_liked
        }

        return render(request, 'profile.html', context)

class FollowSubmitView(LoginRequiredMixin, View):
    def post(self, request, following_id, *args, **kwargs):

        user= request.user
        following_user_id = get_object_or_404(Profile, user_obj__id=following_id)
        req_user_profile = user.profile

        #Check whether the user1 already follow user2 
        followed = Follow.objects.filter(follower=user, following=following_user_id.user_obj)

        if following_user_id.user_obj in req_user_profile.following.all():
            req_user_profile.following.remove(following_user_id.user_obj)
        else:
            req_user_profile.following.add(following_user_id.user_obj)
        
        if user.is_authenticated:
            if not followed:
                follow_obj = Follow.objects.create(follower=user, following=following_user_id.user_obj)
            
            if followed:
                follow_obj = Follow.objects.filter(follower=user, following=following_user_id.user_obj)
                follow_obj.delete()


        return redirect('profile', user=following_user_id.user_obj.username)
