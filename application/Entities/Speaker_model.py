from django.db import models
from extensions.utils import jalali_converter


class Speaker(models.Model):
    gender_attendees_choices = (
        ("m", "مرد"),
        ("w", "زن"),
    )
    name = models.CharField("نام", null=True, blank=True, default="", max_length=255)
    family = models.CharField("نام خانوادگی", null=True, blank=True, max_length=255)
    age = models.IntegerField("سن", null=True, blank=True, default=0)
    phone = models.CharField("شماره همراه", null=True, blank=True, default="+98912345689", max_length=12)
    address = models.CharField("آدرس", null=True, blank=True, default="ثبت نشده", max_length=500)
    education_attendees = models.CharField("تحصیلات سخنران", null=True, blank=True, default="نا مشخص", max_length=255)
    gender_attendees = models.CharField("جنسیت", null=False, blank=False, default="m", max_length=1, choices=gender_attendees_choices)
    register_time = models.DateTimeField("زمان ثبت نام", null=True, blank=True, auto_now_add=True)
    total_number_of_lectures = models.IntegerField("تعداد کل روضه های انجام شده", null=True, blank=True, default=0)
    today_number_of_lectures = models.IntegerField('روضه های انجام شده امروز', null=True, blank=True, default=0)
    status = models.BooleanField("وضعیت", null=False, blank=False, default=True)
    is_deleted = models.BooleanField("حذف شده؟", null=False, blank=False, default=False)

    def jregister_time(self):
        return jalali_converter(self.register_time)
    jregister_time.short_description = "زمان ثبت نام"

    def __str__(self):
        return f"{self.name} - {self.family}"

    def get_fullname(self):
        return f"{self.name} {self.family}"

    class Meta:
        verbose_name = "سخنران"
        verbose_name_plural = "سخنران ها"
        ordering = ["name", 'family', "age", "total_number_of_lectures"]

