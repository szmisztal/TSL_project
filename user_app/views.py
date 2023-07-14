from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def sign_in(request):
    template_name = "login.html"
    next_url = request.GET.get('next')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username = username, password=  password)
            if user:
                login(request, user)
                messages.success(request, "You're logged in.")
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("homepage")
        messages.error(request, "Wrong username or password.")
    else:
        if request.user.is_authenticated:
            return redirect("homepage")
        form = LoginForm()
    return render(request, template_name, {"form": form})

def sign_out(request):
    logout(request)
    messages.success(request, "You have been log out.")
    return redirect("login")
