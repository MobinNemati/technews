from django.urls import path
from news import views



app_name = 'news'

urlpatterns = [
    path('', views.news_view, name='home'),
    path('single/<int:pid>/', views.news_single, name='single'),
    path('search/', views.news_search, name='search'),
    path('category/<str:cat_name>', views.news_view, name='category'),
    path('tag/<str:tag_name>', views.news_view, name='tag'),
    path('author/<str:author_username>', views.news_view, name='author'),


]