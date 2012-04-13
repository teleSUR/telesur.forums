# -*- coding: utf-8 -*-

from five import grok
from zope import schema

from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage

from plone.directives import dexterity, form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from zope.security import checkPermission

from telesur.forums import _


class ISession(form.Schema):
    """
    A session than contains questions
    """

    moderator = schema.Choice(
            title=_(u'Moderator'),
            description=_(u'help_moderator',
                          default=u'Choose a user that will be a moderator '
                                   'for the session.'),
            vocabulary=u'plone.principalsource.Users',
            required=True,
        )

    guest_name = schema.TextLine(
            title=_(u'Guest Name'),
            description=_(u'help_guest_name',
                          default=u'Enter here the guest\'s fullname.'),
            required=True,
        )

    guest_description = RichText(
            title=_(u'Guest Description'),
            description=_(u'help_guest_description',
                          default=u'Enter here the guest\'s description.'),
            required=False,
        )

    guest_photo = NamedBlobImage(
            title=_(u'Guest Photo'),
            description=_(u'help_guest_photo',
                          default=u'Enter here the guest\'s photo.'),
            required=True,
        )

    banner = NamedBlobImage(
            title=_(u'Banner'),
            description=_(u'help_banner',
                          default=u'Enter the banner you want to show on top of the session.'),
            required=False,
        )


class View(dexterity.DisplayForm):
    grok.context(ISession)
    grok.require('zope2.View')

    def render(self):
        pt = ViewPageTemplateFile('session_templates/session_view.pt')

        if not self.can_edit():
            self.request.set('disable_border', 1)

        return pt(self)

    def can_edit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def can_add_question(self):
        return checkPermission('telesur.forums.questionAddable', self.context)

    def _get_catalog_results(self, state):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "telesur.forums.question"
        path='/'.join(self.context.getPhysicalPath())
        sort_on='Date'
        sort_order='reverse'

        results = pc.unrestrictedSearchResults(portal_type=ct,
                                               review_state=state,
                                               sort_on=sort_on,
                                               sort_order=sort_order,
                                               path=path)

        return results

    def get_published_questions(self):
        questions = self._get_catalog_results('published')
        return questions

    def get_pending_questions(self):
        questions = self._get_catalog_results('pending_review')
        return questions

    def get_rejected_questions(self):
        questions = self._get_catalog_results('rejected')
        return questions
