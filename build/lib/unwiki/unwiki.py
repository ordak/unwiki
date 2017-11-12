import pdb
from copy import copy, deepcopy
import re

from lxml import etree

class LogObj:
    def __init__(self, debug=False):
        self.debug = debug

    def _debug(self, *a, **kw):
        if not self.debug:
            return
        print(*a, **kw)

class UnWiki(LogObj):

    def __init__(self, payload, *a, **kw):
        super().__init__(*a, **kw)
        self.encoded = payload
        self.decoded = None

    def _xml_to_str(self, elem):
        self._debug('root 0: {}'.format(etree.tostring(elem)))
        out = elem.text
        for child in elem:
            if child.tag == 'freelink':
                link_payload = self._xml_to_str(child)
                link_segments = link_payload.split('|')
                out += link_segments[-1]
            if child.tail:
                out += child.tail
        self._debug ('   => {}'.format(out))
        return out

    def _decode(self):
        self._debug('\n\nDecoding: {}'.format(self.encoded))
        wip = copy(self.encoded)
        wip = re.sub(r"\[\[", "<freelink>", wip)
        wip = re.sub(r"\]\]", "</freelink>", wip)
        wip = re.sub(r"\{\{", "<template>", wip)
        wip = re.sub(r"\}\}", "</template>", wip)
        self._debug('wip: {}'.format(wip))

        root = etree.fromstring('<text> ' + wip + ' </text>')
        child_tags = [child.tag for child in root]

        root = etree.fromstring('<text> ' + wip + ' </text>')
        self.decoded = self._xml_to_str(root)

    def _old_decode(self):
        #pdb.set_trace()
        for child in root.xpath('//freelink'):
            self._debug('freelink: {} {}'.format(child.text, child.tail))
            if child.tail:
                child.tail = child.text + child.tail
            else:
                child.tail = child.text
        for child in list(root):
            if child.tag == 'template':
                pass
        etree.strip_elements(root, 'freelink', with_tail=False)
        etree.strip_elements(root, 'template', with_tail=False)
        etree.strip_elements(root, 'nowiki', with_tail=False)
        self._debug('root 1: {}'.format(etree.tostring(root)))
        self.decoded = root.text.strip()

    def __str__(self):
        if self.decoded is None:
            self._decode()
        return self.decoded
