from django.urls import path
from .views import  PostListView , PostDetailView , CategoryListView ,CategoryDetailView

app_name = "blog"
urlpatterns = [
    path('' , PostListView.as_view() , name='list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/' , PostDetailView.as_view() , name='detail'),
    path('categories/' , CategoryListView.as_view() , name='categories'),

    path('categories/post-list/<int:category_id>/' , CategoryDetailView.as_view() , name='categories-list'),
]