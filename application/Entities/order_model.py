from typing import Iterable
from django.db import models
from application.Entities.channel_message_model import ChannelMessage
from extensions.utils import jalali_converter_date, jalali_get_day_title, jalali_converter
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
    
    def get_all_not_selected(self):
        return self.get_queryset().filter(is_selected=False)
    
    def get_all_selected(self):
        return self.get_queryset().filter(is_selected=True)

    def make_as_selected(self, order_pk):
        try:
            obj = self.get_queryset().get(pk=order_pk)
            obj.is_selected = True
            obj.save()
            return True
        except:
            return False
        
    def make_as_not_selected(self, order_pk):
        try:
            obj = self.get_queryset().get(pk=order_pk)
            obj.is_selected = False
            obj.save()
            return True
        except:
            return False

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
    is_message_send = models.BooleanField("پیام ارسال شده؟", null=False, blank=False, default=False)
    is_selected = models.BooleanField("انتخاب شده", null=False, blank=False, default=False)
    
    def __str__(self):
        return f"{self.topic} - {jalali_converter_date(self.date)} - {self.time}"

    def jdate(self):
        return jalali_converter_date(self.date)
    jdate.short_description = "تاریخ"


    def daytitle(self):
        return jalali_get_day_title(self.date)
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات ثبت شده"
        ordering = ["-pk", 'date', "time"]

    objects = OrderManage()


class OrderSpeaker(models.Model):
    speaker = models.ForeignKey('Speaker', on_delete=models.DO_NOTHING, verbose_name="سخنران")
    order = models.ManyToManyField('Order', verbose_name="سفارش", related_name="order_set", null=True, blank=True)
    date = models.DateTimeField("زمان ثبت", default=timezone.now, null=True, blank=True)
    related_message = models.ForeignKey('ChannelMessage', on_delete=models.DO_NOTHING, null=True, verbose_name="پیام مرتبط")
    is_message_send = models.BooleanField("پیام ارسال شده؟", null=False, blank=False, default=False)

    def jdate(self):
        return jalali_converter(self.date)
    jdate.short_description = "زمان ثبت شمسی"

    def __str__(self):
        return f"{self.order} - {self.speaker} - {self.date}"
    class Meta:
        verbose_name = "سخنران_سفارش"
        verbose_name_plural = "اختصاص سفارش به سخنران"
