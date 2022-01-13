from django.db import models
from django.db.models.base import Model
from django.forms import widgets
from django.utils import timezone

# Create your models here.
class Users(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=40, unique=True, primary_key=True)
    password = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.FileField(
        default="profile_pics/default.jpg", upload_to="profile_pics/"
    )


"""class Profile(models.Model):
    user_name = models.OneToOneField(Users, on_delete=models.CASCADE)
    following = models.ManyToManyField(Users, related_name="following", blank=True)
    profile_pic = models.ImageField(upload_to="profile-pics", blank=True, null=True)

    def profile_post(self):
        pass

    pass
"""


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.user_name, filename)


class Post(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.FileField(upload_to=user_directory_path)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    likes = models.ManyToManyField(Users, related_name="post_like")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.user.user_name

    def delete(self, *args, **kwargs):
        self.post.delete()
        super().delete(*args, **kwargs)  # Call the "real" delete() method.


class Follow(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    following = models.ManyToManyField(Users, related_name="followers")

    def __str__(self):
        return self.user.name


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]
