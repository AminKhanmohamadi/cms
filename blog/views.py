from logging import raiseExceptions

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, CreateView

from blog.forms import ShareForm , CommentForm , CreatePostForm
from blog.models import Post, Category , Comment


# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.filter(status=Post.StatusChoices.PUBLISHED)
    template_name = 'blog/list.html'
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'] , status=Post.StatusChoices.PUBLISHED , publish_time__year=self.kwargs['year'] , publish_time__month=self.kwargs['month'] , publish_time__day=self.kwargs['day'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(approved=True , post=self.get_object())
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user= request.user
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
        else:
            self.object = post
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context=context)



class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/categories.html'
    queryset = Category.objects.filter(active=True)


class CategoryDetailView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        posts = Post.objects.filter(category=category)
        return render(request, 'blog/list.html', {'posts': posts})



class SharePostView(View):
    def get(self, request, pk):
        form = ShareForm()
        post = get_object_or_404(Post, pk=pk)
        return render(request , 'blog/share.html' , {'form':form , 'post':post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = ShareForm(request.POST)
        if form.is_valid():
            send_mail(
                'Sharing Post {}'.format(post.title),
                form.cleaned_data.get('description'),
                form.cleaned_data.get('email'),
                [form.cleaned_data.get('to')],
                fail_silently=False,
            )
            return redirect(post.get_absolute_url())
        return render(request , 'blog/share.html' , {'form':form , 'post':post})

