import os
import unittest
import template_parser
import codecs
import xml.etree.ElementTree as ET

from requirement_types.root import Root
from requirement_types.supply_file import SupplyFile


class PreFlightTest(unittest.TestCase):

    def SetUp(self):
        pass

    def test_parse_file(self):
        xml_reference = os.path.join(os.path.dirname(__file__), 'test_files/test_parse_file.xml')
        result_html = os.path.join(os.path.dirname(__file__), 'test_files/test_parse_file_result.html')

        html = codecs.open(result_html, 'r')
        result = template_parser.load_xml(xml_reference)
        self.assertEqual(result, html.read())

    def test_parse_file_method(self):
        xml_reference = os.path.join(os.path.dirname(__file__), 'test_files/test_parse_file.xml')
        tree = ET.parse(xml_reference)
        root = tree.getroot()
        node = Root("test_root")
        template_parser.parse_supply_file(root[0], node)
        self.assertIsInstance(node.get_children()[0], SupplyFile)
