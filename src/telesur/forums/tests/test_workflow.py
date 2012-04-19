# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import logout

from Products.CMFCore.exceptions import AccessControl_Unauthorized
from Products.CMFCore.WorkflowCore import WorkflowException

from telesur.forums.testing import INTEGRATION_TESTING


class WorkflowTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _loginAsManager(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def _loginAsForumModerator(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])

    def _transition_poll(self, poll, action):
        self._loginAsManager()
        self.wt.doActionFor(poll, action)

    def setUp(self):
        self.portal = self.layer['portal']
        self.wt = getattr(self.portal, 'portal_workflow')
        self.portal_membership = getattr(self.portal, 'portal_membership')
        self.checkPermission = self.portal_membership.checkPermission
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('telesur.forums.forum', 'test-forum')
        self.folder = self.portal['test-forum']
        self.folder.invokeFactory('telesur.forums.session', 's1')
        self.session = self.folder['s1']

    def test_workflows_installed(self):
        ids = self.wt.getWorkflowIds()
        self.assertTrue('session_workflow' in ids)
        self.assertTrue('question_workflow' in ids)

    def test_default_workflow(self):
        chain = self.wt.getChainForPortalType('telesur.forums.session')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'session_workflow')

        chain = self.wt.getChainForPortalType('telesur.forums.question')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'question_workflow')

    def test_workflow_initial_state(self):
        review_state = self.wt.getInfoFor(self.session, 'review_state')
        self.assertEqual(review_state, 'private')
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])
        self.wt.doActionFor(self.session, 'publish')
        self.session.invokeFactory('telesur.forums.question', 'q1')
        q1 = self.session['q1']
        review_state = self.wt.getInfoFor(q1, 'review_state')
        self.assertEqual(review_state, 'pending_review')

    def test_cannot_publish_unless_forum_moderator(self):

        review_state = self.wt.getInfoFor(self.session, 'review_state')
        self.assertEqual(review_state, 'private')

        setRoles(self.portal, TEST_USER_ID, ['Forum Guest'])

        self.assertRaises(WorkflowException,
                          self.wt.doActionFor,
                          self.session, 'publish')


        setRoles(self.portal, TEST_USER_ID, ['Forum Moderator'])
        self.wt.doActionFor(self.session, 'publish')

        review_state = self.wt.getInfoFor(self.session, 'review_state')
        self.assertEqual(review_state, 'published')

    def test_questions_only_addable_in_published_state(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])

        self.assertRaises(AccessControl_Unauthorized,
                          self.session.invokeFactory,
                          'telesur.forums.question', 'q1')

        self.wt.doActionFor(self.session, 'publish')

        self.session.invokeFactory('telesur.forums.question', 'test-question', question=u'Test question')
        self.assertTrue('test-question' in self.session)

        self.wt.doActionFor(self.session, 'close')

        self.assertRaises(AccessControl_Unauthorized,
                          self.session.invokeFactory,
                          'telesur.forums.question', 'q2')

    def test_anonymous_can_add_questions(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])

        self.wt.doActionFor(self.session, 'publish')

        logout()

        self.session.invokeFactory('telesur.forums.question', 'test-question', question=u'Test question')
        self.assertTrue('test-question' in self.session)

    def test_question_not_publishable_until_answered(self):

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])

        self.wt.doActionFor(self.session, 'publish')

        self.session.invokeFactory('telesur.forums.question', 'test-question', question=u'Test question')

        question = self.session['test-question']

        self.assertRaises(WorkflowException,
                          self.wt.doActionFor,
                          question, 'publish')

        question.answer = u"Test answer"

        self.wt.doActionFor(question, 'publish')

    def test_question_not_visible_by_anonymous_if_it_is_not_published(self):
        checkPermission = self.checkPermission
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])

        self.wt.doActionFor(self.session, 'publish')

        logout()

        self.session.invokeFactory('telesur.forums.question', 'test-question', question=u'Test question')

        question = self.session['test-question']

        # Esto es correcto, podemos agregar como anonimo, pero no podemos verlo.
        self.assertNotEqual(checkPermission('View', question), 1)

        self._loginAsForumModerator()
        question.answer = u"Test answer"

        self.wt.doActionFor(question, 'publish')

        logout()

        self.assertEqual(checkPermission('View', question), 1)

        self._loginAsForumModerator()

        self.wt.doActionFor(question, 'reject')

        logout()

        self.assertNotEqual(checkPermission('View', question), 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
