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

    try:
      syntax_tree = dict()
      cells = self.style_tree['root']['cells']
      relationships = self.style_tree['root']['relationships']
      parent = self.style_tree['root']['id']

      propertiesDone = False

      for key, value in cells.items():
        if value['parent_id'] == parent and value['style']['type'].lower() == 'swimlane':
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

      return syntax_tree
    except Exception as e:
      print(f"SyntaxParser.convert_to_sytax_tree ERROR: {e}")
  
  def _tree_template(self, main_cell):
    """
    Create the template thta will house each cell

    Parameters:
      main_cell: the starting, parent cell
    
    Returns:
      template: the starting template (dictionary)
    """

    return {
      'type': "class | interface | abstract",
      "name": main_cell["values"][0] if len(main_cell["values"]) > 0 else "",
      'properties': {},
      'methods': {},
      'relationships': {
        'implements': [],
        'extends': []
      }
    }
  
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
      _id += 1

      val = val.strip()
      access_modifier_symbol = val[0]
      temp_val = val[1:].split(":")

      template[_id] = {
        "access": self._get_access_modifier(access_modifier_symbol),
        "name": temp_val[0].strip(),
        "type": temp_val[1].strip(),
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
      _id += 1

      val = val.strip()
      access_modifier_symbol = val[0]
      temp_val = val[1:].split(":")

      template[_id] = {
        "access": self._get_access_modifier(access_modifier_symbol),
        "name": temp_val[0].strip(),
        "return_type": temp_val[1].strip(),
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
      "+": "public",
      "#": "protected",
      "-": "private"
    }
    return access_modifier_dict[symbol]
