from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
# from application.send_message import edit_message_from_channel


@admin.action(description="تغییر موارد به اختصاص داده نشده", permissions=["change"])
def make_as_not_assign(modeladmin, request, queryset):
    queryset.update(is_assign=False)


@admin.action(description="تغییر موارد به اختصاص داده شده", permissions=["change"])
def make_as_assign(modeladmin, request, queryset):
    queryset.update(is_assign=True)

# "phone", "date", "jdate", "time", "num_attendees", "gender_attendees", "education_min_attendees",
# "education_max_attendees", "city", "topic", "status", "related_message", "is_assign", "is_message_send"
class OrderAdmin(admin.ModelAdmin):
    actions = [make_as_not_assign, make_as_assign]
    list_display = ["topic", "phone", "jdate", "time", "num_attendees", "city", "status", "is_assign",]
    search_fields = [
        "phone", "date", "time", "num_attendees",
        "education_min_attendees", "education_max_attendees", "city", "topic",
    ]
    list_filter = [
        "status", "is_assign",
    ]
    readonly_fields = [
        "phone", "date", "time", "num_attendees", "education_min_attendees",
        "education_max_attendees", "city", "topic", "related_message",
        "gender_attendees", "is_assign", "status","is_message_send", 
    ]
    def has_add_permission(self, request, obj=None):
        return False
    # list_editable = ["status", "is_assign"]

    # def save_model(self, request: HttpRequest, obj, form: ModelForm, change: bool) -> None:
    #     if change:
    #         with open("message_template.txt", "+r", encoding='utf-8') as f:
    #             file = f.read()
    #             file = file.format(
    #                 phone = obj.phone,
    #                 date = obj.date,
    #                 time = obj.time,
    #                 num_attendees = obj.num_attendees,
    #                 gender_attendees = obj.gender_attendees,
    #                 education_min_attendees = obj.education_min_attendees,
    #                 education_max_attendees = obj.education_max_attendees,
    #                 city = obj.city,
    #                 topic = obj.topic,
    #                 status = "انجام شد" if obj.status == "c" else "انجام نشده"
    #             )
    #             channel_status = edit_message_from_channel(
    #                 message_id=obj.related_message.message_id, new_text=file, unix_time=float(obj.related_message.date)
    #             )
    #     return super().save_model(request, obj, form, change)
    
