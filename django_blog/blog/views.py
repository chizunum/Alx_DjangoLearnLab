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
from .models import Post, Comment
from .forms import PostForm
from .forms import CommentForm
from django.urls import reverse

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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'


    def dispatch(self, request, *args, **kwargs):
   # cache the parent post
       self.post = get_object_or_404(Post, pk=kwargs['post_pk'])
       return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})




class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'


    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user




class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'


    def get_success_url(self):
       return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


    def test_func(self):
      comment = self.get_object()
      return comment.author == self.request.user




class CommentListView(ListView):
    model = Comment
    template_name = 'comments/comment_list.html'
    context_object_name = 'comments'


    def get_queryset(self):
       post_pk = self.kwargs['post_pk']
       return Comment.objects.filter(post__pk=post_pk).select_related('author')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


    def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      post = self.object
      ctx['comments'] = post.comments.select_related('author').all()
      if self.request.user.is_authenticated:
        ctx['comment_form'] = CommentForm()
      return ctx