from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Post
from django.contrib.auth import login, authenticate
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class HomeView(LoginView):
    # redirect_authenticated_user = True
    template_name= 'base/home.html'

    def get_success_url(self):
        user = self.request.user
        messages.success(self.request, f'Logged in as {user}!')
        return reverse_lazy('base-home')
    
    def form_invalid(self, form: AuthenticationForm):
        messages.error(self.request, 'Invalid username or password')

        return self.render_to_response(self.get_context_data(form=form))




class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 6


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list_user.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Any]:
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']        

    def form_valid(self, form: BaseModelForm):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_update.html'       

    def form_valid(self, form: BaseModelForm):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated !!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def get_success_url(self):
        post = self.get_object()
        post_title = post.title
        messages.warning(self.request, f'{post_title} had been deleted!!')
        return reverse_lazy('blog-home')