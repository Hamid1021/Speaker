from django.contrib import admin
from application.Entities.Speaker_model import Speaker


# "name","family","age","phone","address","education_attendees","gender_attendees",
# "register_time","total_number_of_lectures","status",
# "is_deleted","jregister_time"

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ["name","family","total_number_of_lectures","jregister_time","status",]
    list_filter = ["status",]
    search_fields = ["name","family","age","phone","address","education_attendees",]
    readonly_fields = ["total_number_of_lectures",]
