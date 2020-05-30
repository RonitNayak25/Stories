from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('post/<int:pk>/', single, name='post_detail'),
    path('foods/', Foods.as_view(), name='foods'),
    path('lifestyle/', Lifestyle.as_view(), name='lifestyle'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='MyApp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='MyApp/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete')
]
