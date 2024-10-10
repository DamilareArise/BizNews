from django.shortcuts import render, redirect
from .models import BlogInfo, Like, Comment
from .forms import BlogForm
from django.contrib import messages
from BizNews.userApp.models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def allPostView(request):
    allPost = BlogInfo.objects.all() # [ (), () ]
   
    blog_data = [] # [{},{}]
    for post in allPost:
        blog_data.append(
            {
                'post': post,
                'likes': post.total_likes(),
                'comments': post.total_comments()
            }
        )

    print(blog_data)

    return render(request, template_name='index.html', context={'post_data':blog_data}) 

@login_required
def createBlogView(request):
    if request.method == 'POST':
        form = BlogForm(request.POST,  request.FILES)
        if form.is_valid():
            blogForm = form.save(commit=False)
            author = Profile.objects.get(user_id = request.user.id)
            blogForm.author = author
            blogForm.save()

            messages.success(request, 'Post created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Error creating a Post')
            return render(request, template_name='blogApp/create_blog.html', context={'blogForm':form})
    else:
        form = BlogForm()
        return render(request, template_name='blogApp/create_blog.html', context={'blogForm':form}) 


@login_required
def displayBlogView(request, id):
    blog = BlogInfo.objects.get(blog_id = id)
    likes = blog.total_likes()
    comments = blog.total_comments()
    return render(request, template_name='blogApp/view_blog.html', context={'blog':blog, 'likes':likes, 'comments':comments}) 