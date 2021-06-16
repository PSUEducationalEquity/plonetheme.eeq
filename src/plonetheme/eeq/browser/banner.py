from datetime import date
from zope.component import getUtility
from plone.app.layout.viewlets import common as base
from plone.registry.interfaces import IRegistry
from plone import api
from plonetheme.eeq.interfaces import ISettings


class AboveHeaderBanner(base.ViewletBase):
    def render(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings, False)

        today = date.today()
        if settings.top_banner_publication_date and today < settings.top_banner_publication_date:
            return ""
        if settings.top_banner_retire_date and today >= settings.top_banner_retire_date:
            return ""
        if not settings.top_banner_body:
            return ""
        url = api.portal.get().absolute_url()
        return '<div id="AboveHeaderBanner">' + settings.top_banner_body.replace("${portal_url}", url) + "</div>"
