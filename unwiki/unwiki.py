import pdb
from io import StringIO
from copy import copy, deepcopy
import re
import traceback
import sys
from tidylib import tidy_document

from lxml import etree

class LogObj:
    def __init__(self, debug=False):
        self.debug = debug

    def _error(self, *a, **kw):
        print(*a, **kw)

    def _debug(self, *a, **kw):
        if not self.debug:
            return
        print(*a, **kw)
        if False:
            sys.stderr.buffer.write(*a, **kw)
            sys.stderr.buffer.write('\n')
            sys.stderr.flush()

class UnWiki(LogObj):
    XHTML_LEADER = """<?xml version="1.0"?>
                    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
                    >"""

    XHTML_LEADER = """<?xml version="1.1"?>
                      <!DOCTYPE naughtyxml [
                        <!ENTITY nbsp "&#0160;">
                      ]>
                    """

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
        wip = re.sub(r"\]\]", "</freelink>", wip) # (\s?)
        wip = re.sub(r"\{\{", "<template>", wip)
        wip = re.sub(r"\}\}", "</template>", wip)
        wip = re.sub(r"<\s*br\s*>", "<br/>", wip)
        wip = re.sub(r"'{2,3}", "", wip)
        #self._debug('wip: {}'.format(wip.encode('utf-8')))

        # root = etree.fromstring('<text> ' + wip + ' </text>')
        # child_tags = [child.tag for child in root]

        root = None
        wip_doc = self.XHTML_LEADER + '<text xml:space="preserve"> ' + wip + ' </text>'
        with open('wip', 'w', encoding='utf-8') as f:
            f.write(wip_doc)
        wip_doc, errs = tidy_document(
            wip_doc,
            options={ 'input-xml': 1
                    , 'output-xml' : 1
                    , 'quote-nbsp' : 1
                    }
        )
        with open('wip_corr', 'w', encoding='utf-8') as f:
            f.write(wip_doc)
    
        try:
            parser = etree.XMLParser(resolve_entities=False)
            root = etree.fromstring(wip_doc, parser=parser)
        except Exception as e:
            self._error(traceback.format_exc())
            wip_l = wip.split('\n')
            pdb.set_trace()
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
