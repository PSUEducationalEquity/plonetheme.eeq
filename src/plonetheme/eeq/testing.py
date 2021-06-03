# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import plonetheme.eeq


class PlonethemeEeqLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plonetheme.eeq)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetheme.eeq:default')


PLONETHEME_EEQ_FIXTURE = PlonethemeEeqLayer()


PLONETHEME_EEQ_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONETHEME_EEQ_FIXTURE,),
    name='PlonethemeEeqLayer:IntegrationTesting',
)


PLONETHEME_EEQ_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONETHEME_EEQ_FIXTURE,),
    name='PlonethemeEeqLayer:FunctionalTesting',
)


PLONETHEME_EEQ_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONETHEME_EEQ_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PlonethemeEeqLayer:AcceptanceTesting',
)
