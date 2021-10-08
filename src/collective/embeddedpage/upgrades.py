from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility


def migrate_behaviors(context):
    # Migrate FTI
    fti = queryUtility(IDexterityFTI, name="EmbeddedPage")
    behavior_list = [a for a in fti.behaviors]
    behavior_list.clear()
    fti.behaviors = behavior_list
    context.runImportStepFromProfile("collective.embeddedpage:default", "typeinfo")
