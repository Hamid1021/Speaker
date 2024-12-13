from django.contrib import admin
from application.Entities.Speaker_model import Speaker

# "order","speaker","date","is_message_send"
class AssignOrderSpeakerAdmin(admin.ModelAdmin):
    list_display = ["speaker","date","jdate","is_message_send"]
    readonly_fields = ["date", "is_message_send"]



# "order","speaker","date","is_message_send"
class SelectOrderSpeakerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "speaker",]
    readonly_fields = ["speaker"]
    filter_horizontal = ['order',]

    def save_model(self, request, obj, form, change):
        user = request.user
        get_speacker = Speaker.objects.filter(user=user).first()
        if get_speacker:
            obj.speaker = get_speacker
            obj.save()
        super().save_model(request, obj, form, change)
