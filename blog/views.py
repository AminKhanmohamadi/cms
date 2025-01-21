from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category


# Create your views here.

def list_view(request):
    queryset = Post.objects.filter(status=Post.StatusChoices.PUBLISHED , publish_time__lte=timezone.now())
    return render(request , 'blog/list.html' , {'posts': queryset})



def detail_view(request, **kwargs):
    year = kwargs.get('year')
    month = kwargs.get('month')
    day = kwargs.get('day')
    slug = kwargs.get('slug')
    post = get_object_or_404(Post , slug=slug , status=Post.StatusChoices.PUBLISHED , publish_time__year=year , publish_time__month=month , publish_time__day=day)
    return render(request , 'blog/detail.html' , {'post': post})


def categories_view(request):
    queryset = Category.objects.all()
    return render(request , 'blog/categories.html' , {'categories': queryset})