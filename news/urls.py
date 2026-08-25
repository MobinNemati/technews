from django.urls import path

from news import views


app_name = 'news'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('single/<int:pid>/', views.PostDetailView.as_view(), name='single'),
    path('search/', views.PostSearchView.as_view(), name='search'),
    path('category/<str:cat_name>', views.PostListView.as_view(),
         name='category'),
    path('tag/<str:tag_name>', views.PostListView.as_view(), name='tag'),
    path('author/<str:author_username>', views.PostListView.as_view(),
         name='author'),
]
