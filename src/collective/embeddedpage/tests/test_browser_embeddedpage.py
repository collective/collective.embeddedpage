# -*- coding: utf-8 -*-
from collective.embeddedpage.testing import COLLECTIVE_EMBEDDEDPAGE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from zope.component import getMultiAdapter

import lxml
import unittest


class EmbeddedPageViewIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_EMBEDDEDPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            'EmbeddedPage',
            id='epage',
            title='Embedded Page',
            before=RichTextValue('Before', 'text/html', 'text/html'),
            after=RichTextValue('After', 'text/html', 'text/html'),
        )
        self.portal.epage.url = 'https://plone.org'
        self.epage = self.portal.epage

    def test_view_with_get_multi_adapter(self):
        # Get the view
        view = getMultiAdapter((self.epage, self.request), name="view")
        # Put the view into the acquisition chain
        view = view.__of__(self.epage)
        # Call the view
        self.assertTrue(view())

    def test_view_with_restricted_traverse(self):
        view = self.epage.restrictedTraverse('view')
        self.assertTrue(view())

    def test_view_with_unrestricted_traverse(self):
        view = self.epage.unrestrictedTraverse('view')
        self.assertTrue(view())

    def get_parsed_data(self):
        view = getMultiAdapter((self.epage, self.request), name="view")
        view = view.__of__(self.epage)
        return lxml.html.fromstring(view())

    def test_view_html_structure(self):
        output = self.get_parsed_data()
        before = output.cssselect('.before-embeddedpage')
        embedded = output.cssselect('.embeddedpage')
        after = output.cssselect('.after-embeddedpage')
        self.assertEqual(1, len(embedded))
        self.assertEqual(1, len(embedded))
        self.assertEqual(1, len(embedded))

    def test_view_data_embedded(self):
        output = self.get_parsed_data()
        embedded = output.cssselect('.embeddedpage')[0]
        self.assertEqual('https://plone.org', embedded.attrib['data-embedded'])

    def test_view_data_embedded(self):
        output = self.get_parsed_data()
        embedded = output.cssselect('.embeddedpage')[0]
        self.assertEqual('https://plone.org', embedded.attrib['data-embedded'])
