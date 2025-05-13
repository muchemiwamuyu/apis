from django.urls import path
from .views import index, register, login

urlpatterns = [
    path('accounts/', index, name="index"),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
]