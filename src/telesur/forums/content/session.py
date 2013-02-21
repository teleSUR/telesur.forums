# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    # Python 2.54 / Plone 3.3 use simplejson
    # version > 2.3 < 3.0
    import simplejson as json

from five import grok
from zope import schema
from zope.component import getUtility, getMultiAdapter
from zope.i18n import translate

from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.registry.interfaces import IRegistry

from plone.directives import dexterity, form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from zope.security import checkPermission

from telesur.forums.controlpanel import IForumsSettings
from telesur.forums import _

grok.templatedir("session_templates")

MONTHS_DICT = {
    '01': _(u'January'),
    '02': _(u'February'),
    '03': _(u'March'),
    '04': _(u'April'),
    '05': _(u'May'),
    '06': _(u'June'),
    '07': _(u'July'),
    '08': _(u'August'),
    '09': _(u'September'),
    '10': _(u'October'),
    '11': _(u'November'),
    '12':_(u'December'),
}

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

    guest = schema.Choice(
            title=_(u'Guest'),
            description=_(u'help_guest',
                          default=u'Choose the guest for the session.'),
            vocabulary=u'plone.principalsource.Users',
            required=False,
        )

    guest_name = schema.TextLine(
            title=_(u'Guest Name'),
            description=_(u'help_guest_name',
                          default=u'Enter here the guest\'s fullname.'),
            required=True,
        )

    guest_photo = NamedBlobImage(
            title=_(u'Guest Photo'),
            description=_(u'help_guest_photo',
                          default=u'Enter here the guest\'s photo.'),
            required=True,
        )

    guest_description = RichText(
            title=_(u'Guest Description'),
            description=_(u'help_guest_description',
                          default=u'Enter here the guest\'s description.'),
            required=False,
        )

    date = schema.Date(title=_(u'Date'), required=True)

    banner = NamedBlobImage(
            title=_(u'Banner'),
            description=_(u'help_banner',
                          default=u'Enter the banner you want to show on top of the session.'),
            required=False,
        )


@form.default_value(field=IExcludeFromNavigation['exclude_from_nav'])
def excludeFromNavDefaultValue(data):
    return data.request.URL.endswith('++add++telesur.forums.session')


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

    def can_answer(self):
        return checkPermission('telesur.forums.questionCanAnswer', self.context)

    def can_add_question(self):
        return checkPermission('telesur.forums.questionAddable', self.context)

    def is_closed(self):
        obj = self.context
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        chain = portal_workflow.getChainForPortalType(obj.portal_type)
        status = portal_workflow.getStatusOf(chain[0], obj)
        state = status["review_state"]
        return state == "closed"

    def can_edit_question_fields(self, question):
        return checkPermission('telesur.forums.questionCanEdit', question)

    def can_answer_question(self, question):
        return checkPermission('telesur.forums.questionCanAnswer', question)

    def can_change_question_wf(self, question):
        return checkPermission('cmf.ReviewPortalContent', question)

    def _get_catalog_results(self, state, ordering='created'):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "telesur.forums.question"
        path = '/'.join(self.context.getPhysicalPath())
        sort_on = ordering
        sort_order = 'reverse'

        results = pc.unrestrictedSearchResults(portal_type=ct,
                                               review_state=state,
                                               sort_on=sort_on,
                                               sort_order=sort_order,
                                               path=path)

        return results

    def get_published_questions(self):
        questions = self._get_catalog_results('published', 'effective')
        return questions

    def get_pending_questions(self):
        questions = self._get_catalog_results('pending_review')
        return questions

    def get_rejected_questions(self):
        questions = self._get_catalog_results('rejected')
        return questions

    def no_questions(self):
        return len(self.get_published_questions()) == 0

    def js_update(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IForumsSettings)
        seconds = 10
        if settings.seconds:
            seconds = settings.seconds

        portal_state = getMultiAdapter(
            (self.context, self.request),
            name="plone_portal_state"
        )

        js = """
            $(document).ready(function() {
                setInterval(intervalSetAnon, %s000);
            });
        """ % seconds

        if not portal_state.anonymous():
            js = """
                $(document).ready(function() {
                    setInterval(intervalSetAnon, %s000);
                    setInterval(intervalSetMember, %s000);
                });
            """ % (seconds, seconds)
        return js

    def format_date(self):
        date = self.context.date
        sep = _(u"of")
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%Y")
        return "%s %s %s %s %s" % (day,
            translate(sep, context=self.request),
            translate(MONTHS_DICT[month], context=self.request),
            translate(sep, context=self.request), year)


class SessionAjax(View):
    grok.context(ISession)
    grok.require('zope2.View')
    grok.name("session-view-published")

    def render(self):
        pt = ViewPageTemplateFile('session_templates/session_view_pag.pt')
        return pt(self)


class SessionAjaxPending(View):
    grok.context(ISession)
    grok.require('zope2.View')
    grok.name("session-view-pending")

    def render(self):
        pt = ViewPageTemplateFile('session_templates/session_pending.pt')
        return pt(self)


class SessionAjaxRejected(View):
    grok.context(ISession)
    grok.require('zope2.View')
    grok.name("session-view-rejected")

    def render(self):
        pt = ViewPageTemplateFile('session_templates/session_rejected.pt')
        return pt(self)


class SessionAjaxPendingNumber(View):
    grok.context(ISession)
    grok.require('zope2.View')
    grok.name("session-pending-number")

    def render(self):
        result = json.dumps({'pending': len(self.get_pending_questions())})
        self.request.response.setHeader("Content-type", "application/json")
        return result
