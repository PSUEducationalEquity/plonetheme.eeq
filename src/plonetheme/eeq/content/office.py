from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope.interface import alsoProvides


class IOffice(model.Schema):
    model.load('../models/office.xml')


alsoProvides(IOffice, IContentType)


class Office(Container):
    portal_type = 'plonetheme.eeq.office'
