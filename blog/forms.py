from django import forms

from blog.models import Comment, Post


class ShareForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'body': 'متن پیام'
        }


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'category', 'lead', 'body', 'status', 'publish_time')
        widgets = {
            'publish_time': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
