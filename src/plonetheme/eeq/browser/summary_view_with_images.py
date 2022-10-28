from DateTime import DateTime

DATE_FORMAT = '%B %-d, %Y'
TIME_FORMAT = '%-I:%M%p'


class BrainDateInfo(object):
    """Utility view to get the date of the object to display in the
    "Summary View With Images" view.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def date(self):
        if self.context.PortalType() in ['Event', 'plonetheme.eeq.eventlink']:
            # It would be better to not invoke `getObject` here, but
            # the event start date is not part of the brain.
            obj = self.context.getObject()
            start_date = obj.start
            if not start_date:
                return ''
            end_date = obj.end
            layout = '{start_date} {start_time} {sep} {end_date} {end_time}'
            values = {
                'start_date': start_date.strftime(DATE_FORMAT),
                'start_time': '',
                'sep': '',
                'end_date': '',
                'end_time': '',
            }
            if not obj.whole_day:
                values['start_time'] = start_date.strftime(TIME_FORMAT)
            if end_date:
                if start_date.date() != end_date.date():
                    values['end_date'] = end_date.strftime(DATE_FORMAT)
                    values['sep'] = '-'
                if not obj.whole_day:
                    values['end_time'] = end_date.strftime(TIME_FORMAT)
                    values['sep'] = '-'
            return layout.format(**values)
        effective_date_str = self.context.EffectiveDate()
        if effective_date_str and effective_date_str != 'None':
            try:
                effective_date = DateTime(effective_date_str)
                return effective_date.strftime(DATE_FORMAT)
            except SyntaxError:
                return ''
        return ''
