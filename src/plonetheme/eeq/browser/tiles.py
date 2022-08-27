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
from plone.app.textfield import RichText
from plone.app.z3cform.widget import DatetimeWidget
from plone.memoize.view import memoize
from plone.tiles import Tile
from plone.subrequest import ISubRequest
from plone.supermodel import model
from plone import api
from zExceptions import Unauthorized
from zope import schema
from datetime import datetime, timedelta
from DateTime import DateTime


DATE_FORMAT = '%B %-d, %Y'
TIME_FORMAT = '%-I:%M%p'


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


class ICollectionChronology(model.Schema):

    content_uid = schema.Choice(
        title=_(u'Select an existing collection'),
        required=True,
        source=CatalogSource(
            object_provides=(
                'plone.app.contenttypes.behaviors.collection.IFolder',
                'plone.app.contenttypes.behaviors.collection.ICollection',
                'plone.app.contenttypes.behaviors.collection.ISyndicatableCollection',
                'plone.app.collection.interfaces.ICollection',
            )
        ),
    )
    if RelatedItemsWidget is not None:
        form.widget('content_uid', RelatedItemsWidget)

    show_title = schema.Bool(
        title=_(u'Show collection title'),
        default=True,
    )

    show_description = schema.Bool(
        title=_(u'Show collection description'),
        default=False,
    )

    show_lead_image = schema.Bool(
        title=_(u'Show lead image as background'),
        default=False,
    )

    limit = schema.Int(
        title=_(u'Number of items to display'),
        default=3,
        min=1,
    )


class CollectionChronology(Tile):
    """Tile for displaying collection items with chronological data"""

    template = ViewPageTemplateFile('templates/collectionchronology.pt')

    def __call__(self):
        self.update()
        return self.template()

    def update(self):
        limit = self.data.get('limit', 3)
        self.results = []
        for b in self.content.results(batch=False, b_size=limit)[:limit]:
            try:
                obj = b.getObject()
                self.results.append(obj)
            except Unauthorized:
                continue
        self.show_title = self.data.get('show_title', False)
        self.show_description = self.data.get('show_description', False)
        self.show_lead_image = self.data.get('show_lead_image', False)

    @property
    @memoize
    def content(self):
        uuid = self.data.get('content_uid')
        if uuid != api.content.get_uuid(self.context):
            try:
                item = uuidToObject(uuid)
            except Unauthorized:
                item = None
                if not self.request.get('PUBLISHED'):
                    raise  # Should raise while still traversing
            if item is not None:
                return item
        return None

    def day(self, obj=None):
        start_date = self._start_date(obj)
        end_date = self._end_date(obj)
        result = start_date.strftime('%-d')
        try:
            end_day = end_date.strftime('%-d')
        except AttributeError:
            pass
        else:
            if result != end_day:
                result += '-' + end_day
        return result

    def _end_date(self, obj=None):
        content = obj or self.content
        try:
            return content.end
        except AttributeError:
            return None

    def image_url(self, obj=None, scale_name="preview"):
        content = obj or self.content
        if content is None:
            return

        images_view = content.unrestrictedTraverse('@@images')

        for field_name in ['image', 'leadImage']:
            try:
                scale = images_view.scale(fieldname=field_name,
                                          scale=scale_name)
            except AttributeError:
                continue
            if scale is not None:
                return scale.url

    def month(self, obj=None):
        start_date = self._start_date(obj)
        end_date = self._end_date(obj)
        result = start_date.strftime('%b')
        try:
            end_month = end_date.strftime('%b')
        except AttributeError:
            pass
        else:
            if result != end_month:
                result += '-' + end_month
        return result

    def start(self, obj=None):
        start_date = self._start_date(obj)
        try:
            all_day = obj.whole_day
        except AttributeError:
            all_day = False
        result = start_date.strftime('%a, %b %-d, ')
        if all_day:
            result += 'All day'
        else:
            result += start_date.strftime(TIME_FORMAT)
        return result

    def _start_date(self, obj=None):
        content = obj or self.content
        try:
            return content.start
        except AttributeError:
            try:
                return content.effective_date
            except AttributeError:
                return None
        return None


class ITimedContentTile(model.Schema):

    title = schema.TextLine(
        title=_('Title'),
        required=False
    )

    heading_level = schema.Choice(
        title=_('Heading Level'),
        description="Which heading level should 'title' be displayed as?",
        default='Heading 2',
        values=('Heading 2',
                'Heading 3',
                'Heading 4',
                'Heading 5',
                'Heading 6'),
    )

    summary = schema.Text(
        title=_('Summary'),
        required=False
    )

    date_method = schema.Choice(
        title=_('Date Method'),
        description="'Annual' will adjust the Publication and "
                    "Expiration date years appropriate in reference "
                    "to the current year",
        default='Actual',
        values=('Actual',
                'Annual'),
    )

    publication_date = TileDatetime(
        title=_('Publication Date'),
        description="Display 'Published content' after this date and "
                    "before Expiration Date",
        required=True
    )
    form.widget('publication_date', DatetimeWidget)

    published_content = RichText(
        title=_('Published Content'),
        description="Content displayed after 'Publication Date' and "
                    "before 'Expiration Date'",
        required=True
    )

    expiration_date = TileDatetime(
        title=_('Expiration Date'),
        description="Display 'Expired Content' after this date. If blank, "
                    "nothing is displayed",
        required=True
    )
    form.widget('expiration_date', DatetimeWidget)

    expired_content = RichText(
        title=_('Expired Content'),
        description="Content displayed after 'Expiration Date'",
        required=False
    )

    editor_notes = schema.Text(
        title=_('Editor Notes'),
        description="Displayed only in edit mode for content editors",
        required=False
    )


class TimedContentTile(Tile):
    """Tile for displaying different content when published/expired"""

    template = ViewPageTemplateFile('templates/timed_content.pt')

    def __call__(self):
        self.update()
        return self.template()

    def update(self):
        self.title = self.data.get('title', '')
        self.description = self.data.get('summary', '')
        self.published_content = self.data.get('published_content', '')
        self.expired_content = self.data.get('expired_content', '')
        self.editor_notes = self.data.get('editor_notes', '')
        self.date_method = self.data.get('date_method')
        # if not date_method:
        #     date_method = 'Actual'
        # date_method = date_method.lower()
        # self._now = datetime.now()
        # self._pub_date = None
        # self._exp_date = None
        # pub_date = self.data.get('publication_date')
        # exp_date = self.data.get('expiration_date')
        # if pub_date is None and exp_date is None:
        #     self._pub_date = self._now - timedelta(days=1)
        #     self._exp_date = self._now + timedelta(days=1)
        # elif pub_date is None and exp_date is not None:
        #     import pdb; pdb.set_trace()
        #     self._exp_date = datetime.strptime(exp_date, '%Y-%m-%dT%H:%M:%S')
        #     if self._now <= self._exp_date:
        #         self._pub_date = self._now - timedelta(days=1)
        #     else:
        #         self._pub_date = self._exp_date - timedelta(days=1)
        # elif pub_date is not None and exp_date is None:
        #     import pdb; pdb.set_trace()
        #     self._pub_date = datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%S')
        #     if self._now <= self._pub_date:
        #         self._exp_date = self._pub_date + timedelta(days=1)
        #     else:
        #         self._exp_date = self._now + timedelta(days=1)
        # else:
        #     import pdb; pdb.set_trace()
        #     x = 2
        # print('------------ UPDATE ------------')
        # print('_now: {}'.format(self._now))
        # print('_pub_date: {}'.format(self._pub_date))
        # print('_exp_date: {}'.format(self._exp_date))
        # if date_method == 'annual':
        #     pass

    def _expired_actual(self, pub_date, exp_date):
        now = datetime.now()
        pub_date = datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%S')
        exp_date = datetime.strptime(exp_date, '%Y-%m-%dT%H:%M:%S')
        if (pub_date < now and exp_date < now) or (pub_date > now and exp_date > now):
            return pub_date < exp_date
        else:
            return exp_date < pub_date

    def _expired_annual(self, pub_date, exp_date):
        return False

    @property
    @memoize
    def inEditMode(self):
        # only output the javascript if not rendering for layout editor
        if (self.request.get('_layouteditor') is True or
                ISubRequest.providedBy(self.request)):
            return False
        else:
            return True

    @property
    @memoize
    def isExpired(self):
        # if self._pub_date <= self._now <= self._exp_date:
        #     return False
        # elif self._exp_date <= self._now <= self._pub_date:
        #     return True
        # elif self._pub_date <= self._exp_date:
        #     return True
        # return False
        pub_date = self.data.get('publication_date')
        exp_date = self.data.get('expiration_date')
        date_method = self.data.get('date_method')
        if not date_method:
            date_method = 'Actual'
        date_method = date_method.lower()
        if date_method == 'actual':
            return self._expired_actual(pub_date, exp_date)
        elif date_method == 'annual':
            return self._expired_annual(pub_date, exp_date)
        return False

    @property
    @memoize
    def title_tag(self):
        title = self.data.get('title', '')
        if not title:
            return ''
        level = self.data.get('heading_level')
        if level is None:
            level = 'Heading 2'
        level = level.replace('Heading ', 'h')
        return '<{}>{}</{}>'.format(level, title, level)





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
