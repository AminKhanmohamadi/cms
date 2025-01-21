from django.urls import path
from .views import list_view, detail_view, categories_view

urlpatterns = [
    path('' , list_view , name='list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/' , detail_view , name='detail'),
    path('categories/' , categories_view , name='categories'),
]