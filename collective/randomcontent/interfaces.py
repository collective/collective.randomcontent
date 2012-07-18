from zope.interface import Interface
from zope import schema

from collective.randomcontent import randomContentMessageFactory as _


class IRandomContentSettings(Interface):
    """RandomContent settings
    """

    randomContentFolder = schema.Choice(
        title=_(u"Random content folder"),
        description=_(u"The folder that contains the random content."),
        required=False,
        source='collective.randomcontent.folders',
        )
