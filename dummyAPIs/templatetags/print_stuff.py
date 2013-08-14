from django import template
import datetime
from dummyAPIs.models import HistoryTransaction, LicensePlate, Participant
register = template.Library()

def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)

register.filter(print_timestamp)

@register.filter("print_rate")
def print_rate(rate,granularity):
    if granularity == '1':
        newG = '/day'
    elif granularity == '2':
        newG = '/hour'
    newR = '$'+'%.2f' % rate
    return newR + newG

@register.filter("print_cost")
def print_cost(cost):
    return '$'+'%.2f' % cost

@register.filter("print_lp")
def print_lp(participant_id):
    p = Participant.objects.filter(id=participant_id)
    if p:
        lp = p[0].licenseplate_set.filter(isActive=True)
        if lp:
            return lp[0].text
    return 'None'
