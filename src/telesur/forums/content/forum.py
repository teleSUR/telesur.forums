# -*- coding: utf-8 -*-
from five import grok

from plone.directives import dexterity, form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from zope.security import checkPermission

class IForum(form.Schema):
    """
    A forum than contains sessions
    """

class View(dexterity.DisplayForm):
    grok.context(IForum)
    grok.require('zope2.View')

    def render(self):
        pt = ViewPageTemplateFile('forum_templates/forum_view.pt')
        self.published = self.get_sessions("published")
        self.closed = self.get_sessions("closed")
        return pt(self)
   
    def can_edit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)
        
    def get_date(self, session):
        date = ""
        if session.date:
            date = session.date.strftime("%d/%m/%Y")
        return date
   
    def get_sessions_published(self):
        return self.get_sessions(["published", "closed"])
    
    def get_sessions_private(self):
        return self.get_sessions("private")
    
    def is_closed(self, session):
        obj = session
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        chain = portal_workflow.getChainForPortalType(obj.portal_type)
        status = portal_workflow.getStatusOf(chain[0], obj)
        state = status["review_state"]
        return state == "closed"

    def get_sessions(self, state):
        pc = getToolByName(self.context, 'portal_catalog')

        ct = "telesur.forums.session"
        path='/'.join(self.context.getPhysicalPath())
        sort_on='Date'
        sort_order='reverse'

        results = pc(portal_type=ct,
                        review_state=state,
                        sort_on=sort_on,
                        sort_order=sort_order,
                        path=path)

        return results