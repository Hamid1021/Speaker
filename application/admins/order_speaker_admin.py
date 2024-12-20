from django.contrib import admin
from application.Entities.Speaker_model import Speaker

# "order","speaker","date","is_message_send"
class AssignOrderSpeakerAdmin(admin.ModelAdmin):
    list_display = ["speaker", "get_order_topic", "get_order_city", "get_order_date", "get_order_time", "jdate","is_message_send"]
    readonly_fields = ["date", "is_message_send"]
    search_fields = [
        "speaker__name", "order__phone",
        "speaker__family", "order__topic",
        "order__city",
    ]

    def get_order_topic(self, obj):
        return obj.order.topic
    get_order_topic.short_description = "موضوع روضه"

    def get_order_city(self, obj):
        return obj.order.city
    get_order_city.short_description = "شهر"

    def get_order_date(self, obj):
        return obj.order.jdate
    get_order_date.short_description = "تاریخ"

    def get_order_time(self, obj):
        return obj.order.time
    get_order_time.short_description = "زمان"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False



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
