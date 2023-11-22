from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('new',views.new_show),
    path('<int:pk>',views.new_show)
]