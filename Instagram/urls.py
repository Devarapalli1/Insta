"""Instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from instagramapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.signup_page),
    path("sign-up/", views.signup_page),
    path("login/", views.view_login),
    path("home/", views.view_home),
    path("profile/<str:user_name>", views.view_profile, name="profile"),
    path("post/", views.post),
    path("explore/", views.explore),
    path("delete-post/<int:pk>/", views.delete_post, name="deletepost"),
    path("viewpost/<int:pk>/", views.view_post, name="viewpost"),
    path("follow/<str:user_name>/", views.follow_user, name="follow"),
    path("unfollow/<str:user_name>/", views.unfollow, name="unfollow"),
    path("delete/<str:user_name>/", views.delete_account, name="delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
