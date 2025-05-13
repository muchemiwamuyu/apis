from django.urls import path, include
from .views import index, StudentViewSet, CourseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)



urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),

]