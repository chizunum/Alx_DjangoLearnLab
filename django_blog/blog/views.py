from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, ProfileForm
from django.urls import reverse_lazy

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
