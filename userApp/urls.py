from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profileView, name='profile'),
    path('edit-profile/<int:userid>/', editProfileView, name='editProfile')
]
