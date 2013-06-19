import qtmessage.TriggerParser as TriggerParser
import simplejson
import datetime
from qtmessage.models import Message, InitFile
from lxml import etree as ET

def main():
    f = InitFile.objects.latest('id')
    tree = ET.parse(f.doc)
    if tree:
        for i in tree.findall('survey'):
            #surveyname= i.attrib['description']
            xform = i.find('xform').attrib['id']
            trigger_list=TriggerParser.collectXMLTriggers(i)

            now = datetime.datetime.now()
            today = '%02d' % now.month+ '%02d' % now.day
            timetriggers = {}
            timetriggers[xform]=TriggerParser.getTimeTriggersForOneDay(TriggerParser.getTimeTriggersFromSurvey(trigger_list),today)

            loctriggers = {}
            loctriggers[xform]=TriggerParser.getLocTriggersFromSurveys(trigger_list)

            for k in i.findall('group'):
                group = k.attrib['ref']
                m = Message.objects.filter(group=group)
                for t in m:
                    if t.timetrigger:
                        current = simplejson.loads(t.timetrigger)
                        if xform in current:
                            current[xform] = current[xform]+' '+timetriggers[xform]
                        else:
                            current[xform] = timetriggers[xform]
                        t.timetrigger = simplejson.dumps(current)
                        t.save()
                    else:
                        t.timetrigger = simplejson.dumps(timetriggers)
                        t.save()

                    if t.loctrigger:
                        current = simplejson.loads(t.loctrigger)
                        if xform in current:
                            current[xform] = current[xform].update(loctriggers[xform])
                        else:
                            current[xform] = loctriggers[xform]
                        t.loctrigger = simplejson.dumps(current)
                        t.save()
                    else:
                        t.loctrigger = simplejson.dumps(loctriggers)
                        t.save()

            for l in i.findall('user'):
                m = Message.objects.filter(user__username=l.attrib['ref'])
                for t in m:
                    if t.timetrigger:
                        current = simplejson.loads(t.timetrigger)
                        if xform in current:
                            current[xform] = current[xform]+' '+timetriggers[xform]
                        else:
                            current[xform] = timetriggers[xform]
                        t.timetrigger = simplejson.dumps(current)
                        t.save()
                    else:
                        t.timetrigger = simplejson.dumps(timetriggers)
                        t.save()

                    if t.loctrigger:
                        current = simplejson.loads(t.loctrigger)
                        if xform in current:
                            current[xform] = current[xform].update(loctriggers[xform])
                        else:
                            current[xform] = loctriggers[xform]
                        t.loctrigger = simplejson.dumps(current)
                        t.save()
                    else:
                        t.loctrigger = simplejson.dumps(loctriggers)
                        t.save()


if __name__ == 'main':
    main()