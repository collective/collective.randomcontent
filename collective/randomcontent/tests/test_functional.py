import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.randomcontent.testing import (
    RANDOM_CONTENT_INTEGRATION_TESTING,
    make_test_doc, make_test_image, make_test_folder
    )


class TestRandomContent(unittest.TestCase):

    layer = RANDOM_CONTENT_INTEGRATION_TESTING

    def testRandomSiteNoImage(self):
        portal = self.layer['portal']
        view = portal.restrictedTraverse('randomsiteimage')
        result = view()
        # There are no images, so we only get an empty string.
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 200)
        self.assertEqual(response.headers.get('location'), None)

    def testRandomSiteImage(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        image = make_test_image(portal)
        view = portal.restrictedTraverse('randomsiteimage')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         image.absolute_url())

    def testRandomImageNoFolder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        image = make_test_image(portal)
        view = portal.restrictedTraverse('randomimage')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         image.absolute_url())

    def testRandomImageWithEmptyFolder(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        make_test_image(portal)
        make_test_folder(portal, register=True)
        view = portal.restrictedTraverse('randomimage')
        result = view()
        # There are no images, so we only get an empty string.
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 200)
        self.assertEqual(response.headers.get('location'), None)

    def testRandomImage(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        make_test_image(portal)
        folder = make_test_folder(portal, register=True)
        folder_image = make_test_image(folder)
        view = portal.restrictedTraverse('randomimage')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         folder_image.absolute_url())
        # Let's see if that is not a lucky break.
        locations = set()
        for i in range(10):
            result = view()
            self.assertFalse(result)
            response = self.layer['request'].response
            self.assertEqual(response.status, 302)
            location = response.headers.get('location')
            self.assertTrue(location)
            locations.add(location)
        self.assertEqual(len(locations), 1)

    def testRandomness(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        for i in range(5):
            make_test_image(portal)
        view = portal.restrictedTraverse('randomsiteimage')
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
