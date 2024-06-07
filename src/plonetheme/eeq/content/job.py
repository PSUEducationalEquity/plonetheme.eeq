from plone.dexterity.content import Item
from plone.supermodel import model
from plone.dexterity.interfaces import IContentType
from zope.interface import alsoProvides


class IJob(model.Schema):
    model.load('../models/job.xml')


alsoProvides(IJob, IContentType)


class Job(Item):
    portal_type = 'plonetheme.eeq.job'
