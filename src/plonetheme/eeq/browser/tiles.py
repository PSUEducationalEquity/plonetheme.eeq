from plonetheme.eeq import _
from jazkarta.tesserae.utils import uuidToObject
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import CatalogSource
try:
    from plone.app.widgets.dx import RelatedItemsWidget
    from plone.autoform import directives as form
except ImportError:
    RelatedItemsWidget = None
from plone.memoize.view import memoize
from plone.tiles import Tile
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

    use_date_range = schema.Bool(
        title=_(u'Use date range'),
        description="Optionally, restrict display date range by providing publication and expiration dates",
        default=False,
        required=False
    )

    publication_date = schema.Datetime(
        description="Display tile from this date",
        title=_(u'Publication Date'),
        required=False
    )

    expiration_date = schema.Datetime(
        description="Display tile until this date",
        title=_(u'Expiration Date'),
        required=False
    )

    # can add more alert styles here 1/3
    style = schema.Choice(
        title=_(u'Select alert style'),
        default=u'primary',
        values=(u'primary', 
                u'warning'),
    )


class AlertTile(Tile):
    """ Custom alert tile with style selection and optional url link
    """

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
        if self.data.get('use_date_range'):

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
