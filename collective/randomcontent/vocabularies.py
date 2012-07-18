from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements


class PortalTypesVocabulary(object):

    implements(IVocabularyFactory)

    def __init__(self, portal_type):
        self.portal_type = portal_type

    def __call__(self, context):
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog', None)
        if catalog is None:
            return SimpleVocabulary([])

        brains = catalog(portal_type=self.portal_type)
        items = [(brain.UID, brain.Title) for brain in brains]
        # Most schema fields expect unicode values.
        terms = [SimpleTerm(value=unicode(pair[0]), token=unicode(pair[0]),
                             title=pair[1]) for pair in items]
        return SimpleVocabulary(terms)


# Products.CMFCore.interfaces._content.IFolderish
FolderVocabularyFactory = PortalTypesVocabulary('Folder')
