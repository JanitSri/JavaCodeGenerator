from bs4 import BeautifulSoup as bs
from collections import OrderedDict 
import json 

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
      while(child):
        child_attrs = child.attrs

        if "parent" in child_attrs:
          if child_attrs['parent'] == grandparent:  # found the root parent element
            root_parent = child_attrs['id']
            self.style_tree["root"] = self._add_root_parent(child_attrs)
          elif "source" in child_attrs and "target" in child_attrs:  # found a relationship element
            relationship_list.append(child_attrs)
          else:  # found a cell element
            self.style_tree["root"]["cells"][child_attrs['id']] = self._add_cells(child_attrs)
        else:  # found the grandparent element  
          if grandparent is None:
            grandparent = child_attrs['id']

        child = next(root_children, None)
      
      # need to process the relationships at the end to get the right target
      for relationship in relationship_list:
        child_attrs = relationship
        self.style_tree["root"]["relationships"][child_attrs['id']] = self._add_relationships(child_attrs, self.style_tree, root_parent)

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
      "id":attrs["id"],
      "parent_id":attrs["parent"],
      "cells": OrderedDict(),  # need to keep insertion order to seperate the properties and methods 
      "relationships": dict()
    }
  
  def _add_relationships(self, attrs, tree, root_parent):
    """
    Format dictionary for the relationships

    Parameters:
      attrs: the relationship element attributes
      tree: the style tree, needed to find the parent target
      root_parent: the id of the root parent element 

    Returns:
      root_parent_dict: dictionary containing id, parent_id, cells, connections 
    """

    source = attrs["source"]
    parent_source = self.style_tree['root']['cells'][source]['parent_id']
    while(parent_source != root_parent):
      source = parent_source
      parent_source = self.style_tree['root']['cells'][source]['parent_id']
    
    target = attrs["target"]
    parent_target = self.style_tree['root']['cells'][target]['parent_id']
    while(parent_target != root_parent):
      target = parent_target
      parent_target = self.style_tree['root']['cells'][target]['parent_id']

    style = self._get_style(attrs['style'])

    return {
      "id":attrs["id"],
      "parent_id":attrs["parent"],
      "source": source,
      "target": target,
      "style": style
    }
  
  def _add_cells(self, attrs):
    """
    Format dictionary for the cells

    Parameters:
      attrs: the cell element attributes

    Returns:
      cell_dict: dictionary containing id, parent_id, style, values
    """

    style = self._get_style(attrs['style'])

    value = attrs['value']
    temp_val = ""
    final_values = []
    for v in value:
      if v in ['+', '-', "#"]:
        if temp_val:
          final_values.append(temp_val.strip())
        temp_val = ""
      
      temp_val += v
    
    final_values.append(temp_val.strip())
    
    return {
      "id":attrs["id"],
      "parent_id":attrs["parent"],
      "style": style,
      "values": final_values
    }

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
          style_dict["type"] = s

    return style_dict