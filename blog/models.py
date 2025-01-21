from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255 , verbose_name=_('title'))
    active = models.BooleanField(default=True, verbose_name=_('active'))

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
        return reverse_lazy('detail', kwargs={'year': self.publish_time.year , 'month': self.publish_time.month ,'day':self.publish_time.day , 'slug': self.slug})