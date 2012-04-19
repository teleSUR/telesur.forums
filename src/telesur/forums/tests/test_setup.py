# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from telesur.forums.config import PROJECTNAME
from telesur.forums.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):
    """Ensure the NITF package is properly installed.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_permissions_roles(self):
        permission = 'telesur.forums: Can add a Question'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertEqual(roles, ['Anonymous'])

        permission = 'telesur.forums: Can answer a Question'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertEqual(roles, ['Forum Guest', 'Forum Moderator'])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
