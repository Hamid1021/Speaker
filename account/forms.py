from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


from django.contrib.auth.forms import PasswordChangeForm

class SpeakerPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        label="نام کاربری",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "name": "username",
                "id": "username",
                "placeholder": "نام کاربری",
                "class": "form-control",
            }
        ))
    password = forms.CharField(
        max_length=100,
        label="رمز عبور",
        label_suffix="",
        widget=forms.PasswordInput(
            attrs={
                "name": "password",
                "id": "password",
                "placeholder": "رمز عبور",
                "class": "form-control",
            }
        ))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError(
                "نام کاربری صحیح نمی باشد دوباره امتحان کنید")
        else:
            return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username, pass_per_save=password)
        if not user:
            raise forms.ValidationError(
                "رمز عبور صحیح نمی باشد دوباره امتحان کنید")
        else:
            return password


class SingUpForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        label="نام کاربری",
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "name": "username",
                "id": "username",
                "placeholder": "نام کاربری",
                "class": "form-control",
                "oninput":"validateInput(event)", 
                "onkeypress":"validateInput(event)", 
            }
        ))
    first_name = forms.CharField(
        max_length=200,
        label="",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input--style-4", "id": "first_name", "placeholder":"نام"}
        ))
    education = forms.CharField(
        max_length=300,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "input--style-4", "placeholder":"میزان تحصیلات"}
        ))
    address = forms.CharField(
        max_length=700,
        label="",
        required=False,
        widget=forms.Textarea(
            attrs={"class": "input--style-4", "placeholder":"آدررس"}
        ))
    last_name = forms.CharField(
        max_length=200,
        label="",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input--style-4", "id": "last_name", "placeholder":"نام خانوادگی"}
        ))
    email = forms.CharField(
        max_length=300,
        label="",
        required=False,
        widget=forms.EmailInput(
            attrs={"name": "email", "class": "input--style-4",
                   "id": "email", "placeholder":"test@test.com"}
        ))
    password = forms.CharField(
        max_length=100,
        label="رمز عبور",
        label_suffix="",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "name": "password",
                "id": "password",
                "placeholder": "رمز عبور",
                "class": "form-control",
            }
        ))
    password_confirm = forms.CharField(
        max_length=100,
        label="تکرار رمز عبور",
        label_suffix="",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "name": "password",
                "id": "password",
                "placeholder": "تکرار رمز عبور",
                "class": "form-control",
            }
        ))
    # familier = forms.CharField(
    #     max_length=8,
    #     label="",
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs={"type": "text", "class": "input--style-4", "id": "familier_code"}
    #     ))
    phone_number = forms.CharField(
        max_length=11,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "type": "tel", "pattern": "^(\+989)+\d{9}$|^(09)+\d{9}$",
            "class": "input--style-4", "id": "phone", "placeholder":"09123456789"}
        ))
    age = forms.IntegerField(
        label="سن",
        label_suffix="",
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "input--style-4", "id": "age", "min":0, "value":0}
        ))
    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 0:
            raise forms.ValidationError("سن نمی‌تواند کمتر از 0 باشد.")
        return age
    # def clean_familier(self):
    #     familier_code = self.cleaned_data.get("familier")
    #     if not familier_code:
    #         return familier_code
    #     else:
    #         user_check = User.objects.filter(familier_code=familier_code)
    #         if not user_check:
    #             raise forms.ValidationError(
    #                 "کد معرف یافت نشد خالی رها کرده یا اصلاح نمایید")
    #         return familier_code

    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data.get("phone_number")
    #     user_check = User.objects.filter(phone_number=phone_number)
    #     if user_check:
    #         raise forms.ValidationError(
    #             "این شماره همراه قبلا ثبت نام کرده است")
    #     else:
    #         return phone_number

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     user_check = User.objects.filter(email=email)
    #     if user_check:
    #         raise forms.ValidationError(
    #             "فردی با این ایمیل ثبت نام کرده است")
    #     else:
    #         return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_check = User.objects.filter(username=username)
        if user_check:
            raise forms.ValidationError(
                "نام کاربری انتخابی از قبل موجود است با نام دیگری دوباره امتحان کنید")
        else:
            return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password_confirm != password:
            raise forms.ValidationError(
                "تکرار رمز عبور صحیح نمی باشد لطفا بررسی نمایید")
        else:
            return password_confirm
