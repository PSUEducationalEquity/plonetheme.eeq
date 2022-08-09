from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope.interface import alsoProvides


class IArea(model.Schema):
    model.load('../models/area.xml')


alsoProvides(IArea, IContentType)


class Area(Container):
    portal_type = 'plonetheme.eeq.area'
