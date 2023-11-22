from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.list_songs),
    path('new',views.edit_song),
    path('<int:pk>',views.edit_song),
]