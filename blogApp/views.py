from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogInfo, Like, Comment
from .forms import BlogForm, CommentForm
from django.contrib import messages
from BizNews.userApp.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def allPostView(request):
    allPost = BlogInfo.objects.all() # [ (), () ]
   
    blog_data = [] # [{},{}]
    for post in allPost:
        if post.approved:
            blog_data.append(
                {
                    'post': post,
                    'likes': post.total_likes(),
                    'comments': post.total_comments()
                }
            )

    # print(blog_data)

    return render(request, template_name='index.html', context={'post_data':blog_data}) 

@login_required
def allBlogView(request):
    blogs = BlogInfo.objects.all()

    return render(request, template_name='blogApp/all_blog.html', context={'allBlog':blogs})

@login_required
def createBlogView(request):
    if request.method == 'POST':
        form = BlogForm(request.POST,  request.FILES)
        if form.is_valid():
            blogForm = form.save(commit=False)
            title = blogForm.title

            author = Profile.objects.get(user_id = request.user.id)
            blogForm.author = author
            blogForm.save()

            # send mail to the user that created the blog
            send_mail(
                subject='Blog created successfully',
                message=f'You have successfull created a blog titled {title}. Kindly wait as it get approved.\nThank you for using our Service',
                from_email='biznews@gmail.com',
                recipient_list=[request.user.email],
                fail_silently = True
            )

            # Sending emails to all the staffs
            # emails =User.objects.filter(is_staff = True).values_list('email', flat=True) 

            # or 

            staffs = User.objects.filter(is_staff = True) 
            emails = [staff.email for staff in staffs]
            send_mail(
                subject='Approve Request',
                message=f'A blog titled {title} was just created by {request.user.first_name} {request.user.last_name}. Kindly review via http://127.0.0.1:8800/blogApp/all-blog',
                from_email='biznews@gmail.com',
                recipient_list= emails,
                fail_silently = True
            )

            

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
    user = get_object_or_404(Profile, user_id = request.user.id)
    blog = BlogInfo.objects.get(blog_id = id)
    likes = blog.total_likes()
    noOfComments = blog.total_comments()
    
    all_comment = Comment.objects.filter(blog_id = id)
    # print(all_comment)


    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            validform = form.save(commit=False)
            validform.user = user
            validform.blog = blog

            validform.save()

            messages.success(request, 'comment successfully')
        else:
            messages.error(request, 'error occured')
        
        return redirect('view-blog', id)


    else:
        form = CommentForm()

    return render(request, template_name='blogApp/view_blog.html', context={'blog':blog, 'likes':likes, 'comments':noOfComments, 'commentForm':form, 'all_comment':all_comment}) 

@login_required
def deleteBlogView(request, id):
    blog = BlogInfo.objects.get(blog_id = id)
    blog.delete()

    messages.success(request, 'Post Deleted successfully')
    return redirect('home')


@login_required
def editBlogView(request, id):
    blog = get_object_or_404(BlogInfo, blog_id = id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Edited successfully')
            return redirect('view-blog', id)
        else:
            messages.error(request, 'Post Could not be edited')
            return render(request, template_name='blogApp/edit_blog.html', context={'editForm':form})

    else:
        form = BlogForm(instance=blog)
        return render(request, template_name='blogApp/edit_blog.html', context={'editForm':form})
    

@login_required
def approveView(request, id):
    blog = BlogInfo.objects.get(blog_id = id)
    
    if blog.approved:
       BlogInfo.objects.filter(blog_id = id).update(approved = False)
    else:
        BlogInfo.objects.filter(blog_id = id).update(approved = True)

    return redirect('all-blog')




@login_required
def likeView(request, blog_id):
    blog = get_object_or_404(BlogInfo, blog_id = blog_id)
    user = get_object_or_404(Profile, user_id = request.user.id)

    exists = Like.objects.filter(user_id = request.user.id, blog_id = blog_id ).exists()
    
    if exists:
        Like.objects.filter(user_id = request.user.id, blog_id = blog_id ).delete()
    else:
        Like.objects.create(user = user, blog = blog)

    return redirect('view-blog', blog_id)


@login_required
def addCommentVIew(request, blog_id):
    user = get_object_or_404(Profile, user_id = request.user.id)
    blog = get_object_or_404(BlogInfo, blog_id = blog_id)

    if request.method == 'POST':
       content = request.POST['content']
       Comment.objects.create(user = user, blog = blog, content = content)

    return redirect('view-blog', blog_id)

