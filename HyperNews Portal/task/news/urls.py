from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index_url"),
    path('news/', views.news, name="news_url"),
    path('news/create/', views.create_news, name="create_news_url"),
    path('news/<int:link>/', views.news_details, name="index_url"),

]
