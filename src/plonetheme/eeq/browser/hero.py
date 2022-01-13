from plone.app.layout.viewlets import common as base
from plone import api


class HeroImage(base.ViewletBase):
    def render(self):
        context = self.get_folder_or_office_context()
        if context is None:
            portal = api.portal.get()
            try:
                url = portal.assets.default_hero.absolute_url() + "/@@images/image/psu_hero"
            except AttributeError:
                url = portal.absolute_url() + "/++theme++psu-educational-equity/images/hero-home.jpg"
        else:
            url = context.absolute_url() + "/@@images/image/psu_hero"
        return f"""
        <span id="office-leadimage">
            <img alt="" id="hero-image" class="w-100 d-none d-md-block" src="{url}" />
        </span>
        """

    def get_folder_or_office_context(self):
        """Walk up the acquisition chain until we find
        an office or folder that has a lead image specified.
        """
        context = self.context
        while hasattr(context, "portal_type"):
            if context.portal_type in ["plonetheme.eeq.office", "Folder"]:
                if hasattr(context, "image") and context.image:
                    return context
            context = context.aq_parent
        return None
