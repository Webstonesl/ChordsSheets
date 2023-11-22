from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.home),
    path('login',views.login_page),
    path('logout',views.logout_page),
    path('signup',views.create_account_page),
    path('accounts/check',views.checkforuser),
    *views.getFileViews()

]
