import datetime
from django import template
register = template.Library()

@register.filter(name='unix_to_datetime')
def unix_to_datetime(value):
    return datetime.datetime.fromtimestamp(int(value))