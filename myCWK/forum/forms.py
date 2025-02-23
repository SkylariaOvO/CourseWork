from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'file']

    image = forms.ImageField(required=False)
    file = forms.FileField(required=False)
