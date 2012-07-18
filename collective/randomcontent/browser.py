import logging
import random

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

logger = logging.getLogger('collective.randomcontent')


class RandomCatalogImage(BrowserView):

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
        return '/'

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


class RandomImage(RandomCatalogImage):

    def _get_path(self):
        registry = getUtility(IRegistry)
        randomContentFolder = registry.records.get(
            'collective.randomcontent.interfaces.IRandomContentSettings'
            '.randomContentFolder')
        if not randomContentFolder or not randomContentFolder.value:
            return '/'
        UID = randomContentFolder.value
        context = aq_inner(self.context)
        # Note: if we would use the uid_catalog, we do not get a
        # workable path from the brain.
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(UID=UID)
        if not brains:
            logger.warn('No object found for UID %s' % UID)
            return '/'
        return brains[0].getPath()
