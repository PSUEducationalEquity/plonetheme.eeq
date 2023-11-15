"""Python code to support event views"""
from six.moves.urllib.parse import urlencode
from Products.Five.browser import BrowserView


class PSUEventHelpers(BrowserView):
    """Helper functions for event content type"""

    def gcal_url(self):
        """Returns a Google Calendar URL for the context event"""
        dates = "/".join((
            self.context.start.strftime('%Y%m%dT%H%S%M'),
            self.context.end.strftime('%Y%m%dT%H%S%M')
        ))
        try:
            event_location = self.context.location
        except AttributeError:
            try:
                event_location = self.context.remoteUrl
            except AttributeError:
                event_location = ""
        return "https://calendar.google.com/calendar/event?" + urlencode({
                "action": "TEMPLATE",
                "text": self.context.title,
                "sprop": self.context.absolute_url(),
                "details": self.context.description,
                "dates": dates,
                "location": event_location,
            })

    def format_time(self, time):
        """Format the given `time` (a datetime object)

        Examples: '7:00 p.m.' / '11:00 a.m.' / '9:00 a.m.' / 'All day'
        """
        if self.context.whole_day:
            return 'All day'
        formatted_time = time.strftime('%I:%M')
        if formatted_time.startswith('0'):
            formatted_time = formatted_time[1:]
        am_or_pm = time.strftime('%p').lower().replace("am", "a.m.").replace("pm", "p.m.")
        return formatted_time + " " + am_or_pm
