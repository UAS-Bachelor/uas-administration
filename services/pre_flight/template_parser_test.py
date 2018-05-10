import codecs
import os
import unittest
import xml.etree.ElementTree as ET

import template_parser
from exceptions.requirement_choice_exception import WrongChoiceChildException
from exceptions.requirement_exception import RequirementNotRecognized
from exceptions.tag_name_exception import EmptyNameException, NoNameException
from requirement_types.checkbox import Checkbox
from requirement_types.choice import Choice
from requirement_types.multiline_text import MultilineText
from requirement_types.root import Root
from requirement_types.supply_file import SupplyFile
from requirement_types.text import Text


class TemplateParserTest(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.no_name_xml_reference = os.path.join(os.path.dirname(__file__),
                                                 'test_template_files/test_parse_no_name.xml')
        cls.empty_name_xml_reference = os.path.join(os.path.dirname(__file__),
                                                    'test_template_files/test_parse_empty_name.xml')
        cls.unknown_requirement_xml_reference = os.path.join(os.path.dirname(__file__),
                                                             'test_template_files/test_unknown_requirement.xml')
        cls.file_xml_reference = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_file.xml')
        cls.text_xml_reference = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_text.xml')
        cls.multiline_text_xml_reference = os.path.join(os.path.dirname(__file__),
                                                        'test_template_files/test_parse_multiline_text.xml')
        cls.choice_xml_reference = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_choice.xml')
        cls.choice_wrong_child_xml_reference = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_choice_wrong_child.xml')
        cls.checkbox_xml_reference = os.path.join(os.path.dirname(__file__),
                                                  'test_template_files/test_parse_checkbox.xml')

    def setUp(self):
        self.node = Root("test_root")

    def test_unknown_requirement(self):
        with self.assertRaises(RequirementNotRecognized):
            template_parser.load_xml(self.unknown_requirement_xml_reference)

    def test_no_name_on_requirement(self):
        tree = ET.parse(self.no_name_xml_reference)
        root = tree.getroot()
        with self.assertRaises(NoNameException):
            template_parser.parse_text(root[0], self.node)

    def test_empty_name_on_requirement(self):
        tree = ET.parse(self.empty_name_xml_reference)
        root = tree.getroot()
        with self.assertRaises(EmptyNameException):
            template_parser.parse_text(root[0], self.node)

    def test_parse_file_method(self):
        tree = ET.parse(self.file_xml_reference)
        root = tree.getroot()
        template_parser.parse_supply_file(root[0], self.node)
        self.assertIsInstance(self.node.get_children()[0], SupplyFile)

    def test_parse_file(self):
        result_html = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_file_result.html')

        html = codecs.open(result_html, 'r')
        result = template_parser.load_xml(self.file_xml_reference)
        self.assertEqual(result, html.read())

    def test_parse_text_method(self):
        tree = ET.parse(self.text_xml_reference)
        root = tree.getroot()
        template_parser.parse_text(root[0], self.node)
        self.assertIsInstance(self.node.get_children()[0], Text)

    def test_parse_text(self):
        result_html = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_text_result.html')

        html = codecs.open(result_html, 'r')
        result = template_parser.load_xml(self.text_xml_reference)
        self.assertEqual(result, html.read())

    def test_parse_multiline_text_method(self):
        tree = ET.parse(self.multiline_text_xml_reference)
        root = tree.getroot()
        template_parser.parse_multiline_text(root[0], self.node)
        self.assertIsInstance(self.node.get_children()[0], MultilineText)

    def test_parse_multiline_text(self):
        result_html = os.path.join(os.path.dirname(__file__),
                                   'test_template_files/test_parse_multiline_text_result.html')

        html = codecs.open(result_html, 'r')
        result = template_parser.load_xml(self.multiline_text_xml_reference)
        self.assertEqual(result, html.read())

    def test_parse_choice_method(self):
        tree = ET.parse(self.choice_xml_reference)
        root = tree.getroot()
        template_parser.parse_choice(root[0], self.node)
        self.assertIsInstance(self.node.get_children()[0], Choice)

    def test_parse_choice(self):
        result_html = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_choice_result.html')

        html = codecs.open(result_html, 'r')
        result = template_parser.load_xml(self.choice_xml_reference)
        self.assertEqual(result, html.read())

    def test_parse_choice_wrong_child(self):
        tree = ET.parse(self.choice_wrong_child_xml_reference)
        root = tree.getroot()
        with self.assertRaises(WrongChoiceChildException):
            template_parser.parse_choice(root[0], self.node)

    def test_parse_checkbox_method(self):
        tree = ET.parse(self.checkbox_xml_reference)
        root = tree.getroot()
        template_parser.parse_checkbox(root[0], self.node)
        self.assertIsInstance(self.node.get_children()[0], Checkbox)

    def test_parse_checkbox(self):
        result_html = os.path.join(os.path.dirname(__file__), 'test_template_files/test_parse_checkbox_result.html')

        html = codecs.open(result_html, 'r')
        result = template_parser.load_xml(self.checkbox_xml_reference)
        self.assertEqual(result, html.read())
