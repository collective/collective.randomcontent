import random

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import getMultiAdapter


class RandomSiteImage(BrowserView):

    portal_type = 'Image'

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

    def _get_path(self):
        context = aq_inner(self.context)
        pps = getMultiAdapter((context, self.request),
                              name='plone_portal_state')
        return pps.navigation_root_path()

    def _filter(self):
        return dict(portal_type=self.portal_type,
                    path=self._get_path())

    def __call__(self):
        self._nocache()
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        images = catalog(**self._filter())
        if not images:
            return ""
        rnd = random.randint(0, len(images) - 1)
        self.request.RESPONSE.redirect(images[rnd].getURL())
        return ""


class RandomImage(RandomSiteImage):

    def _get_path(self):
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
        portal_path = '/'.join(portal.getPhysicalPath())
        if portal_path == root_path:
            # Already checked
            return root_path
        if not content_path.startswith(portal_path):
            path = '/'.join([portal_path, content_path])
        path = path.replace('//', '/')
        target = portal.unrestrictedTraverse(path, None)
        if target:
            # Acquisition could mean the target has a different
            # physical path.
            return '/'.join(target.getPhysicalPath())
        return root_path
