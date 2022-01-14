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

        now = DateTime()
        self.left_links = [{
                "title": "Home",
                "url": office.absolute_url()
        }] + [
            {
                "title": obj.title,
                "url": obj.absolute_url()
            }
            for obj in office.listFolderContents()
            if not obj.exclude_from_nav
            and obj.isEffective(now)
        ]
        self.right_links = [
            {
                "title": obj.to_object.title,
                "url": obj.to_object.absolute_url()
            }
            for obj in office.navigation_links or []
            if obj.to_object
        ]
        return self.index()

    def office_context(self):
        """Walk up hierarchy to find the office context.
        """
        context = self.context
        while hasattr(context, "portal_type"):
            if context.portal_type == 'plonetheme.eeq.office':
                return context
            context = context.aq_parent
        return None
