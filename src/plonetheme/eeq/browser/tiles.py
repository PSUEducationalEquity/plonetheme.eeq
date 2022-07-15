from plonetheme.eeq import _
from plonetheme.eeq.overrides import TileDatetime
from jazkarta.tesserae.utils import uuidToObject
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives as form
try:
    from plone.app.widgets.dx import RelatedItemsWidget
except ImportError:
    RelatedItemsWidget = None
from plone.app.z3cform.widget import DatetimeWidget
from plone.memoize.view import memoize
from plone.tiles import Tile
from plone.subrequest import ISubRequest
from plone.supermodel import model
from plone import api
from zExceptions import Unauthorized
from zope import schema
from datetime import datetime


class IAlertTile(model.Schema):

    title = schema.TextLine(
        title=_(u'Alert title'),
        required=False
    )

    content = schema.Text(
        title=_(u'Alert message'),
        required=False
    )

    content_uid = schema.Choice(
        title=_(u'Select an existing content item to link to (optional)'),
        required=False,
        source=CatalogSource(),
    )
    if RelatedItemsWidget is not None:
        form.widget('content_uid', RelatedItemsWidget)

    url = schema.TextLine(
        title=_(u'Specify external url to link to (optional)'),
        description="Please include full url with 'http/https' prefix",
        required=False,
    )

    publication_date = TileDatetime(
        title=_(u'Publication Date (optional)'),
        description="Display tile from this date",
        required=False
    )

    expiration_date = TileDatetime(
        title=_(u'Expiration Date (optional)'),
        description="Display tile until this date",
        required=False
    )

    form.widget('publication_date', DatetimeWidget)
    form.widget('expiration_date', DatetimeWidget)

    # can add more alert styles here 1/3
    style = schema.Choice(
        title=_(u'Select alert style'),
        default=u'primary',
        values=(u'primary',
                u'warning'),
    )


class AlertTile(Tile):
    """ Custom alert tile with style selection and optional url link"""

    template = ViewPageTemplateFile('templates/alert.pt')

    def __call__(self):
        return self.template()

    @property
    @memoize
    def title(self):
        return self.data.get('title')

    @property
    @memoize
    def content(self):
        return self.data.get('content')

    @property
    @memoize
    def content_url(self):
        uuid = self.data.get('content_uid')
        if uuid is None:
            url = self.data.get('url')
            if url is not None:
                return url

        if uuid != api.content.get_uuid(self.context):
            try:
                item = uuidToObject(uuid)
            except Unauthorized:
                item = None
                if not self.request.get('PUBLISHED'):
                    raise  # Should raise while still traversing
            if item is not None:
                return item.absolute_url()
        return None

    @property
    def alert_style(self):
        choice = self.data.get('style', 'primary')

        # setting : css class map
        # can add more alert styles here 2/3

        style_table = {'primary' : 'alert-primary',
                       'warning' : 'alert-danger'}

        # expiration check
        pub_date = self.data.get('publication_date')
        exp_date = self.data.get('expiration_date')
        now = datetime.now()
        if pub_date:
            if now < datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%S'):
                return 'alert ' + style_table[choice] + ' in-active'
        if exp_date:
            if now >= datetime.strptime(exp_date, '%Y-%m-%dT%H:%M:%S'):
                return 'alert ' + style_table[choice] + ' in-active'

        return 'alert ' + style_table[choice]


class ITwentyFiveLiveTile(model.Schema):

    web_name = schema.TextLine(
        title=_('Calendar webName'),
        description='The "webName" value for the spud.',
        required=True,
    )
    spud_type = schema.TextLine(
        title=_('Spud type'),
        description='The "spudType" value for the spud.',
        required=True,
    )
    options = schema.Text(
        title=_('Options'),
        description='Any additional key/value options for the spud.',
        required=False,
    )


class TwentyFiveLiveTile(Tile):
    """Tile for inserting calendar data from 25Live"""

    template = ViewPageTemplateFile('templates/twentyfivelive.pt')

    def __call__(self):
        return self.template()

    @property
    @memoize
    def javascript_code(self):
        """Provides the JavaScript for configuring and displaying the spud"""
        # only output the javascript if not rendering for layout editor
        if (self.request.get('_layouteditor') is True or
                ISubRequest.providedBy(self.request)):
            js = '$Trumba.addSpud({webName: "%s", spudType: "%s"' % (
                self.data.get('web_name'),
                self.data.get('spud_type'),
            )
            options = self.data.get('options')
            if options:
                options = options.strip()
                if options.endswith(','):
                    options = options[:-1]
                js += ', {}'.format(options)
            js += '});'
            return js
        else:
            return ''

    @property
    @memoize
    def spud_type(self):
        return self.data.get('spud_type')

    @property
    @memoize
    def web_name(self):
        return self.data.get('web_name')
