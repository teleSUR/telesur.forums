# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from telesur.forums.content.forum import IForum
from telesur.forums.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('telesur.forums.forum', 'test-forum')
        self.folder = self.portal['test-forum']

    def test_adding(self):
        self.assertTrue(IForum.providedBy(self.folder))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.forum')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.forum')
        schema = fti.lookupSchema()
        self.assertEquals(IForum, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='telesur.forums.forum')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IForum.providedBy(new_object))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
