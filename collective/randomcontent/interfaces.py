from zope.interface import Interface
from zope import schema

from collective.randomcontent import randomContentMessageFactory as _


class IRandomContentSettings(Interface):
    """RandomContent settings
    """

    randomContentFolder = schema.ASCIILine(
        title=_(u"Path to random content folder"),
        description=_(u"Path to the folder that contains the random content. "
                      u"The navigation root would have / as path."),
        required=False,
        )
