from django.urls import path
from .views import *

urlpatterns = [
    path('create-blog/', createBlogView, name='create-blog')
]