import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.randomcontent.testing import (
    RANDOM_CONTENT_INTEGRATION_TESTING,
    make_test_doc, make_test_image, make_test_folder, register_path,
    )


class TestRandomContent(unittest.TestCase):

    layer = RANDOM_CONTENT_INTEGRATION_TESTING

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

    def testCaching(self):
        # We want the content to be random, so we make sure this is
        # never cached.
        portal = self.layer['portal']
        view = portal.restrictedTraverse('randomcontent')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        headers = response.headers
        self.assertEqual(headers.get('expires'),
                         'Mon, 26 Jul 1997 05:00:00 GMT')
        self.assertEqual(headers.get('pragma'), 'no-cache')
        self.assertEqual(headers.get('cache-control'),
                         'no-store, no-cache, must-revalidate')

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

    def testRandomSiteImageNoDoc(self):
        # When searching for images, we should never find documents.
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        image = make_test_image(portal)
        make_test_doc(portal)
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
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations.pop(),
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

    def testRandomImageNoDoc(self):
        # When searching for images, we should never find documents.
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        make_test_image(portal)
        make_test_doc(portal)
        folder = make_test_folder(portal, register=True)
        folder_image = make_test_image(folder)
        make_test_doc(folder)
        view = portal.restrictedTraverse('randomimage')
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
        self.assertEqual(locations.pop(),
                         folder_image.absolute_url())

    def testRandomSiteContent(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        doc = make_test_doc(portal)
        view = portal.restrictedTraverse('randomsitecontent')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         doc.absolute_url())

    def testRandomContent(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        make_test_doc(portal)
        folder = make_test_folder(portal, register=True)
        # Note: the folder itself is an excellent random content item,
        # so we do not need to add another document.
        #folder_doc = make_test_doc(folder)
        view = portal.restrictedTraverse('randomcontent')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         folder.absolute_url())
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

    def testRandomSiteImageOtherFolder(self):
        # Check that we can use the views (or one of them anyway) on a
        # regular folder.
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        image = make_test_image(portal)
        folder = make_test_folder(portal)
        view = folder.restrictedTraverse('randomsiteimage')
        result = view()
        self.assertFalse(result)
        response = self.layer['request'].response
        self.assertEqual(response.status, 302)
        self.assertEqual(response.headers.get('location'),
                         image.absolute_url())

    def testRandomSiteImageNavigationRoot(self):
        # Searching for an image in the entire site still takes the
        # navigation root into account.
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        make_test_image(portal)
        folder = make_test_folder(portal)
        from plone.app.layout.navigation.interfaces import INavigationRoot
        from zope.interface import alsoProvides
        alsoProvides(folder, INavigationRoot)
        folder_image = make_test_image(folder)
        view = folder.restrictedTraverse('randomsiteimage')
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
        self.assertEqual(locations.pop(),
                         folder_image.absolute_url())

    def test_path(self):
        # Test some corner cases.
        def get_path(obj):
            return '/'.join(obj.getPhysicalPath())

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        nav_root = make_test_folder(portal)
        from plone.app.layout.navigation.interfaces import INavigationRoot
        from zope.interface import alsoProvides
        alsoProvides(nav_root, INavigationRoot)

        portal_view = portal.restrictedTraverse('randomcontent')
        nav_root_view = nav_root.restrictedTraverse('randomcontent')
        self.assertEqual(portal_view._get_nav_root_path(),
                         get_path(portal))
        self.assertEqual(nav_root_view._get_nav_root_path(),
                         get_path(nav_root))
        self.assertEqual(portal_view._get_folder_path(),
                         get_path(portal))
        self.assertEqual(nav_root_view._get_folder_path(),
                         get_path(nav_root))

        top_folder = make_test_folder(portal, new_id='top', register=True)
        self.assertEqual(portal_view._get_folder_path(),
                         get_path(top_folder))
        self.assertEqual(nav_root_view._get_folder_path(),
                         get_path(top_folder))
        # The path does not need to be the full path from the zope
        # root.
        register_path('top')
        self.assertEqual(portal_view._get_folder_path(),
                         get_path(top_folder))
        self.assertEqual(nav_root_view._get_folder_path(),
                         get_path(top_folder))

        # Make two folders with the same id
        folder_in_portal = make_test_folder(portal, 'target')
        folder_in_nav_root = make_test_folder(nav_root, 'target')
        register_path('target')
        self.assertEqual(portal_view._get_folder_path(),
                         get_path(folder_in_portal))
        self.assertEqual(nav_root_view._get_folder_path(),
                         get_path(folder_in_nav_root))

        # Try with the top level folder again, calling the view on a
        # folder at a deeper level.
        register_path('top')
        view = folder_in_nav_root.restrictedTraverse('randomcontent')
        self.assertEqual(view._get_folder_path(),
                         get_path(top_folder))

        # If the path cannot be traversed, so be it.
        register_path('non-existing')
        self.assertEqual(portal_view._get_folder_path(),
                         get_path(portal))
        self.assertEqual(nav_root_view._get_folder_path(),
                         get_path(nav_root))
