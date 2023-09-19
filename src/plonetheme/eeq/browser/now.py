"""Python code to support event views"""
from Products.Five.browser import BrowserView
from datetime import datetime


class Now(BrowserView):
    """Provides the current date/time (because apparently that's hard)"""
    def now(self):
        return datetime.now()

    def year(self):
        return datetime.now().strftime('%Y')
