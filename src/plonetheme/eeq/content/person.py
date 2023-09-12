from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFPlone.utils import isExpired
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Item
from plone.locking.interfaces import ILockable
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope import schema
from zope.container.interfaces import INameChooser
from zope.interface import alsoProvides, provider

import re
import transaction


class IPerson(model.Schema):
    model.load('../models/person.xml')


alsoProvides(IPerson, IContentType)


class Person(Item):
    portal_type = 'plonetheme.eeq.person'

    @property
    def description(self):
        try:
            job_titles = self.jobtitles.replace('\r\n', '\n').split('\n')
        except AttributeError:
            job_titles = []
        try:
            return job_titles[0]
        except IndexError:
            return ''

    @property
    def display_name(self):
        name = '{} {}'.format(self.first_name, self.last_name)
        if self.suffix:
            name += ', {}'.format(self.suffix)
        return name

    @property
    def email(self):
        if self.alternate_email:
            return self.alternate_email
        if re.findall(r'\d+', self.id):
            return '{}@psu.edu'.format(self.id)
        else:
            return ''

    @property
    def is_separated(self):
        return isExpired(self)

    @property
    def jobTitles(self):
        try:
            return self.jobtitles.replace('\r\n', '\n').split('\n')
        except AttributeError:
            return self.jobtitles

    @property
    def office_phone(self):
        phone = self.office_phone_raw
        if not phone:
            return self.office_phone_number
        return '{}-{}-{}'.format(phone[:3], phone[3:6], phone[6:])

    @property
    def office_phone_raw(self):
        try:
            phone = (self.office_phone_number.replace('-', '')
                                             .replace('(', '')
                                             .replace(')', '')
                                             .replace(' ', ''))
        except AttributeError:
            return ''
        if len(phone) != 10:
            return ''
        return phone

    @property
    def quotationText(self):
        try:
            return (self.quotation.replace('"', '')
                                  .replace('\u201C', ''))
        except AttributeError:
            return ''

    @property
    def quotationBy(self):
        if not self.quotation_attribution.strip():
            return 'Unknown'
        return self.quotation_attribution

    @property
    def title(self):
        if self.last_name:
            return '{}, {}'.format(self.last_name, self.first_name)
        else:
            return self.first_name


@provider(IFormFieldProvider)
class IUsername(model.Schema):

    # borrowed from plone.app.dexterity.behaviors.id.ShortName
    id = schema.ASCIILine(
        title='Username',
        description='Penn State username (e.g., abc123)',
        required=True,
    )
    directives.order_before(id='*')
    directives.write_permission(id='cmf.AddPortalContent')


class Username(object):

    # borrowed from plone.app.dexterity.behaviors.id.ShortName
    def __init__(self, context):
        self.context = context

    def _get_id(self):
        return self.context.getId()

    def _set_id(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        parent = aq_parent(context)
        if parent is None:
            # Object hasn't been added to graph yet; just set directly
            context.id = value
            return
        new_id = INameChooser(parent).chooseName(value, context)
        if getattr(aq_base(context), 'id', None):
            transaction.savepoint()
            locked = False
            lockable = ILockable(context, None)
            if lockable is not None and lockable.locked():
                locked = True
                lockable.unlock()
            parent.manage_renameObject(context.getId(), new_id)
            if locked:
                lockable.lock()
        else:
            context.id = new_id
    id = property(_get_id, _set_id)
