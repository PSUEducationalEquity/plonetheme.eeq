"""Python code to support event views"""
from six.moves.urllib.parse import urlencode
from Products.Five.browser import BrowserView


class CalendarLinks(BrowserView):
    def gcal_url(self):
        """Returns a Google Calendar URL for the context event.
        """
        dates = "/".join((
            self.context.start.strftime('%Y%m%dT%H%S%M'),
            self.context.end.strftime('%Y%m%dT%H%S%M')
        ))
        return "https://calendar.google.com/calendar/event?" + urlencode({
                "action": "TEMPLATE",
                "text": self.context.title,
                "sprop": self.context.absolute_url(),
                "details": self.context.description,
                "dates": dates,
                "location": self.context.location or "",
            })
