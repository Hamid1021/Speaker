import os
from datetime import datetime
import jdatetime

from extensions import jalali
from django.utils import timezone
from django.core.mail import send_mail as send
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from application.send_message import send_message_to_channel


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def send_message_by_template(*args, **kwargs):
    with open("message_template.txt", "+r", encoding='utf-8') as f:
        file = f.read()
        file = file.format(
            phone = kwargs.get("phone"),
            date = kwargs.get("date"),
            time = kwargs.get("time"),
            num_attendees = kwargs.get("num_attendees"),
            gender_attendees = kwargs.get("gender_attendees"),
            education_min_attendees = kwargs.get("education_min_attendees"),
            education_max_attendees = kwargs.get("education_max_attendees"),
            city = kwargs.get("city"),
            topic = kwargs.get("topic"),
            speaker = "\n🎙 سخنران: " + str(kwargs.get("speaker")) + "\n" if kwargs.get("speaker") else "",
        )
    channel_message, channel_status = send_message_to_channel("sendMessage", kwargs.get("chatID"), kwargs.get("topic"), file)
    kwargs.get("obj").related_message = channel_message
    kwargs.get("obj").is_message_send = True
    kwargs.get("obj").save()



class SendEmail(object):
    @classmethod
    def send_mail_admin(cls, subject, recipient_list, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, "admin@toupchee.ir", recipient_list, auth_user="admin@toupchee.ir",
                auth_password="Hamid1063", html_message=html_message
            )
            return message
        except Exception:
            return ""

    @classmethod
    def send_mail_info(cls, subject, recipient_list, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, "info@toupchee.ir", recipient_list, auth_user="info@toupchee.ir",
                auth_password="Hamid1063", html_message=html_message
            )
            return message
        except Exception:
            return ""

    @classmethod
    def send_mail_customer(cls, subject, recipient_list, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, "customer@toupchee.ir", recipient_list, auth_user="customer@toupchee.ir",
                auth_password="Hamid1063", html_message=html_message
            )
            return message
        except Exception:
            return ""

    @classmethod
    def send_mail(cls, subject, from_email, recipient_list, auth_user, auth_password, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, from_email, recipient_list, auth_user=auth_user,
                auth_password=auth_password, html_message=html_message
            )
            return message
        except Exception:
            return ""


def persian_numbers_converter(string):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        string = string.replace(e, p)

    return string


def num_to_month(month_str):
    month_str = int(month_str)
    month_list = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    return month_list[month_str - 1]


def jalali_converter(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    mon = time_to_tuple[1] if time_to_tuple[1] > 9 else "0" + str(time_to_tuple[1])
    day = time_to_tuple[2] if time_to_tuple[2] > 9 else "0" + str(time_to_tuple[2])
    hou = time.hour if time.hour > 9 else "0" + str(time.hour)
    min = time.minute if time.minute > 9 else "0" + str(time.minute)
    sec = time.second if time.second > 9 else "0" + str(time.second)
    output = f"{time_to_tuple[0]}/{mon}/{day} "
    output += f" ساعت {hou}:{min}:{sec} "
    return persian_numbers_converter(output)


def jalali_converter_date(time):
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    mon = time_to_tuple[1] if time_to_tuple[1] > 9 else "0" + str(time_to_tuple[1])
    day = time_to_tuple[2] if time_to_tuple[2] > 9 else "0" + str(time_to_tuple[2])
    output = f"{time_to_tuple[0]}/{mon}/{day}"
    return persian_numbers_converter(output)


def jalali_converter_en(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    mon = time_to_tuple[1] if time_to_tuple[1] > 9 else "0" + str(time_to_tuple[1])
    day = time_to_tuple[2] if time_to_tuple[2] > 9 else "0" + str(time_to_tuple[2])
    hou = time.hour if time.hour > 9 else "0" + str(time.hour)
    min = time.minute if time.minute > 9 else "0" + str(time.minute)
    sec = time.second if time.second > 9 else "0" + str(time.second)
    output = f"{time_to_tuple[0]}/{mon}/{day} "
    output += f"{hou}:{min}:{sec}"
    return output


def jalali_get_day(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{time_to_tuple[2]}"

    return persian_numbers_converter(output)


def jalali_get_day_title(dt):
    day_map = {
        "Saturday": "شنبه",
        "Sunday": "یکشنبه",
        "Monday": "دوشنبه",
        "Tuesday": "سه‌شنبه",
        "Wednesday": "چهارشنبه",
        "Thursday": "پنجشنبه",
        "Friday": "جمعه",
    }
    jalali_date = jdatetime.datetime.fromgregorian(datetime=dt)

    jalali_day_name = jalali_date.strftime('%A')

    return day_map[jalali_day_name]


def jalali_get_month(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{num_to_month(time_to_tuple[1])}"

    return persian_numbers_converter(output)


def jalali_get_year(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{time_to_tuple[0]}"

    return persian_numbers_converter(output)


def date_comper(date_1, date_2):
    """Get Tow Date And if Date_1 Is Bigger Than Date_2 Return True Else Return False"""
    date_1 = timezone.localtime(date_1)
    date_2 = timezone.localtime(date_2)
    d_1 = datetime(
        year=date_1.year,
        month=date_1.month,
        day=date_1.day,
        hour=date_1.hour,
        minute=date_1.minute,
        second=date_1.second,
    )
    d_2 = datetime(
        year=date_2.year,
        month=date_2.month,
        day=date_2.day,
        hour=date_2.hour,
        minute=date_2.minute,
        second=date_2.second,
    )
    if d_1 > d_2:
        return True
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def gregorian_converter(time:str):
    year, month, day = jalali.Persian(time.split(" ")[0]).gregorian_tuple()
    hour, minute, second = [int(i) for i in time.split(" ")[1].split(":")]
    return datetime(year, month, day, hour, minute, second)


def gregorian_converter_date(time:str, spliter = "/"):
    year, month, day = jalali.Persian(*[int(x) for x in time.split(spliter)]).gregorian_tuple()
    return datetime(year, month, day, 0, 0, 0)