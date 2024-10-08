from django.shortcuts import render
from .models import BlogInfo, Like, Comment

# Create your views here.
def allPostView(request):
    allPost = BlogInfo.objects.all()
    return render(request, template_name='index.html', context={'allpost':allPost}) 