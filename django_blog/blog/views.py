# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from .forms import RegisterForm, ProfileForm, PostForm, CommentForm
from .models import Post, Comment, Tag


# ---------- Registration / Login ----------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("blog:home")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "blog/login.html"


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("blog:home")


# ---------- Profile ----------
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


# ---------- Home ----------
def home(request):
    return render(request, "blog/home.html")


# ---------- Posts ----------
class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    context_object_name = "posts"
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object
        ctx["comments"] = post.comments.select_related("author").all()
        if self.request.user.is_authenticated:
            ctx["comment_form"] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = reverse_lazy("blog:login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = reverse_lazy("blog:login")

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:posts-list")
    login_url = reverse_lazy("blog:login")

    def test_func(self):
        return self.get_object().author == self.request.user


# ---------- Comments ----------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs["post_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentListView(ListView):
    model = Comment
    template_name = "comments/comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        return Comment.objects.filter(post__pk=post_pk).select_related("author")


# ---------- Search ----------
def search_posts(request):
    query = request.GET.get("q", "")
    results = Post.objects.all()
    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(
        request,
        "blog/search_results.html",
        {"query": query, "results": results},
    )


# ---------- Tags ----------
class TagPostListView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return Post.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
