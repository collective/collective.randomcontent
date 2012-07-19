import random

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import getMultiAdapter


class BaseRandomView(BrowserView):

    portal_type = None

    def _nocache(self):
        """Don't you dare cache this ever.

        It should be a redirect so it probably does not get cached
        anyway, but let's be sure.  Also, if no images are found, no
        redirect takes place.
        """
        self.request.response.setHeader(
            'Expires', 'Mon, 26 Jul 1997 05:00:00 GMT')
        self.request.response.setHeader(
            'Cache-Control', 'no-store, no-cache, must-revalidate')
        self.request.response.setHeader(
            'Pragma', 'no-cache')

    def _get_nav_root_path(self):
        """Get the navigation root path.
        """
        context = aq_inner(self.context)
        pps = getMultiAdapter((context, self.request),
                              name='plone_portal_state')
        return pps.navigation_root_path()

    def _get_folder_path(self):
        """Get the path of the folder selected for random content.
        """
        context = aq_inner(self.context)
        pps = getMultiAdapter((context, self.request),
                              name='plone_portal_state')
        root_path = pps.navigation_root_path()
        registry = getUtility(IRegistry)
        randomContentFolder = registry.records.get(
            'collective.randomcontent.interfaces.IRandomContentSettings'
            '.randomContentFolder')
        if not randomContentFolder or not randomContentFolder.value:
            return root_path
        content_path = randomContentFolder.value
        portal = pps.portal()
        if content_path.startswith(root_path):
            path = content_path
        else:
            path = '/'.join([root_path, content_path])
        path = path.replace('//', '/')
        target = portal.unrestrictedTraverse(path, None)
        if target:
            # Acquisition could mean the target has a different
            # physical path.
            return '/'.join(target.getPhysicalPath())
        return root_path

    def _get_path(self):
        """Get the path in which we will look for random content.

        By default we use the navigation root path.
        """
        return self._get_nav_root_path()

    def _update_filter(self, myfilter):
        """Update the filter.

        By default we do nothing.  Override this if you need special
        handling.  The filter is passed to the portal_catalog.
        """
        pass

    def _filter(self):
        myfilter = {}
        path = self._get_path()
        if path:
            myfilter['path'] = path
        if self.portal_type:
            myfilter['portal_type'] = self.portal_type
        self._update_filter(myfilter)
        return myfilter

    def __call__(self):
        self._nocache()
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(**self._filter())
        if not brains:
            return ""
        rnd = random.randint(0, len(brains) - 1)
        self.request.RESPONSE.redirect(brains[rnd].getURL())
        return ""


class RandomSiteContent(BaseRandomView):
    pass


class RandomContent(BaseRandomView):

    def _get_path(self):
        """Get the path in which we will look for random content.

        We want to look in the selected folder.
        """
        return self._get_folder_path()


class RandomSiteImage(BaseRandomView):

    portal_type = 'Image'


class RandomImage(BaseRandomView):

    portal_type = 'Image'

    def _get_path(self):
        """Get the path in which we will look for random content.

        We want to look in the selected folder.
        """
        return self._get_folder_path()
