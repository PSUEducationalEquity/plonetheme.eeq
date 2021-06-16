# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'plonetheme.eeq:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def rebuild_bundles(context):
    if hasattr(context, 'getSite'):
        if context.readDataFile('doaks-content.txt') is None:
            return
        portal = context.getSite()
    else:
        portal = getToolByName(context, 'portal_url').getPortalObject()
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.reinstallProduct('plone.staticresources')
