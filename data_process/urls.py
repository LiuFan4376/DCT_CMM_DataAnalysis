from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('upload', views.upload_file),
    path('downloadA',views.download_fileA),
    path('downloadB',views.download_fileB),
]
