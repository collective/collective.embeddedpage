# -*- coding: utf-8 -*-
from collective.embeddedpage.interfaces import ICollectiveEmbeddedpageLayer
from collective.embeddedpage.interfaces import IEmbeddedPage
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(ISerializeToJson)
@adapter(IEmbeddedPage, ICollectiveEmbeddedpageLayer)
class CustomSerializeUserToJson(SerializeToJson):

    def __call__(self, version=None, include_items=True):
        serialization = super(CustomSerializeUserToJson, self).__call__(
            version=version, include_items=include_items)
        view = getMultiAdapter((self.context, self.request), name="view")
        serialization.update({
            'html': view.process_page(),
        })
        return serialization
