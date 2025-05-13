from django.urls import path, include
from .views import index, get_mpesa_access_token, stk_push
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'pay', stk_push)

urlpatterns = [
    path('', index, name="index"),
    path('pay/', stk_push, name='stk_push')
]