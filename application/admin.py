from django.contrib import admin

from application.Entities.order_model import Order, OrderSpeaker
from application.admins.order_admin import OrderAdmin

from application.Entities.channel_message_model import ChannelMessage, ChatUser, FromUser
from application.admins.message_admin import ChannelMessageAdmin, ChatUserAdmin, FromUserAdmin

from application.Entities.Speaker_model import Speaker
from application.admins.speaker_admin import SpeakerAdmin


admin.site.register(Order, OrderAdmin)
admin.site.register(ChannelMessage, ChannelMessageAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(FromUser, FromUserAdmin)
admin.site.register(Speaker, SpeakerAdmin)


class OrderSpeakerAdmin(admin.ModelAdmin):
    readonly_fields = ["date"]
admin.site.register(OrderSpeaker, OrderSpeakerAdmin)