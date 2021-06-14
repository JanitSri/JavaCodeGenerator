class SyntaxParser:
  """
  Parse the style tree into the syntax tree

  Parameters: 
    style_tree: style tree of the drawio file
  """

  def __init__(self, style_tree):
    self.style_tree = style_tree

  def convert_to_sytax_tree(self):
    """
    Convert the style tree to sytnax tree

    Returns:
      syntax_tree: the syntax tree that is used by the generators  
    """

    print("<<< CONVERTING STYLE TREE TO SYNTAX TREE >>>")    

    try:
      syntax_tree = dict()
      cells = self.style_tree['root']['cells']
      relationships = self.style_tree['root']['relationships']
      parent = self.style_tree['root']['id']

      propertiesDone = False

      _id = 0
      for key, value in cells.items():
        
        if value['parent_id'] in relationships.keys() or "endArrow" in value['style'].keys():  
          # skip the label for relationships
          continue

        if value['parent_id'] == parent and value['style']['type'].lower() == 'swimlane' or value['style']['type'].lower() == 'html':
          # start of a new cell 
          syntax_tree[key] = self._tree_template(value)
          propertiesDone = False
          _id = 0
        else:
          # properties and methods in the cell 
          if value['style']['type'].lower() == 'line' and value['parent_id'] in syntax_tree.keys():  # line seperating the properties and methods
            propertiesDone = True
            _id = 0
          else:
            if not propertiesDone:  # properties
              syntax_tree[value['parent_id']]['properties'] = {**syntax_tree[value['parent_id']]['properties'], **self._properties_template(value, _id)}
              _id += len(value['values'])
            else: # methods
              syntax_tree[value['parent_id']]['methods'] = {**syntax_tree[value['parent_id']]['methods'], **self._methods_template(value, _id)}
              _id += len(value['values'])

      for relationship in relationships.keys():
        self._add_relationships(syntax_tree, relationships[relationship])

      return syntax_tree
    except Exception as e:
      print(f"SyntaxParser.convert_to_sytax_tree ERROR: {e}")
  
  def _tree_template(self, main_cell):
    """
    Create the template that will house each cell

    Parameters:
      main_cell: the starting, parent cell
    
    Returns:
      template: the starting template (dictionary)
    """

    template =  {
      'type': "class",
      'name': main_cell['values'][0] if len(main_cell['values']) > 0 else "",
      'properties': {},
      'methods': {},
      'relationships': {
        'implements': [],
        'extends': [],
        'association': [],
        'aggregation': [],
        'composition': []
      }
    }

    if main_cell['style']['type'] == "html":
      values_length = len(main_cell['values'])
      name = main_cell['values'][0] if values_length > 0 else None
      properties = {'values': main_cell['values'][1] if values_length > 1 else None}
      methods = {'values': main_cell['values'][2] if values_length > 2 else None}
      
      template['name'] = name[0]
      template['properties'] = self._properties_template(properties, 0) if not None else []
      template['methods'] = self._methods_template(methods, 0) if not None else []
      

    if "fontStyle" in main_cell['style'] and main_cell['style']['fontStyle'] == "2": 
      # if the fontStyle is italic, then it is an abstract class
      template['type'] = "abstract"
    elif template['name'].lower().startswith("<<interface>>"):
      template['type'] = "interface"
      template['name'] = template['name'][13:]

    return template

  def _properties_template(self, property_dict, _id):
    """
    Create the template for properties 

    Parameters:
      property_dict: the properties dictionary from the style tree 
      _id: id for the keys in the dictionary
    
    Returns:
      template: the properties tempate (dictionary) 
    """

    values = property_dict['values']
    template = dict()

    for val in values:
      if len(val) == 0:
        continue 

      _id += 1

      val = val.strip()
      access_modifier_symbol = val[0]
      temp_val = val[1:].split(":")

      template[_id] = {
        'access': self._get_access_modifier(access_modifier_symbol),
        'name': temp_val[0].strip(),
        'type': temp_val[1].strip(),
      }

    return template
  
  def _methods_template(self, method_dict, _id):
    """
    Create the template for methods 

    Parameters:
      method_dict: the methods dictionary from the style tree 
      _id: id for the keys in the dictionary
    
    Returns:
      template: the methods tempate (dictionary) 
    """
    
    values = method_dict['values']
    template = dict()

    for val in values:
      if len(val) == 0:
        continue 

      _id += 1

      val = val.strip()
      access_modifier_symbol = val[0]
      temp_val = val[1:].split(":")

      template[_id] = {
        'access': self._get_access_modifier(access_modifier_symbol),
        'name': temp_val[0].strip(),
        'return_type': temp_val[1].strip(),
      }

    return template
  
  def _get_access_modifier(self, symbol):
    """
    Return the access modifier

    Parameters:
      symbol: symbol representing the access modifier 
    
    Returns:
      text: the text of the access modifier symbol
    """

    access_modifier_dict = {
      '+': "public",
      '#': "protected",
      '-': "private"
    }

    return access_modifier_dict[symbol]

  def _add_relationships(self, syntax_tree, relationship):
    """
    Add the relationship for the cells in the syntax tree

    Parameters:
      syntax_tree: the syntax_tree dictionary
      relationship: relationship to be added to the syntax tree
    """
    
    source = relationship['source']
    target = relationship['target']
    style = relationship['style']

    source_cell = syntax_tree[source]
    target_cell = syntax_tree[target]

    if "endArrow" in style.keys() and (style['endArrow'].lower() == "block" or style['endArrow'].lower() == "none"):
      if style['endArrow'].lower() == "none" or style['endFill'].lower() == "1":
        # association
        target_cell['relationships']['association'] += [source]
      elif "dashed" in style.keys() and style['dashed'] == "1":
        # implements 
        source_cell['relationships']['implements'] += [target]        
      else:
        # extends 
        source_cell['relationships']['extends'] += [target]        
    elif ("endArrow" in style.keys() and style['endArrow'].lower() == "diamondthin") or \
      ("startArrow" in style.keys() and style['startArrow'].lower() == "diamondthin"):
      if  "endFill" in style.keys() and style['endFill'] == "1":
        # composition
        target_cell['relationships']['composition'] += [source]        
      else: 
        # aggregation 
        target_cell['relationships']['aggregation'] += [source]        
