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

class ProfileView(View):
    def get(self, request, user, *args, **kwargs):

        user_profile = get_object_or_404(Profile, user_obj__username=user)
        # print(user_profile)
        user_id = user_profile.user_obj.id
        # print(user_id)
        user_post = Post.objects.filter(user__pk=user_id).order_by('-created_on')
        user_post_liked = Like.objects.filter(user__pk=user_id).order_by('-created_on')

        context = {
            'user_profile' : user_profile,
            'user_post' : user_post,
            'user_post_liked' : user_post_liked
        }

        return render(request, 'profile.html', context)