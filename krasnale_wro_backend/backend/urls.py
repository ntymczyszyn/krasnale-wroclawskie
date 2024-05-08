from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('image/upload', views.image_upload, name='image_upload'),
]