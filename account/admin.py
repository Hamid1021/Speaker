from django.contrib import admin
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from account.models import USER, Ticket, AnswerTicket
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.urls import reverse

from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

from PIL import Image

class UserAdminForm(forms.ModelForm):
      """Form for comments to the article."""

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
        #   self.fields["text"].required = False

      class Meta:
          model = USER
          fields = '__all__'
          widgets = {
              "bio": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              )
          }


class USERAdmin(UserAdmin):
    form = UserAdminForm
    fieldsets = (
        ("اطلاعات کاربری", {'fields': ('username', 'password', 'pass_per_save')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'avatar', 'email', 'bio')}),
        (('اطلاعات کاربردی'), {'fields': ('phone_number', 'custom_user_id', 'code_send', 'email_sended')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ("password",)
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    def add_view(self, request: HttpRequest, form_url: str = ..., extra_context: None = ...) -> HttpResponse:
        return redirect(reverse("account:register"))
        # return super().add_view(request, form_url, extra_context)
    
    list_display = ('username', 'phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_display_links = ('username', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'bio')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = ("password",)
            self.fieldsets = (
                ("اطلاعات کاربری", {'fields': ('username', 'password', 'pass_per_save')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'avatar', 'email', 'bio')}),
                (('اطلاعات کاربردی'), {'fields': ('phone_number', 'custom_user_id', 'code_send', 'email_sended')}),
                (_('Permissions'), {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        return request.user.is_superuser or (obj and obj.id == request.user.id)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        else:
            self.fieldsets = (
                ("اطلاعات کاربری", {'fields': ('username', 'pass_per_save')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'avatar', 'email', 'bio')}),
                (('اطلاعات کاربردی'), {'fields': ('phone_number',)}),
            )
            self.readonly_fields = (
                "username", "pass_per_save", "custom_user_id",
                "code_send", "email_sended", "is_active",
                "is_staff", "is_superuser", "groups", "user_permissions",
                "last_login", "date_joined",
            )
            return qs.filter(id=user.id)
    
    
    def save_model(self, request, obj, form, change) -> None:
        if change:
            unhash_password = obj.pass_per_save
            hash_password = make_password(unhash_password)
            obj.password = hash_password
            obj.save()
        return super().save_model(request, obj, form, change)



admin.site.register(USER, USERAdmin)


def make_True_Status(modeladmin, request, queryset):
    queryset.update(status=True)


make_True_Status.short_description = 'نمایش همه انتخاب شده ها به کاربر'


def make_False_Status(modeladmin, request, queryset):
    queryset.update(status=False)


make_False_Status.short_description = 'عدم نمایش انتخاب شده ها به کاربر'


# "title","message","created","status","user","replay","jcreated", "file",
class TicketAdmin(admin.ModelAdmin):
    fieldsets = (
        ("محتوی ارسالی", {'fields': ('title', 'message',)}),
        (_('user'), {'fields': ('user',)}),
        ("زمان ارسال", {'fields': ('created',)}),
        ('وضعیت', {'fields': ('status',)}),
    )
    list_display = [
        "title", "user", "jcreated", "status", "is_answer",
    ]
    search_fields = [
        "title", "message", "user__username", "user__first_name",
        "user_last_name", "replay__message"
    ]
    # readonly_fields = [
    #     "title", "message", "user", "created", "status", "file",
    # ]
    list_filter = ["status", ]
    actions = [make_True_Status, make_False_Status]

    # def save_model(self, request, obj, form, change):
    #     status = obj.status
    #     if not status:
    #         obj.status = True
    #     super().save_model(request, obj, form, change)

    # def has_add_permission(self, request, obj=None):
    #     return None

    # https://support.google.com/mail/answer/10336?p=NotAuthorizedError&visit_id=637740991285333331-3410284230&rd=1
    def is_answer(self, obj):
        status = False
        if obj.replay is not None:
            status = True
        return status

    is_answer.short_description = "پاسخ داده شده"
    is_answer.boolean = True


# admin.site.register(Ticket, TicketAdmin)


# "message","status", "jcreated", "created",
class AnswerTicketAdmin(admin.ModelAdmin):
    list_display = [
        "id", "__str__", "status", "jcreated",
    ]
    search_fields = ["message", ]
    list_filter = ["status", ]
    list_editable = ["status", ]
    actions = [make_True_Status, make_False_Status]


# admin.site.register(AnswerTicket, AnswerTicketAdmin)
