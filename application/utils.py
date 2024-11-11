import datetime
import pytz
import jdatetime


def convert_unix_to_jalali(unix_time):
    # تبدیل زمان یونیکس به datetime
    dt = datetime.datetime.fromtimestamp(unix_time, pytz.UTC)
    # تبدیل datetime به تاریخ و زمان شمسی
    jalali_date = jdatetime.datetime.fromgregorian(datetime=dt)
    return jalali_date.strftime('%Y/%m/%d %H:%M:%S')