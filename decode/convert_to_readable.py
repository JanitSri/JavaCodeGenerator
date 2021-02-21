from urllib.parse import unquote
import zlib
from bs4 import BeautifulSoup as bs
import base64

class DecodeAndDecompress:
  
  @staticmethod
  def convert(drawio_filepath):
    """
    References:
      https://drawio-app.com/extracting-the-xml-from-mxfiles/
      https://github.com/pzl/drawio-read/blob/master/read.py

    Convert the DrawIO file to raw XML

    Paramters:
      drawio_filepath: file path to the .drawio file
    
    Returns:
      decoded_xml: decode and decompressed xml
    """

    try:
      with open(drawio_filepath, "r") as f:
        content = f.readlines()
        content = "".join(content)
    
      drawio_file_raw = bs(content, "lxml")
      diagram_tag = drawio_file_raw.find("diagram")
      diagram_tag_text = base64.b64decode(diagram_tag.text)

      decoded_xml = unquote(zlib.decompress(diagram_tag_text,-15).decode('utf8'))

      return decoded_xml
      
    except Exception as e:
      print(f"DecodeAndDecompress.convert ERROR: {e}")
      return False
    
  @staticmethod
  def write_xml_file(xml_file_name, decoded_xml):
    """
    Write the decoded XML to file 

    Paramters:
      xml_file_name: name to give the xml file 
      decoded_xml: the decoded XML to write to file 
    
    Returns:
      boolean: if successful or not 
    """

    try:
      with open(f"{xml_file_name}.xml", "w") as f:
        f.write(decoded_xml)
      
      return True
    except Exception as e:
      print(f"DecodeAndDecompress.write_xml_file ERROR: {e}")
      return False