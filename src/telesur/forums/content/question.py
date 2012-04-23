# -*- coding: utf-8 -*-

import transaction

from Acquisition import aq_base

from five import grok
from zope import schema

from zope.component import getUtility

from zope.event import notify

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from zope.lifecycleevent import ObjectMovedEvent
from OFS.event import ObjectWillBeMovedEvent

from plone.directives import form, dexterity
from plone.i18n.normalizer import idnormalizer

from z3c.form.interfaces import IEditForm

from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.interfaces import IVocabularyFactory

from zope.container.contained import notifyContainerModified

from plone.dexterity.content import Item

from telesur.forums import _

from plone.formwidget.captcha.widget import CaptchaFieldWidget

class IQuestion(form.Schema):
    """
    A question that any site visitor can add.
    """

    dexterity.write_permission(name='telesur.forums.questionCanEdit')
    name = schema.TextLine(
            title=_(u'Name'),
            description=_(u'help_name',
                          default=u'Enter here your full name.'),
            required=True,
        )

    dexterity.write_permission(country='telesur.forums.questionCanEdit')
    country = schema.Choice(
            title=_(u'Country'),
            description=_(u'help_country',
                          default=u'Choose your country.'),
            vocabulary=u"telesur.forums.countries",
            required=True,
        )

    dexterity.write_permission(question='telesur.forums.questionCanEdit')
    question = schema.Text(
            title=_(u'Question'),
            description=_(u'help_question',
                          default=u'Enter your question here.'),
            required=True,
        )
    form.omitted(IEditForm, 'captcha')
    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(
            required=True,
        )
    
    form.omitted('answer')
    form.no_omit(IEditForm, 'answer')
    answer = schema.Text(
            title=_(u'Answer'),
            description=_(u'help_answer',
                          default=u'Enter the answer here.'),
            required=False,
        )


class Question(Item):
    """

    """
    implements(IQuestion)

    def get_country_name(self):
        vocab = getUtility(IVocabularyFactory, name="telesur.forums.countries")
        countries = vocab(self)
        country = countries.getTermByToken(self.country).title

        return country.lower().capitalize()


class canPublishQuestion(grok.View):
    grok.context(IQuestion)
    grok.name("can-publish-question")
    grok.require("cmf.ReviewPortalContent")

    def __call__(self):

        if self.context.answer:
            return True

        return False

    def render(self):
        return "can-publish-question"


@grok.subscribe(IQuestion, IObjectCreatedEvent)
def rename_after_add(obj, event):
    """
    Se asigna el ID a la pregunta, basado en la pregunta propiamente
    """

    id = idnormalizer.normalize(obj.question)
    obj.id = id


@grok.subscribe(IQuestion, IObjectAddedEvent)
@grok.subscribe(IQuestion, IActionSucceededEvent)
def redirect_after_event(obj, event):
    """
    se redirige a la sessión en lugar de permanecer en la pregunta recien
    cargada.
    También se redirige a la sesión, luego de cambiar el estado de workflow
    """

    parent = obj.aq_inner.aq_parent
    obj.REQUEST.RESPONSE.redirect(parent.absolute_url())


@grok.subscribe(IQuestion, IObjectModifiedEvent)
def publish_after_respond(obj, event):
    """
    Se publica la pregunta luego de ser respondida
    """

    workflowTool = getToolByName(obj, "portal_workflow")
    chain = workflowTool.getChainForPortalType(obj.portal_type)
    status = workflowTool.getStatusOf(chain[0], obj)
    review_state = status['review_state']

    if 'answer' in event.descriptions[0].attributes:
        if 'published' not in review_state:
            workflowTool.doActionFor(obj, "publish")
