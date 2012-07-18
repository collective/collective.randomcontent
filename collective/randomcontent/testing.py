from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.configuration import xmlconfig


class RandomContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.randomcontent
        xmlconfig.file('configure.zcml', collective.randomcontent,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        # Apply our profile.
        applyProfile(portal, 'collective.randomcontent:default')

RANDOM_CONTENT_FIXTURE = RandomContentLayer()
RANDOM_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RANDOM_CONTENT_FIXTURE,), name="RandomContent:Integration")

# tool.gif
IMAGE_DATA = (
    'GIF89a\x10\x00\x10\x00\xf2\x08\x00>\xa8\xd2\x12\x9a\xcb*\xa2\xcf\xac\xd7'
    '\xebP\xaf\xd5a\xb6\xd9\x81\xc3\xe1\x00\x93\xc8!\xff\x0bNETSCAPE2.0\x03'
    '\x01\x00\x00\x00!\xf9\x04\x05\x00\x00\x08\x00,\x00\x00\x00\x00\x10\x00'
    '\x10\x00\x00\x04Z\x10I4\xc8\xb9\x87\x8c\xc9\x01&\xd6\x05pHp\x08\xdb4'
    '\x08G0y\x85d\x18\x9c5\x0e\xa7|\xd1\x13[\x1d)\xc3\x8e\x83\x0bqf2\xde\x87'
    '\xa4;\xd0B\x04&B\xe8D\x84\x0eG\x1e\x12q\xb1\x04\x87\xaa\x0cN\xd0\xe4I|'
    '\x08Otj\xb6\x1eF\x12\x13\x8a\xc8ru>W8\xe9\xf7II"\x00;')

# A few helper functions.


def make_test_image(context):
    new_id = context.generateUniqueId('Image')
    context.invokeFactory('Image', new_id, image=IMAGE_DATA)
    image = context[new_id]
    image.reindexObject()  # Might have already happened, but let's be sure.
    return image


def make_test_doc(context):
    new_id = context.generateUniqueId('Document')
    context.invokeFactory('Document', new_id)
    doc = context[new_id]
    doc.reindexObject()  # Might have already happened, but let's be sure.
    return doc


def register_path(path):
    # Register as random content folder
    registry = getUtility(IRegistry)
    randomContentFolder = registry.records.get(
        'collective.randomcontent.interfaces.IRandomContentSettings'
        '.randomContentFolder')
    randomContentFolder.value = path


def make_test_folder(context, new_id=None, register=False):
    if not new_id:
        new_id = context.generateUniqueId('Folder')
    context.invokeFactory('Folder', new_id)
    folder = context[new_id]
    folder.reindexObject()
    if register:
        # Register as random content folder
        register_path('/'.join(folder.getPhysicalPath()))
    return folder
