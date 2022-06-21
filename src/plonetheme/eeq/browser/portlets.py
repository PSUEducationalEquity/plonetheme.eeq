from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer

SOCIAL_FIELDS = (
    ('facebook', 'facebook_url'),
    ('twitter', 'twitter_url'),
    ('instagram', 'instagram_url'),
    ('youtube', 'youtube_url'),
    ('linkedin', 'linkedin_url'),
)


class ISocialLinksPortlet(IPortletDataProvider):
    """A portlet which can render a login form.
    """


@implementer(ISocialLinksPortlet)
class SocialLinksAssignment(base.Assignment):

    title = u'Social Media Links'


class SocialLinksRenderer(base.Renderer):
    """Portlet renderer for archive navigation"""
    render = ViewPageTemplateFile('templates/social_links_portlet.pt')
    links = ()

    def update(self):
        links = []
        for name, fname in SOCIAL_FIELDS:
            val = getattr(self.context, fname, None)
            if val:
                links.append((name, val))
        self.links = tuple(links)

    @property
    def available(self):
        for name, fname in SOCIAL_FIELDS:
            if getattr(self.context, fname, None):
                return True
        return False


class SocialLinksAddForm(base.NullAddForm):

    def create(self):
        return SocialLinksAssignment()
