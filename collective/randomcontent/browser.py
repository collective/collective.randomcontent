from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
import random


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

    def __call__(self):
        self._nocache()
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        images = catalog(portal_type=self.portal_type)
        if not images:
            return ""
        rnd = random.randint(0, len(images) - 1)
        self.request.RESPONSE.redirect(images[rnd].getURL())
        return ""
