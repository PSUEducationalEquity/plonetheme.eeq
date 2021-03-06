from plone.app.layout.viewlets import common as base
from DateTime import DateTime


class OfficeLinks(base.ViewletBase):
    """Viewlet to render links in the office navigation bar.
    Also renders the office title and the hero banner.
    """

    def render(self):
        self.office = office = self.office_context()
        if office is None:
            return ""

        if office.abbreviation:
            office_home_link = office.abbreviation + " Home"
        else:
            office_home_link = "Home"
        self.office_nav = [{
            'title': office_home_link,
            'url': office.absolute_url()
        }] + [
            {
                'title': obj.to_object.title,
                'url': obj.to_object.absolute_url()
            }
            for obj in office.office_nav or []
            if obj.to_object
        ]
        self.audience_nav = [
            {
                'title': obj.to_object.title,
                'url': obj.to_object.absolute_url()
            }
            for obj in office.audience_nav or []
            if obj.to_object
        ]
        return self.index()

    def is_office(self):
        return getattr(self.context, 'portal_type', None) == 'plonetheme.eeq.office'

    def office_context(self):
        """Walk up hierarchy to find the office context"""
        context = self.context
        while hasattr(context, "portal_type"):
            if context.portal_type == 'plonetheme.eeq.office':
                return context
            context = context.aq_parent
        return None
