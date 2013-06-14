from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

def collectXMLTriggers(survey):
    trigger_dict = {}
    trigger_list = []
    for item in survey.findall("trigger"):
        child = item[0]
        if child.tag == "geoTrigger":
            trigger_dict[child.tag] = child.attrib
        elif child.tag == "timeTrigger":
            time_dict = {}
            time = child[0]
            start_date_time = time.attrib
            recur_dict = {}
            recur = child[1]
            freq = recur[0]
            recurType = freq[0]
            if recurType.tag == 'WEEKLY':
                if recurType[0].tag == 'byweekly':
                    interval = recurType[0].attrib['interval']
                    recur_dict["freq"] = {"type": 'byweekly', "interval": interval}
            elif recurType.tag == 'DAILY':
                days = []
                if recurType[0].tag == 'byweekday':
                    for day_of_week in recurType:
                        days.append(day_of_week.attrib['weekdays'])
                        recur_dict["freq"] = {"type": 'byweekday', "weekdays": days}
                elif recurType[0].tag == 'bydaily':
                    recur_dict["freq"] = {"type": 'bydaily', "interval": recurType[0].attrib['interval']}
            elif recurType.tag == 'HOURLY':
                hours = []
                if recurType[0].tag == 'byhourly':
                    recur_dict["freq"] = {"type": 'byhourly', 'interval': recurType[0].attrib['interval']}
                else:
                    for hour_of_day in recurType:
                        hours.append(hour_of_day.attrib['byhour'])
                        recur_dict["freq"] = {"type": 'byhour', "hours": hours}
                        count = freq.attrib['count']
                        recur_dict["count"] = count
                        trigger_dict[child.tag] = {"time": start_date_time, "recur": recur_dict}
            elif child.tag == "ASA":
                trigger_dict[child.tag] = child.text
            else:
                pass #Unknown Trigger
        trigger_list.append(trigger_dict)
        trigger_dict={}

    return trigger_list

def getTimeTriggersFromSurvey(survey_trigger):
    trigger_dict = {}
    for trigger in survey_trigger:
        if 'timeTrigger' in trigger:
            t = trigger['timeTrigger']
            parsed_trigger = parseTimeTriggerToDay(t)
            timeTriggertoJSONDays(parsed_trigger)
            trigger_dict[t['time']['datetime']] = timeTriggertoJSONDays(parsed_trigger)
    return trigger_dict

def timeTriggertoJSONDays(time_trigger):
    trigger_list = []
    for i in time_trigger:
        for j in i:
            trigger_list.append({'%02d' % j.month+ '%02d' % j.day : '%02d' % j.hour + '%02d' % j.minute})
    return trigger_list


def parseTimeTriggerToDay(time_trigger):
    """
    This function takes in one trigger and
    returns the daily trigger times as a dict with the key
    being the number of days from the start day.
    """
    TODAY = date.today()
    result = []
    recur_def = time_trigger['recur']
    dtstart_t = parse(time_trigger['time']['datetime'])
    count_t = int(recur_def['count'])
    freqType = recur_def['freq']['type']

    if freqType == 'hourly':
        freqVals = recur_def['freq']['interval']['byhour'].split(" ")
        #Same times every day
        for val in range(1, count_t, 1):
            result.append(freqVals)
    elif freqType == 'byhour':
        #dateutil differs from the RFC here, so some tweaking is necessary
        byhour_t = map(int, recur_def['freq']['hours'])
        result.append(list((rrule(DAILY, count=len(byhour_t*count_t), byhour=byhour_t, dtstart=dtstart_t))))
    elif freqType == 'byweekly':
        interval_t = int(recur_def['freq']['interval'])
        result.append(list(rrule(WEEKLY, count=count_t, interval=interval_t, dtstart=dtstart_t)))
    elif freqType == 'byweekno':
        byweekno_t = tuple(map(int, recur_def['freq']['weeknolist']))
        result.append(list(rrule(WEEKLY, byweekno=byweekno_t, count=count_t, dtstart=dtstart_t)))
    elif freqType == 'bydaily':
        interval_t = int(recur_def['freq']['interval'])
        result.append(list(rrule(DAILY, count=count_t, interval=interval_t, dtstart=dtstart_t)))
    elif freqType == 'byweekday':
        byweekday_t = tuple(map(eval, recur_def['freq']['weekdays']))
        result.append(list(rrule(WEEKLY, count=count_t, byweekday=byweekday_t, dtstart=dtstart_t)))
    return result

def getDay(trigger, day):
    for days in trigger:
        return days[day] in trigger

def getTimeTriggersForOneDay(res, day):
    trigger=""
    for triggers in dict.values(res):
        for t in triggers:
            h = lambda x: x in t
            if h(day):
                trigger += t[day]+' '
    return trigger.strip()

def getLocTriggersFromSurveys(survey_trigger):
    trigger_dict = {}
    for trigger in survey_trigger:
        if 'geoTrigger' in trigger:
            g = trigger['geoTrigger']
            trigger_dict[g['name']] = str(g['lat'])+','+str(g['lon'])+','+str(g['radius'])+','
            if g['event']=='exit':
                trigger_dict[g['name']] += str(2)
            else:  trigger_dict[g['name']] += str(1)
    return trigger_dict

