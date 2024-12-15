from django.contrib import admin
import datetime
import pytz
import jdatetime

from application.utils import convert_unix_to_jalali


# "message_id", "date", "text", "status", "from_user", "chat_user", 
class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = [
        "message_id", "get_short_decs", "get_unix_time", "status", "get_from_user", "get_from_chat", 
    ]
    search_fields = [
        "message_id", "text", "from_user__username", "chat_user__username", 
        "from_user__first_name", "from_user__last_name",
    ]
    list_filter = [
       "status",
    ]
    readonly_fields = [
        "message_id", "date", "text", "status", "from_user", "chat_user", 
    ]

    def get_short_decs(self, obj):
        return f"{obj.text[:70]}" + "...."

    def get_unix_time(self, obj):
        return convert_unix_to_jalali(float(obj.date))
    get_unix_time.short_description = "زمان ارسال"
    
    def get_from_user(self, obj):
        return obj.from_user.username
    get_from_user.short_description = "کاربر"
    
    def get_from_chat(self, obj):
        return obj.chat_user.username
    get_from_chat.short_description = "چت"

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# "m_id", "is_bot", "first_name", "last_name", "username", "can_join_groups", 
# "can_read_all_group_messages", "supports_inline_queries", 
class FromUserAdmin(admin.ModelAdmin):
    list_display = ["m_id", "first_name", "last_name", "username",]
    search_fields = [
        "m_id", "first_name", "last_name", "username",
    ]
    list_filter = [
       "can_join_groups", "can_read_all_group_messages", "supports_inline_queries", 
    ]
    readonly_fields = [
       "m_id", "is_bot", "first_name", "last_name", "username", "can_join_groups", 
        "can_read_all_group_messages", "supports_inline_queries", 
    ]

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

# "m_id","username","m_type",
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ["m_id","username","m_type",]
    search_fields = [
        "m_id","username","m_type",
    ]
    readonly_fields = [
        "m_id","username","m_type",
    ]

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False