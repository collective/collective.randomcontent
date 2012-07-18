import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.randomcontent.testing import (
    RANDOM_CONTENT_INTEGRATION_TESTING,
    make_test_doc, make_test_image,
    )


class TestRandomContent(unittest.TestCase):

    layer = RANDOM_CONTENT_INTEGRATION_TESTING

    def testRandomCatalogImage(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        make_test_image(portal)
        view = portal.restrictedTraverse('randomcatalogimage')
        import pdb; pdb.set_trace()
        view()
