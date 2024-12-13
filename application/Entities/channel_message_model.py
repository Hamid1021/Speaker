from django.db import models


class ChannelMessage(models.Model):
    status_choice = (
        ("s", "ارسال شد"), ("us", "ارسال نشد")
    )
    message_id = models.IntegerField("message_id", null=True, blank=True, default=0)
    date = models.CharField("date", null=True, blank=True, max_length=12)
    text = models.TextField("text", null=True, blank=True, default="")
    status = models.CharField("ok", null=True, blank=True, default="us", choices=status_choice, max_length=2)
    from_user = models.ForeignKey('FromUser', on_delete=models.DO_NOTHING)
    chat_user = models.ForeignKey('ChatUser', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.message_id} - {self.from_user.first_name} - {self.from_user.last_name} - {self.from_user.username}"

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام های ارسال شده"



class FromUser(models.Model):
    m_id = models.IntegerField("id", null=True, blank=True, default=0, unique=True)
    is_bot = models.BooleanField("is_bot", null=True, blank=True, default=False)
    first_name = models.CharField("first_name", null=True, blank=True, default="", max_length=255)
    last_name = models.CharField("last_name", null=True, blank=True, default="", max_length=255)
    username = models.CharField("username", null=True, blank=True, default="", max_length=255)
    can_join_groups = models.BooleanField("can_join_groups", null=True, blank=True)
    can_read_all_group_messages = models.BooleanField("can_read_all_group_messages", null=True, blank=True)
    supports_inline_queries = models.BooleanField("supports_inline_queries", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.username}"

    class Meta:
        verbose_name = "مخاطب"
        verbose_name_plural = "مخاطبین"


class ChatUser(models.Model):
    m_id = models.IntegerField("id", null=True, blank=True, default=0, unique=True)
    username = models.CharField("username", null=True, blank=True, default="", max_length=255)
    m_type = models.CharField("type", null=True, blank=True, default="", max_length=255)

    def __str__(self):
        return f"{self.username} - {self.m_type}"

    class Meta:
        verbose_name = "چت"
        verbose_name_plural = "چت مخاطبین"
