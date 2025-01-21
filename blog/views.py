from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView , View

from blog.models import Post, Category


# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.filter(status=Post.StatusChoices.PUBLISHED , publish_time__lte=timezone.now())
    template_name = 'blog/list.html'
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'] , status=Post.StatusChoices.PUBLISHED , publish_time__year=self.kwargs['year'] , publish_time__month=self.kwargs['month'] , publish_time__day=self.kwargs['day'])



class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/categories.html'


class CategoryDetailView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        posts = Post.objects.filter(category=category)
        return render(request, 'blog/list.html', {'posts': posts})

