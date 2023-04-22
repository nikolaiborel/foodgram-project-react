from django.urls import path, include
from .views import (Authorization, LogOut, SubscribeUser, subscribtion)

urlpatterns = [
    path('users/subscriptions/', subscribtion, name='subscription'),
    path('auth/token/login/', Authorization.as_view(), name='login'),
    path('auth/token/logout/', LogOut().as_view(), name='logout'),
    path('users/<str:pk>/subscribe/', SubscribeUser.as_view(), name='subscribe'),
    path('', include('djoser.urls')),
]
