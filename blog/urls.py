from django.urls import path
from .views import PostListView, PostDetailView, CategoryListView, CategoryDetailView, SharePostView, CreatePostView

app_name = "blog"
urlpatterns = [
    path('' , PostListView.as_view() , name='list'),
    path('share/<int:pk>', SharePostView.as_view(), name='share_post'),
    path('create-post/' , CreatePostView.as_view() , name='create_post'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/' , PostDetailView.as_view() , name='detail'),
    path('categories/' , CategoryListView.as_view() , name='categories'),
    path('categories/post-list/<int:category_id>/' , CategoryDetailView.as_view() , name='categories-list'),

]