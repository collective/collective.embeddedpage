# -*- coding: utf-8 -*-
from lxml import etree
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import lxml
import requests


class EmbeddedPageView(BrowserView):

    template = ViewPageTemplateFile('embeddedpage.pt')

    def __call__(self):
        request_type = self.request['REQUEST_METHOD']
        method = getattr(requests, request_type.lower(), requests.get)
        response = method(self.context.url, params=self.request.form)
        # Normalize charset to unicode
        content = safe_unicode(response.content)
        # Turn to utf-8
        content = content.encode('utf-8')
        el = lxml.html.fromstring(content)
        if el.find('body'):
            el = el.find('body')
        self.embeddedpage = etree.tostring(el, method='html')
        return self.template()
