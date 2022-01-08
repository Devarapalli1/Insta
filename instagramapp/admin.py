from pathlib import PosixPath
from django.contrib import admin
from instagramapp.models import Users, Post, Follow

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "user_name", "password", "date_created"]


admin.site.register(Users, UsersAdmin)
admin.site.register(Post)
# admin.site.register(Profile)
admin.site.register(Follow)
