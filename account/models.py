# from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid
from django.apps import apps
from django.contrib.auth.hashers import make_password
from random import randint
from django.utils import timezone
from extensions.utils import (
    jalali_converter
)
from ckeditor.fields import RichTextField

def generate_ranint():
    return randint(100000, 999999)


def upload_to_Image_file(instance, filename):
    return f"users/images/{filename.encode('utf-8').strip()}"


def upload_to_Ticket_file(instance, filename):
    return f"panel/ticket/{filename.encode('utf-8').strip()}"


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        global_user_model = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = global_user_model.normalize_username(username)
        user = self.model(
            username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # str(uuid.uuid4())[-1:8:-1] is a 24 random character
        extra_fields.setdefault('custom_user_id', str(uuid.uuid4())[:11:-1])
        extra_fields.setdefault('gender', "m")
        extra_fields.setdefault('pass_per_save', password or "")
        extra_fields.setdefault('code_send', generate_ranint())
        extra_fields.setdefault('email_sended', False)
        return self._create_user(username, email, password, **extra_fields)

    def _create_super_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        global_user_model = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = global_user_model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('pass_per_save', password or "")
        extra_fields.setdefault('custom_user_id', str(uuid.uuid4())[:11:-1])
        extra_fields.setdefault('gender', "m")
        extra_fields.setdefault('code_send', generate_ranint())
        extra_fields.setdefault('email_sended', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_super_user(username, email, password, **extra_fields)


class USER(AbstractUser):
    pass_per_save = models.CharField(
        verbose_name="گذر واژه هش نشده", max_length=255, blank=True
    )
    GENDER_CHOICES = (
        ("m", "مرد"),
        ("w", "زن"),
    )
    gender = models.CharField(
        verbose_name="جنسیت", max_length=1, null=False,
        blank=False, choices=GENDER_CHOICES, default="m"
    )
    avatar = models.ImageField(
        verbose_name="آواتار", upload_to=upload_to_Image_file, null=True,
        blank=True, default="None"
    )
    phone_number = models.CharField(
        verbose_name="شماره همراه", max_length=11, null=True, blank=True, unique=True
    )
    bio = RichTextField(
        verbose_name="درباره من", max_length=300, null=True, blank=True,
        help_text="در باره خودتان در حدود 300 کلمه بنویسید"
    )
    custom_user_id = models.CharField(
        verbose_name="کد اختصاصی کاربر", max_length=24, null=True, blank=True, unique=True
    )
    code_send = models.IntegerField(
        verbose_name="کد ارسال شده", null=True, blank=True
    )
    email_sended = models.BooleanField(
        default=False, verbose_name="ایمیل ارسال شده است"
    )
    objects = CustomUserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.first_name != "" or self.last_name != "":
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        else:
            full_name = '%s' % (self.username,)
            return full_name.strip()


class AnswerTicket(models.Model):
    message = RichTextField(
        verbose_name="پاسخ پیام", null=False, blank=False, default=""
    )
    status = models.BooleanField(
        verbose_name="نمایش داده شود/نمایش داده نشود", default=True)

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ارسال پاسخ")

    def jcreated(self):
        return jalali_converter(self.created)

    jcreated.short_description = "زمان ارسال پاسخ به شمسی"

    def __str__(self):
        return f"{self.message[:40]} ..."

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پاسخ های ارسالی"


class Ticket_Manager(models.Manager):
    def get_last_three_unread_message(self):
        try:
            return self.get_queryset().order_by("-created").filter(status=False)[:3]
        except:
            return None


class Ticket(models.Model):
    title = models.CharField(
        verbose_name="موضوع پیام", max_length=255, blank=False, null=False, default="")
    message = RichTextField(
        verbose_name="پیام شما", blank=False, null=False)
    created = models.DateTimeField(
        verbose_name="زمان ارسال به میلادی", blank=True, null=True)
    status = models.BooleanField(
        verbose_name="خوانده شده/خوانده نشده", default=False)
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, null=False, blank=False, verbose_name="کاربر"
    )
    replay = models.ForeignKey(
        AnswerTicket, on_delete=models.CASCADE, null=True, blank=True, default="",
        verbose_name="پاسخ پیام",
    )
    file = models.FileField(
        upload_to=upload_to_Ticket_file, verbose_name='فایل ارسالی کاربر', null=True,
        blank=True, default="None"
    )

    def __str__(self):
        return f"{self.title}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.created = timezone.now()
        return super().save(
            force_insert=False, force_update=False, using=None,
            update_fields=None
        )

    def jcreated(self):
        return jalali_converter(self.created)

    jcreated.short_description = "زمان ارسال به شمسی"

    objects = Ticket_Manager()

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"
        ordering = ['-created']
