from typing import Iterable
from django.db import models
from application.Entities.channel_message_model import ChannelMessage
from extensions.utils import jalali_converter_date
from application.Entities.Speaker_model import Speaker
from django.utils import timezone


class OrderManage(models.Manager):
    def tryCreateObject(self, *args, **kwargs):
        try:
            obj = self.create(*args, **kwargs)
            if obj:
                return obj, True
            raise Exception
        except Exception as e:
            return obj, False


class Order(models.Model):
    status_choice = (
        ("uc", "انجام نشده"), ("c", "انجام شده")
    )
    phone = models.CharField("شماره همراه", null=True, blank=True, default="", max_length=15)
    date = models.DateField("تاریخ", null=True, blank=True)
    time = models.TimeField("زمان", null=True, blank=True)
    num_attendees = models.IntegerField("تعداد اعضای جلسه", null=True, blank=True, default=0,)
    gender_attendees = models.CharField("جنسیت حضار", null=True, blank=True, default="", max_length=255)
    education_min_attendees = models.CharField("حداقل سواد حاضران", null=True, blank=True, default="", max_length=255)
    education_max_attendees = models.CharField("حداکثر سواد حاضران", null=True, blank=True, default="", max_length=255)
    city = models.CharField("شهر", null=True, blank=True, default="", max_length=255)
    topic = models.CharField("موضوع روضه", null=True, blank=True, default="", max_length=255)
    status = models.CharField("وضعیت", null=False, blank=False, default="uc", choices=status_choice, max_length=2)
    related_message = models.ForeignKey('ChannelMessage', on_delete=models.DO_NOTHING, null=True, verbose_name="پیام مرتبط")
    is_assign = models.BooleanField("مرتبط شده؟", null=False, blank=False, default=False)

    def __str__(self):
        return f"{self.topic} - {self.phone} - {self.date} - {self.time}"

    def jdate(self):
        return jalali_converter_date(self.date)
    jdate.short_description = "تاریخ"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات ثبت شده"
        ordering = ["status", '-date', "-time"]

    objects = OrderManage()


class OrderSpeaker(models.Model):
    order = models.ForeignKey('Order', on_delete=models.DO_NOTHING, verbose_name="سفارش")
    speaker = models.ForeignKey('Speaker', on_delete=models.DO_NOTHING, verbose_name="سخنران")
    date = models.DateTimeField("زمان ثبت", default=timezone.now(), null=True, blank=True)
    related_message = models.ForeignKey('ChannelMessage', on_delete=models.DO_NOTHING, null=True, verbose_name="پیام مرتبط")
    
    def __str__(self):
        return f"{self.order} - {self.speaker} - {self.date}"
    class Meta:
        verbose_name = "سخنران_سفارش"
        verbose_name_plural = "اختصاص سفارش به سخنران"
