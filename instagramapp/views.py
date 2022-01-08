from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import forms
from .forms import LoginForm, PostForm
from instagramapp.models import Users, Post, Follow
from django.core.files.storage import FileSystemStorage

# Create your views here.
def signup_page(request):
    if request.session.has_key("user"):
        del request.session["user"]
    form = forms.UserForm
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            request.session["user"] = form.cleaned_data["user_name"]
        return redirect("/home")
        # return render(request, "instagramapp/sign-up.html", {"form": form})
    return render(request, "instagramapp/sign-up.html", {"form": form})


def view_login(request):
    if request.session.has_key("user"):
        del request.session["user"]
    err = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            password = form.cleaned_data["password"]
            user = Users.objects.get(user_name=user_name)

            if user:
                # print(user)
                if user.password == password:
                    request.session["user"] = user.user_name
                    return redirect("/home")
                else:
                    err = "Password Mismatch"

    else:
        form = LoginForm()
    return render(request, "instagramapp/login.html", {"form": form, "err": err})


def view_home(request):
    if request.session.has_key("user"):
        session_user_name = request.session["user"]
        session_user_object = Users.objects.get(user_name=session_user_name)
        session_user_following, create = Follow.objects.get_or_create(
            user=session_user_object
        )
        following = session_user_following.following.all()
        posts = Post.objects.filter(user__in=following).order_by("-created")
        return render(request, "instagramapp/profile-home.html", {"posts": posts})
    else:
        return redirect("/login")


def view_profile(request, user_name):
    if request.session.has_key("user"):
        session_user_name = request.session["user"]
        # user = Users.objects.get(user_name=session_user_name)
        my_posts = Post.objects.filter(user=user_name)
        session_user_object = Users.objects.get(user_name=session_user_name)
        session_user_following = Follow.objects.get(user=session_user_object)
        following_count = session_user_following.following.all().count()
        followers_count = session_user_object.followers.all().count()
        user_info = {
            "my_posts": my_posts,
            "user_name": user_name,
            "count_of_posts": len(my_posts),
            "following_count": following_count,
            "followers_count": followers_count,
        }
        return render(request, "instagramapp/profile.html", context=user_info)
    else:
        return redirect("/login")


def post(request):
    if request.session.has_key("user"):
        user_name = request.session["user"]
        if request.method == "POST":
            form = forms.PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.cleaned_data.get("post")
                location = form.cleaned_data.get("location")
                description = form.cleaned_data.get("description")
                user = Users.objects.get(user_name=user_name)
                obj = Post(
                    user=user, post=post, location=location, description=description
                )
                obj.save()
            return redirect("/profile/" + user_name)
        else:
            form = forms.PostForm()
        return render(request, "instagramapp/post-form.html", {"form": form})
    else:
        return redirect("/login")


# def follow_user(request, user_name):
#     other_user = Users.objects.get(name=user_name)
#     session_user = request.session["user"]
#     get_user = Users.objects.get(name=session_user)
#     check_follower = Follow.objects.get(user=get_user.id)
#     is_followed = False
#     if other_user.name != session_user:
#         if check_follower.another_user.filter(name=other_user).exists():
#             add_usr = Follow.objects.get(user=get_user)
#             add_usr.another_user.remove(other_user)
#             is_followed = False
#             return redirect(f"/profile/{session_user}")
#         else:
#             add_usr = Follow.objects.get(user=get_user)
#             add_usr.another_user.add(other_user)
#             is_followed = True
#             return redirect(f"/profile/{session_user}")

#         return redirect(f"/profile/{session_user}")
#     else:
#         return redirect(f"/profile/{session_user}")


def explore(request):
    if request.session.has_key("user"):
        current_user = request.session["user"]
        current_user_obj = Users.objects.get(user_name=current_user)
        following = Follow.objects.filter(user=current_user_obj).values("following")
        others = Users.objects.exclude(user_name__in=following).exclude(
            user_name=current_user
        )
        user_names = Users.objects.exclude(user_name=current_user).values("user_name")
        return render(
            request,
            "instagramapp/explore-friends.html",
            context={"following": following, "others": others},
        )
    else:
        return redirect("/login")


def delete_post(request, pk):
    session_user = request.session["user"]
    # if request.method == "POST":
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect(f"/profile/{session_user}")


def view_post(request, pk):
    session_user = request.session["user"]
    post = Post.objects.get(pk=pk)
    return render(request, "instagramapp/view-post.html", {"post": post})
