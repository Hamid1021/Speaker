from django.contrib import admin
from application.Entities.Speaker_model import Speaker


@admin.action(description="تغییر موارد به فعال", permissions=["change"])
def make_as_active(modeladmin, request, queryset):
    queryset.update(status=True)


@admin.action(description="تغییر موارد به غیر فعال", permissions=["change"])
def make_as_not_activen(modeladmin, request, queryset):
    queryset.update(status=False)


# "name","family","age","phone","address","education_attendees","gender_attendees",
# "register_time","total_number_of_lectures","status",
# "is_deleted","jregister_time"

class SpeakerAdmin(admin.ModelAdmin):
    actions = [make_as_active, make_as_not_activen]
    list_display = ["name","family","total_number_of_lectures","jregister_time","status",]
    list_filter = ["status",]
    search_fields = ["name","family","age","phone","address","education_attendees",]
    readonly_fields = ["total_number_of_lectures",]
