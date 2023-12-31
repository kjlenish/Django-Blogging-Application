from django.urls import path, include
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, HomeView, UserPostListView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='base-home'),
    path('blog/', PostListView.as_view(), name='blog-home'),
    path('blog/user/<str:username>/', UserPostListView.as_view(), name='blog-user_posts'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='blog-detail'),
    path('blog/new/', PostCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update', PostUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete', PostDeleteView.as_view(), name='blog-delete'),
]