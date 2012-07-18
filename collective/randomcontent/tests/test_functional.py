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

    def testRandomCatalogNoImage(self):
        portal = self.layer['portal']
        view = portal.restrictedTraverse('randomcatalogimage')
        result = view()
        # There are no images, so we only get an empty string.
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 200)
        self.assertEqual(response.headers.get('location'), None)

    def testRandomCatalogImage(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        image = make_test_image(portal)
        view = portal.restrictedTraverse('randomcatalogimage')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         image.absolute_url())

    def testRandomness(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        for i in range(5):
            make_test_image(portal)
        view = portal.restrictedTraverse('randomcatalogimage')
        locations = set()
        for i in range(10):
            result = view()
            self.assertFalse(result)
            response = self.layer['request'].response
            self.assertEqual(response.status, 302)
            location = response.headers.get('location')
            self.assertTrue(location)
            locations.add(location)
        # Assure that not the same image is returned each time.  Note:
        # this is expected to fail once every 10 million times.
        self.assertTrue(len(locations) > 1)
