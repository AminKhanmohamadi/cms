from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255 , verbose_name=_('title'))
    active = models.BooleanField(default=True, verbose_name=_('active'))
    thumbnail = models.ImageField(upload_to="images/", verbose_name=_('thumbnail') , null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')



class Post(models.Model):

    class StatusChoices(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')

    title = models.CharField(max_length=255 , verbose_name=_('title'))
    thumbnail = models.ImageField(upload_to='post/thumbnail', verbose_name=_('thumbnail') , null=True)
    slug = models.SlugField(verbose_name=_('slug') , allow_unicode=True , unique_for_date='publish_time')
    category = models.ForeignKey(Category , on_delete=models.SET_NULL, verbose_name=_('category') , related_name='posts' , null=True)
    lead = models.CharField(verbose_name=_('lead') , max_length=1024 , null=True, blank=True)
    body = models.TextField(verbose_name=_('body'))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE , verbose_name=_('author'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    status = models.CharField(verbose_name=_('status') , max_length=15 , choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    featured = models.BooleanField(default=False, verbose_name=_('featured') , null=True)
    publish_time = models.DateTimeField(verbose_name=_('publish time') , null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-publish_time']

    def get_absolute_url(self):
        local_publish_time = timezone.localtime(self.publish_time)
        return reverse('blog:detail', kwargs={
            'year': local_publish_time.year,
            'month': local_publish_time.month,
            'day': local_publish_time.day,
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title , allow_unicode=True)
        super().save(*args, **kwargs)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE , verbose_name=_('post') , related_name='comments' , null=True)
    name = models.CharField(verbose_name=_('name') , max_length=255) #TODO: fix foreignkey to user model
    email = models.EmailField(verbose_name=_('email'))
    body = models.TextField(verbose_name=_('body'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    approved = models.BooleanField(default=True, verbose_name=_('approved'))

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')




