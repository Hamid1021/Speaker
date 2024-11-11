from django.db import models
from application.Entities.channel_message_model import ChannelMessage

class OrderManage(models.Manager):
    def tryCreateObject(self, *args, **kwargs):
        try:
            obj = self.create(*args, **kwargs)
            if obj:
                return obj, True, "سفارش با موفقیت ذخیره شد"
            raise Exception
        except Exception as e:
            return obj, False, "مشکلی در ایجاد سفارش  وجود دارد"


class Order(models.Model):
    status_choice = (
        ("uc", "انجام نشده"), ("c", "انجام شده")
    )
    phone = models.CharField("شماره همراه", null=True, blank=True, default="", max_length=15)
    date = models.DateField("تاریخ", null=True, blank=True, auto_now_add=True)
    time = models.TimeField("زمان", null=True, blank=True, auto_now_add=True)
    num_attendees = models.IntegerField("تعداد اعضای جلسه", null=True, blank=True, default=0,)
    gender_attendees = models.CharField("جنسیت حضار", null=True, blank=True, default="", max_length=255)
    education_min_attendees = models.CharField("حداقل سواد حاضران", null=True, blank=True, default="", max_length=255)
    education_max_attendees = models.CharField("حداکثر سواد حاضران", null=True, blank=True, default="", max_length=255)
    city = models.CharField("شهر", null=True, blank=True, default="", max_length=255)
    topic = models.CharField("موضوع روضه", null=True, blank=True, default="", max_length=255)
    status = models.CharField("وضعیت", null=False, blank=False, default="uc", choices=status_choice, max_length=2)
    related_message = models.ForeignKey('ChannelMessage', on_delete=models.DO_NOTHING, null=True, verbose_name="پیام مرتبط")

    def __str__(self):
        return f"{self.topic} - {self.phone} - {self.date} - {self.time}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات ثبت شده"
        ordering = ["status", '-date', "-time"]

    objects = OrderManage()