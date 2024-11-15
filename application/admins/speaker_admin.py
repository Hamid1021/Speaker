from django.contrib import admin
from application.Entities.Speaker_model import Speaker


# "name","family","age","phone","address","education_attendees","gender_attendees",
# "register_time","total_number_of_lectures","today_number_of_lectures","status",
# "is_deleted","jregister_time"

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ["name","family","total_number_of_lectures","today_number_of_lectures","gender_attendees","jregister_time","status", "is_deleted",]
    list_filter = ["status", "is_deleted", "gender_attendees",]
    search_fields = ["name","family","age","phone","address","education_attendees",]
    readonly_fields = ["total_number_of_lectures","today_number_of_lectures",]
    list_editable = ["today_number_of_lectures"]
