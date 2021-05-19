from bs4 import BeautifulSoup as bs
from collections import OrderedDict 
import re

class StyleParser:
  """
  Parse the XML into a style tree

  Parameters: 
    di_xml: the decoded and decompressed DrawIO XML
  """

  def __init__(self, di_xml):
    self.di_xml = di_xml
    self.style_tree = None
  
  def convert_to_style_tree(self):
    """
    Convert the XML to a style tree 

    Returns:
      style_tree: dictionary of the extracted elements from the XML
    """

    print("<<< CONVERTING XML TO STYLE TREE >>>")

    try:
      self.style_tree = dict()
      graph_model = bs(self.di_xml, "lxml")
      root = graph_model.find('root')
      root_children = root.children

      grandparent = None
      root_parent = None

      relationship_list = list()

      child = next(root_children, None)
      while child:
        child_attrs = child.attrs

        if "parent" in child_attrs:
          if child_attrs['parent'] == grandparent:  # found the root parent element
            root_parent = child_attrs['id']
            self.style_tree['root'] = self._add_root_parent(child_attrs)
          elif "source" in child_attrs or "target" in child_attrs:  # found a relationship element
            if "source" not in child_attrs:  
              print(f"'source' not present in {child_attrs['id']} relationship")
            elif "target" not in child_attrs:
              print(f"'target' not present in {child_attrs['id']} relationship")              
            else:
              relationship_list.append(child_attrs)
          else:  # found a cell element
            self.style_tree['root']['cells'][child_attrs['id']] = self._add_cells(child_attrs, root_parent)
        else:  # found the grandparent element  
          if grandparent is None:
            grandparent = child_attrs['id']

        child = next(root_children, None)
      
      # need to process the relationships at the end to get the right source and target
      for child_attrs in relationship_list:
        self.style_tree['root']['relationships'][child_attrs['id']] = self._add_relationships(child_attrs, root_parent)

      return self.style_tree
    except Exception as e:
      print(f"StyleParser.convert_to_style_tree ERROR: {e}") 
      return False
  
  def _add_root_parent(self, attrs):
    """
    Format dictionary for the root parent

    Parameters:
      attrs: the root_parent element attributes

    Returns:
      root_parent_dict: dictionary containing id, parent_id, cells, connections 
    """

    return {
      'id': attrs['id'],
      'parent_id': attrs['parent'],
      'cells': OrderedDict(),  # need to keep insertion order to seperate the properties and methods 
      'relationships': dict()
    }
  
  def _add_relationships(self, attrs, root_parent):
    """
    Format dictionary for the relationships

    Parameters:
      attrs: the relationship element attributes
      tree: the style tree, needed to find the parent target
      root_parent: the id of the root parent element 

    Returns:
      root_parent_dict: dictionary containing id, parent_id, cells, connections 
    """

    source = attrs['source']
    parent_source = self.style_tree['root']['cells'][source]['parent_id']
    while parent_source != root_parent:
      source = parent_source
      parent_source = self.style_tree['root']['cells'][source]['parent_id']
    
    target = attrs['target']
    parent_target = self.style_tree['root']['cells'][target]['parent_id']
    while parent_target != root_parent:
      target = parent_target
      parent_target = self.style_tree['root']['cells'][target]['parent_id']

    style = self._get_style(attrs['style'])

    return {
      'id': attrs['id'],
      'parent_id': attrs['parent'],
      'source': source,
      'target': target,
      'style': style
    }
  
  def _add_cells(self, attrs, root_parent):
    """
    Format dictionary for the cells

    Parameters:
      attrs: the cell element attributes
      root_parent: the id of the root parent 

    Returns:
      cell_dict: dictionary containing id, parent_id, style, values
    """

    style = self._get_style(attrs['style'])
    value = attrs['value']
    cell_result = {
      'id': attrs['id'],
      'parent_id': attrs['parent'],
      'style': style
    }

    if "type" not in style.keys() and attrs['parent'] == root_parent: # cell design is html
      style['type'] = "html"
      split_values = re.sub("<hr .*?>", "\n<hr>\n", value).lstrip("\n").split("\n")
      cell_result['values'] = [
        self._get_text_values(bs(val, 'lxml').text) for val in split_values if val != "<hr>"
      ]
      cell_result['style']['type'] = "html"
    else:
      cell_result['values'] = self._get_text_values(value)
 
    return cell_result

  def _get_text_values(self, values):
    """
    Get individual values for the joined values 

    Parameters:
      values: raw values for extraction

    Returns:
      vals: list of the final values 
    """

    temp_val = ""
    vals = []
    for v in values:
      if v in ['+', '-', "#"]: 
        if temp_val:
          vals.append(temp_val.strip().replace(" ", ""))
        temp_val = ""
      
      temp_val += v
    
    vals.append(temp_val.strip().replace(" ", ""))

    return vals

  def _get_style(self, style_attrs):
    """
    Convert the style attribute to a dictionary

    Parameters:
      style_attrs: style attributes of the element  

    Returns:
      style_dict: style attribute as a dictionary 
    """

    style_list = style_attrs.split(";")
    style_dict = dict()

    for s in style_list:
      if "=" in s:
        s_list = s.split("=")
        style_dict[s_list[0]] = s_list[1]
      else:
        if s:
          style_dict['type'] = s

    return style_dict
