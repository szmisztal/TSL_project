from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from .forms import LoginForm, RegisterForm

@method_decorator(login_required, name = "dispatch")
class UsersListView(ListAPIView):
    serializer_class = UserSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users_list.html"

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all().order_by("role")
        return Response({"serializer": self.serializer_class(users), "users": users},
                        template_name = self.template_name)

def sign_up(request):
    template_name = "register.html"
    if request.method == "GET":
        form = RegisterForm()
        return render(request, template_name, {"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            user.set_group()
            messages.success(request, "Registration success, you can log in now.")
            return redirect("login")
        else:
            return render(request, template_name, {"form": form})

def sign_in(request):
    template_name = "login.html"
    next_url = request.GET.get("next")
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
    messages.success(request, "You have been logged out.")
    return redirect("login")
