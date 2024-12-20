from django.contrib import admin

from application.Entities.order_model import Order, SelectOrderSpeaker, AssignOrderSpeaker
from application.admins.order_admin import OrderAdmin
from application.admins.order_speaker_admin import AssignOrderSpeakerAdmin, SelectOrderSpeakerAdmin

from application.Entities.channel_message_model import ChannelMessage, ChatUser, FromUser
from application.admins.message_admin import ChannelMessageAdmin, ChatUserAdmin, FromUserAdmin

from application.Entities.Speaker_model import Speaker
from application.admins.speaker_admin import SpeakerAdmin


admin.site.register(Order, OrderAdmin)
# admin.site.register(ChannelMessage, ChannelMessageAdmin)
# admin.site.register(ChatUser, ChatUserAdmin)
# admin.site.register(FromUser, FromUserAdmin)
admin.site.register(Speaker, SpeakerAdmin)
# admin.site.register(SelectOrderSpeaker, SelectOrderSpeakerAdmin)
admin.site.register(AssignOrderSpeaker, AssignOrderSpeakerAdmin)

from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
