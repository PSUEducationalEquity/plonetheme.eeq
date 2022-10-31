from plone.dexterity.content import Item
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope.interface import alsoProvides


class IPerson(model.Schema):
    model.load('../models/person.xml')


alsoProvides(IPerson, IContentType)


class Person(Item):
    portal_type = 'plonetheme.eeq.person'
