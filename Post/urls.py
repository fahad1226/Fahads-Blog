from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,PostLikeRedirect,UserDetailView
from users.views import UserFollowView

urlpatterns = [

    path('',PostListView.as_view(),name='post-home'),
    path('user/<str:username>/',UserPostListView.as_view(),name='post-user'),
    path('user/<str:username>/detail/',UserDetailView.as_view(),name='user-detail'),
    path('user/<str:username>/detail/follow/',UserFollowView.as_view(),name='user-follow'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:pk>/likes/',PostLikeRedirect.as_view(),name='post-likes'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('about/',views.About,name='post-about'),
    path('post/<int:pk>/new_comment/',views.add_comment,name='add_comments'),
    path('change_pass/',views.change_password,name='change_pass')

]
