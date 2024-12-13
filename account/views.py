from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from .models import USER

from account.forms import SingUpForm, LoginForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("application:select_order_by_speaker"))
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if not user.is_superuser:
                request.session.set_expiry(20 * 60)
                login(request, user=user)
                return redirect(reverse("application:select_order_by_speaker"))
            login(request, user=user)
            return redirect(reverse("admin:index"))

    context = {
        "form": form
    }
    return render(request, "login.html", context)


def register_user(request):
    # if request.user.is_authenticated:
    #     return redirect(str(reverse("admin:app_list", kwargs={"app_label": "account"}))+"user/")
    form = SingUpForm(request.POST or None)
    er_message = ""
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            # first_name = form.cleaned_data.get("first_name")
            # last_name = form.cleaned_data.get("last_name")
            # email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # familier = form.cleaned_data.get("familier")
            # phone = form.cleaned_data.get("phone_number")
            try:
                user = USER.objects.create_user(
                    username=username, password=password
                )
                # if not user.is_superuser:
                #     request.session.set_expiry(20 * 60)
                #     login(request, user=user)
                #     return redirect(reverse("admin:index"))
                # login(request, user=user)
                return redirect(reverse("application:select_order_by_speaker"))
            except:
                er_message = "مشکلی وجود دارد لطفا از راه های ارتباطی به ما اطلاع بدهید"

    context = {
        "form": form,
        "er_message": er_message
    }
    return render(request, "register.html", context)


def logout_admin(request):
    logout(request)
    return redirect(reverse("account:login"))
