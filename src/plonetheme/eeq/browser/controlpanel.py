from plone.app.registry.browser.controlpanel import RegistryEditForm
from plonetheme.eeq.interfaces import ISettings

class SettingsControlPanelView(RegistryEditForm):
    schema = ISettings
