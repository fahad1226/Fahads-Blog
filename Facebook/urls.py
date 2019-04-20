
from django.contrib import admin
from django.urls import path ,include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Post import views
from Post.views import UserDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Post.urls')),
    path('register/',user_views.register,name='register'),
    path('change_pass/',views.change_password,name='change_pass'),
    path('profile/',user_views.profile,name='profile'),
    path('user/<str:username>/detail',UserDetailView.as_view(),name='user_detail'),
    path('update/',user_views.profile_update,name='profile_update'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('social_auth/',include('social.apps.django_app.urls',namespace = 'social')),


]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
