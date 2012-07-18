from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout

from collective.randomcontent.interfaces import IRandomContentSettings
from collective.randomcontent import randomContentMessageFactory as _


class SettingsEditForm(RegistryEditForm):
    """RandomContent Settings edit form for plone.app.registry.
    """
    schema = IRandomContentSettings
    label = _(u"Random Content Settings")
    # redirect to ourselves after edit
    control_panel_view = "collective-randomcontent-settings"


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
