from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
)
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from therapy.models import *
from .forms import UserCreateForm, ChangeUserlnfoForm, UserLoginForm, UserPasswordResetForm, AddBidForm


def index(request):
    context = {
        "title": "THERAPY CLUB",
    }
    return render(request, "therapy/index.html", context=context)


@login_required(login_url="/register/")
def profile(request):
    user = request.user
    context = {
        "user": user,
        "title": "профиль",
    }
    return render(request, "registration/profile.html", context=context)


class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {
            "form": UserCreateForm(),
            "title": "регистрация",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("profile")
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


class UpdateUserInfo(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/update_user_info.html"
    form_class = ChangeUserlnfoForm
    success_url = reverse_lazy("profile")

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserLogin(LoginView):
    template_name = "registration/user_login.html"
    form_class = UserLoginForm


class UserPasswordReset(PasswordResetView):
    template_name = "registration/user_password_reset.html"
    form_class = UserPasswordResetForm

    def get_success_url(self):
        return reverse_lazy("user_password_reset_done")


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = "registration/user_password_reset_done.html"


@login_required(login_url="/register/")
def add_bid(request):
    cotext = {
        'form': AddBidForm()
    }
    return render(request, context=cotext, template_name="therapy/add_bid.html")
