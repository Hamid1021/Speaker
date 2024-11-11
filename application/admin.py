from django.contrib import admin

from application.Entities.order_model import Order
from application.admins.order_admin import OrderAdmin

from application.Entities.channel_message_model import ChannelMessage, ChatUser, FromUser
from application.admins.message_admin import ChannelMessageAdmin, ChatUserAdmin, FromUserAdmin


admin.site.register(Order, OrderAdmin)
admin.site.register(ChannelMessage, ChannelMessageAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(FromUser, FromUserAdmin)
