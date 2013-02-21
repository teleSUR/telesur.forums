# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

from plone.app.registry.browser import controlpanel

from telesur.forums import _


class IForumsSettings(Interface):
    """ Interface for the control panel form.
    """

    seconds = schema.Int(
        title=_(u'Number of seconds to wait to update the questions'),
        required=False,
    )


class ForumsSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IForumsSettings
    label = _(u'Forums Settings')
    description = _(u'Here you can modify the settings for telesur.forums.')


class ForumsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ForumsSettingsEditForm
