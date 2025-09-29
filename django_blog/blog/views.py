from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, ProfileForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # log user in immediately
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("blog:home")  # change to your homepage route name
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "blog/login.html"

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('blog:home')

@login_required
def profile_view(request):
    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
    else:
        pform = ProfileForm(instance=request.user.profile)

    return render(request, "blog/profile.html", {"pform": pform})

def home(request):
    return render(request, "blog/home.html")

class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"   # customize path
    context_object_name = "posts"
    paginate_by = 6

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = reverse_lazy("blog:login")

    def form_valid(self, form):
        # set author to current user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = reverse_lazy("blog:login")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:posts-list")
    login_url = reverse_lazy("blog:login")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user