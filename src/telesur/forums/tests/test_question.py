# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from telesur.forums.content.question import IQuestion
from telesur.forums.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Forum Moderator'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        # Questions are only addable inside published sessions
        self.folder.invokeFactory('telesur.forums.session', 's1')
        self.session = self.folder['s1']
        workflow_tool = getattr(self.portal, 'portal_workflow')
        workflow_tool.doActionFor(self.session, 'publish')

    def test_addable_inside_session(self):
        self.session.invokeFactory('telesur.forums.question', 'q1')
        q1 = self.session['q1']
        self.failUnless(IQuestion.providedBy(q1))

    def test_not_globally_addable(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.question')
        self.assertFalse(fti.global_allow)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.question')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.question')
        schema = fti.lookupSchema()
        self.assertEquals(IQuestion, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.question')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IQuestion.providedBy(new_object))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
