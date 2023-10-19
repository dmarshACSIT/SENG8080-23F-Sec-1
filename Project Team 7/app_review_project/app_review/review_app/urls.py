from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('home', views.home_page, name='home_page'),
    # path('get_app_review_data', views.get_app_review_data, name='get_app_review_data'),
    path('get_app_data', views.get_app_data, name="get_app_data"),
    path('get_category_data', views.get_category_wise_data, name="get_category_wise_data"),
    path('logout', views.logout_page, name="logout"),
]