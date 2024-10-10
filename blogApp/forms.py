from django import forms
from .models import BlogInfo



class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogInfo
        fields = [
            'title',
            'category',
            'image',
            'content'
        ]