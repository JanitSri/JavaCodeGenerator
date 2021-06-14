import json
from decode.convert_to_readable import DecodeAndDecompress
from parsers.style_parser import StyleParser
from parsers.syntax_parser import SyntaxParser
from generators.java_generator import JavaCodeGenerator

def json_to_file(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data, indent=4))

decoded_xml = DecodeAndDecompress.convert("examples/simple_class_diagram.drawio")
# decoded_xml = DecodeAndDecompress.convert("diagram_single_class.drawio")

DecodeAndDecompress.write_xml_file("examples/simple_class_diagram", decoded_xml)

parser_style = StyleParser(decoded_xml)
style_tree = parser_style.convert_to_style_tree()
# print(json.dumps(style_tree, indent=4))
json_to_file("examples/simple_class_style_tree.json", style_tree)

parser_syntax = SyntaxParser(style_tree)
syntax_tree = parser_syntax.convert_to_sytax_tree()
#  print(json.dumps(syntax_tree, indent=4))
json_to_file("examples/simple_class_syntax_tree.json", syntax_tree)

java_code_gen = JavaCodeGenerator(syntax_tree, "examples/example_code")
java_code_gen.generate_code()
