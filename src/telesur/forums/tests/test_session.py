# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from telesur.forums.content.session import ISession
from telesur.forums.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('telesur.forums.session', 's1')
        s1 = self.folder['s1']
        self.assertTrue(ISession.providedBy(s1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.session')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.session')
        schema = fti.lookupSchema()
        self.assertEquals(ISession, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.session')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISession.providedBy(new_object))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
