from django.contrib import admin
from .models import Subscribe, UserFoodgram
from django.contrib.auth.admin import UserAdmin


@admin.register(UserFoodgram)
class User(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('username',)


@admin.register(Subscribe)
class Subscribe(admin.ModelAdmin):
    list_display = ('user', 'author',)
