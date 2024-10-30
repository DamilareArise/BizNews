from django.urls import path
from .views import *

urlpatterns = [
    path('create-blog/', createBlogView, name='create-blog'),
    path('view-blog/<int:id>/', displayBlogView, name='view-blog' ),
    path('delete-blog/<int:id>/', deleteBlogView, name='delete-blog'),
    path('edit-blog/<int:id>/',  editBlogView, name='edit-blog'),
    path('all-blog', allBlogView, name='all-blog'),
    path('approve/<int:id>/', approveView, name='approve'),
    path('like/<int:blog_id>/', likeView, name='like'),
    path('add-comment/<int:blog_id>/', addCommentVIew, name='add-comment')

]