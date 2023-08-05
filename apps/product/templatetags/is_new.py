import datetime
from django.template import Library
import pytz


register = Library()

@register.filter_function
def is_new(queryset):
    utc = pytz.UTC
    last_month = datetime.datetime.now() - datetime.timedelta(weeks=4)
    if queryset.publish_date >= utc.localize(last_month):
        return True
    return False
