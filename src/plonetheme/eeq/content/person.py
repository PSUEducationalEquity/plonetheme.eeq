from Products.CMFPlone.utils import isExpired
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope.interface import alsoProvides


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
        return '{}@psu.edu'.format(self.id)

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
        phone = (self.office_phone_number.replace('-', '')
                                         .replace('(', '')
                                         .replace(')', '')
                                         .replace(' ', ''))
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
        return '{}, {}'.format(self.last_name, self.first_name)
