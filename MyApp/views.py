from django.shortcuts import render, redirect
from .models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can Login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'MyApp/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'MyApp/profile.html', context)


@login_required
def index(request):
    posts = Post.objects.all().order_by("-id")
    featured_posts = Post.objects.filter(is_featured=True).order_by("-id")[0:3]
    recent_posts = Post.objects.all().order_by("-id")[0:4]
    post_count = Post.objects.all().count()
    lifestyle_count = Post.objects.filter(category='Lifestyle').count()
    food_count = Post.objects.filter(category='Food').count()
    others_count = Post.objects.filter(category='Others').count()
    context = {
        'posts': posts,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'post_count': post_count,
        'lifestyle_count': lifestyle_count,
        'food_count': food_count,
        'others_count': others_count
    }
    return render(request, 'MyApp/index.html', context)


class Foods(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'MyApp/foods.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.filter(category='Food').order_by('-id')


class Lifestyle(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'MyApp/lifestyle.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.filter(category='Lifestyle').order_by('-id')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def contact(request):
    return render(request, 'MyApp/contact.html')


@login_required
def single(request, pk):
    posts = Post.objects.get(id=pk)
    recent_posts = Post.objects.all().order_by("-id")[0:3]
    lifestyle_count = Post.objects.filter(category='Lifestyle').count()
    food_count = Post.objects.filter(category='Food').count()
    context = {
        'posts': posts,
        'recent_posts': recent_posts,
        'lifestyle_count': lifestyle_count,
        'food_count': food_count
    }
    return render(request, 'MyApp/single.html', context)
