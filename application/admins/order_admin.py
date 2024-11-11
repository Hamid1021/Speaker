from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
# from application.send_message import edit_message_from_channel


# "phone", "date", "time", "num_attendees", "gender_attendees", "education_min_attendees",
# "education_max_attendees", "city", "topic", "status", "related_message"
class OrderAdmin(admin.ModelAdmin):
    list_display = ["topic", "phone", "date", "time", "num_attendees", "gender_attendees", "city", "status",]
    search_fields = [
        "phone", "date", "time", "num_attendees", "gender_attendees",
        "education_min_attendees", "education_max_attendees", "city", "topic",
    ]
    list_filter = [
        "status",
    ]
    readonly_fields = [
        "phone", "date", "time", "num_attendees", "gender_attendees", "education_min_attendees",
        "education_max_attendees", "city", "topic", "related_message"
    ]
    list_editable = ["status",]

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
    
