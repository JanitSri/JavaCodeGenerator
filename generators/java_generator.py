import re
from generators.code_generator import CodeGeneratorInterface

class JavaCodeGenerator(CodeGeneratorInterface):
    """
    Generate Java code

    Parameters:
        syntax_tree: syntax_tree of the drawio file 
        file_path: path for the code files to be written to 
    """

    def __init__(self, syntax_tree, file_path):
        self.__syntax_tree = syntax_tree
        self.file_path = file_path.strip('/')
        self.__classes = list()
        self.__properties = list()
        self.__methods = list()
        self.__files = list()
    
    def generate_code(self):
        """
        Use the syntax tree to generate code files for the UML class diagrams 
        """
        
        print("<<< GENERATING CODE FILES FROM SYNTAX TREE >>>")

        try:
            for _, _class in self.__syntax_tree.items():
                file = ""
                
                inheritance = ""
                if len(_class['relationships']['extends']) > 0:
                    inheritance += "extends "
                    inheritance += ",".join([self.__syntax_tree[r]['name'] for r in _class['relationships']['extends']]).strip(",")
                    
                implementation = "" 
                if len(_class['relationships']['implements']) > 0:
                    implementation += "implements "
                    implementation += ",".join([self.__syntax_tree[r]['name'] for r in _class['relationships']['implements']]).strip(",")


                interface_methods = list()
                self.get_interface_methods(_class['relationships']['implements'], interface_methods)

                file += self.generate_classes(_class['type'], _class['name'], inheritance, implementation)
                file += "\n"
                file += self.generate_properties(_class['properties'])
                file += "\n"
                file += self.generate_methods(_class['methods'], _class['properties'], _class['type'], interface_methods)
                file += "}\n" 
                self.__files.append([_class['name'], file])

            self.generate_files()
        
        except Exception as e:
            print(f"JavaCodeGenerator.generate_code ERROR: {e}")

    def generate_classes(self, class_type, class_name, extends, implements):
        """
        Generate the class header 

        Parameters:
            class_type: type of class; 'class', 'abstract', 'interface'
            class_name: name of class
            extends: the classes extended by this class
            implements: the interfaces implemented by this class

        Returns:
            class_header: class header string
        """

        type_of_class = "public class" if class_type == "class" else class_type
        type_of_class = class_type + " class" if class_type == "abstract" else type_of_class

        class_header = f"{type_of_class} {class_name} {extends} {implements}" + " {\n"
        class_header = re.sub(' +', ' ', class_header)
        self.__classes.append(class_header)
        return class_header
   
    def get_classes(self):
        """
        Getter for classes
        """

        return self.__classes
 
    def generate_properties(self, properties):
        """
        Generate properties for the class 

        Parameters:
            properties: dictionary of properties

        Returns:
            properties_string: string of the properties
        """

        properties_string = ""
        for _, _property_value in properties.items():
            p = f"\t{_property_value['access']} {_property_value['type']} {_property_value['name']};\n"
            self.__properties.append(p)
            properties_string += p 
 
        return properties_string

    def get_properties(self):
        """
        Getter for properties
        """

        return self.__properties

    def generate_methods(self, methods, properties, class_type, interface_methods):
        """
        Generate methods for the class

        Parameters:
            methods: dictionary of methods
            properties: dictionary of properties
            class_type: type of current class
            interface_method: methods of implemented interfaces
        
        Returns:
            methods_string: string of the methods 
        """
        
        methods_string = ""
        for _, method_value in methods.items():
            m = f"\t{method_value['access']} {method_value['return_type']} {method_value['name']}() {{}}\n";
            methods_string += m + "\n"
            self.__methods.append(m)

        # getter and setter methods
        if class_type == "class" or class_type == "abstract":
            for _, _property_value in properties.items():
                if _property_value['access'] == "private":
                    getter = (f"\tpublic {_property_value['type']} get{_property_value['name'][0].upper() + _property_value['name'][1:]}()"
                              f" {{\n \t\treturn this.{_property_value['name']}; \n\t}}\n");
                    methods_string += getter + "\n"
                    self.__methods.append(getter)

                    setter = (f"\tpublic void set{_property_value['name'].capitalize()}({_property_value['type']} {_property_value['name']})"
                              f" {{\n \t\tthis.{_property_value['name']} = {_property_value['name']}; \n\t}}\n")
                    methods_string += setter + "\n"
                    self.__methods.append(setter)
            
            for interface_method in interface_methods:
                comment = "// ***requires implementation***"
                m = (f"\t {interface_method['access']} {interface_method['return_type']} {interface_method['name']}()"
                     f" {{\n \t\t{comment} \n\t}}\n")
                methods_string += m + "\n"
                self.__methods.append(m)

        return methods_string

    def get_methods(self):
        """
        Getter for the methods
        """        

        return self.__methods

    def get_interface_methods(self, implements, interface_list): 
        """
        Get the interface methods that require implementation
        
        Parameters:
            implements: list of interfaces
            interface_list: list of interface methods
        """

        for i in implements:
            interface_obj = self.__syntax_tree[i]
            interface_list += interface_obj['methods'].values()
            self.get_interface_methods(interface_obj['relationships']['implements'], interface_list)

    def generate_files(self):
        """
        Write generated code to file 

        Returns:
            boolean: True if successful, False if unsuccessful
        """

        print(f"<<< WRITING FILES TO {self.file_path} >>>")

        try:
            for file in self.get_files():
                file_name = file[0] + ".java"
                file_contents = file[1]
                with open(self.file_path + f"/{file_name}", "w") as f:
                    f.write(file_contents)
        except Exception as e:
            print(f"JavaCodeGenerator.generate_files ERROR: {e}")            

    def get_files(self):
        """
        Getter for the files 
        """

        return self.__files
