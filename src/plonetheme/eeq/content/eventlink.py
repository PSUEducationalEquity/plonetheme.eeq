from plone.dexterity.content import Item
from plone.app.contenttypes.interfaces import IEvent
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope.interface import alsoProvides


class IEventLink(model.Schema):
    model.load('../models/eventlink.xml')


alsoProvides(IEventLink, IContentType)
alsoProvides(IEventLink, IEvent)


class EventLink(Item):
    portal_type = 'plonetheme.eeq.eventlink'
