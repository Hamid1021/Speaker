#  templatetags/jalali_filters.py
from django import template
from extensions.utils import jalali_converter_date, gregorian_converter_date

register = template.Library()

@register.filter(name='jalali_date')
def jalali_date(value):
    return jalali_converter_date(value)


@register.filter(name='check_selected_date')
def check_selected_date(self, value):
    if (str(value)) == (self):
        return True
    return False
