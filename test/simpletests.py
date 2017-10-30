from unwiki.unwiki import UnWiki

import unittest

class LinkTests(unittest.TestCase):

    def check(self, instr, outstr, debug=False):
        dut = UnWiki(instr, debug=debug)
        self.assertEqual(str(dut).strip(), outstr.strip())

    def test_linkstream(self):
        self.check('good [[hi]]phop', 'good hiphop')

    def test_basic_template(self):
        self.check('{{NewLine}}', '')

    def test_reftag(self):
        self.check('steven <ref>kiddo</ref>F is silly', 'steven F is silly')

    def test_single_link(self):
        self.check('[[hi]]', 'hi')

    def test_nested_link(self):
        self.check('[[hi|wacky [[dude]]s | wa[[rpag]]e ]]', 'warpage')

    def test_ocmplex_link(self):
        self.check('[[hi|wacky dude|warped]]', 'warped')

    def test_coloned_linkstream(self):
        self.check('[[hi]]:phop', 'hi:phop')

    def test_severed_linkstream(self):
        self.check('[[hi]]<nowiki />phop', 'hiphop')
