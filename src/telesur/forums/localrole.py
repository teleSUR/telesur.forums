# -*- coding: utf-8 -*-

from borg.localrole.interfaces import ILocalRoleProvider

from telesur.forums.content.session import ISession
from telesur.forums.content.question import IQuestion

from zope.interface import Interface

from zope.interface import implements
from zope.component import adapts


class ForumsLocalRoles(object):
    """
    Provide local roles for the forums

    XXX: This was taken literally from
    http://collective-docs.readthedocs.org/en/latest/security/dynamic_roles.html

    see if we can optimize it
    """

    implements(ILocalRoleProvider)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def getForumModeratorRolesOnContext(self, context, principal_id):
        """
        Calculate Forum Moderator roles based on the user object.

        Note: This function is *heavy* since it wakes lots of objects along the acquisition chain.
        """

        session = None

        if ISession.providedBy(context):
            session = context.aq_inner
        else:
            if IQuestion.providedBy(context):
                session = context.aq_inner.aq_parent

        if session:
            pm = self.context.portal_membership
            user = pm.getMemberById(principal_id)

            if user:
                username = user.getUser().getUserName()
                if session.moderator and (username in session.moderator):
                    return ["Forum Moderator"]

        # No match
        return []

    def getRoles(self, principal_id):
        """Returns the roles for the given principal in context.

        This function is additional besides other ILocalRoleProvider plug-ins.

        @param context: Any Plone object
        @param principal_id: User login id
        """
        return self.getForumModeratorRolesOnContext(self.context, principal_id)

    def getAllRoles(self):
        """Returns all the local roles assigned in this context:
        (principal_id, [role1, role2])"""
        return []
