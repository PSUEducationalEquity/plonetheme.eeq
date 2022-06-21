from DateTime import DateTime

DATE_FORMAT = "%B %-d, %Y"


class BrainDateInfo(object):
    """Utility view to get the date of the object to display in the
    "Summary View With Images" view.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def date(self):
        if self.context.PortalType() == "Event":
            # It would be better to not invoke `getObject` here, but
            # the event start date is not part of the brain.
            start_date = self.context.getObject().start
            if start_date:
                return start_date.strftime(DATE_FORMAT)
            else:
                return ""
        effective_date_str = self.context.EffectiveDate()
        if effective_date_str and effective_date_str != 'None':
            try:
                effective_date = DateTime(effective_date_str)
                return effective_date.strftime(DATE_FORMAT)
            except SyntaxError:
                return ""
        return ""
