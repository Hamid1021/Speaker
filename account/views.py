from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
# from django.contrib.auth.models import Group
from account.models import USER
from application.Entities.Speaker_model import Speaker

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
            login(request, user=user)
            if not user.is_superuser:
                # request.session.set_expiry(20 * 60)
                return redirect(reverse("application:select_order_by_speaker"))
            # return redirect(reverse("admin:index"))
            return redirect(reverse("application:assign"))

    context = {
        "form": form
    }
    return render(request, "login.html", context)


def register_user(request):
    form = SingUpForm(request.POST or None)
    er_message = ""
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            phone = form.cleaned_data.get("phone_number")
            age = form.cleaned_data.get("age")
            education = form.cleaned_data.get("education")
            address = form.cleaned_data.get("address")
            try:
                user = USER.objects.create_user(
                    username=username, password=password, 
                    first_name=first_name, last_name=last_name, email=email, phone_number=phone, is_staff=True
                )
                
                # ایجاد سخنران جدید برای کاربر تازه ایجاد شده
                speaker = Speaker.objects.create(
                    user=user,
                    name=first_name,
                    family=last_name,
                    phone=phone,
                    age=age,
                    address=address,
                    total_number_of_lectures=0,
                    status=True,
                    is_deleted=False,
                    education_attendees=education,
                )

                # # بررسی وجود گروه سخنرانان و افزودن کاربر به گروه
                # speaker_group, created = Group.objects.get_or_create(name="سخنرانان")
                # speaker_group.user_set.add(user)

                return redirect(reverse("account:login"))
            except Exception as e:
                print(e)
                er_message = "مشکلی وجود دارد لطفا از راه های ارتباطی به ما اطلاع بدهید"

    context = {
        "form": form,
        "er_message": er_message
    }
    return render(request, "register.html", context)





def logout_admin(request):
    logout(request)
    return redirect(reverse("account:login"))
