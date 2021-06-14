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
        
        print("<<< GENERATING FILES >>>")

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

                file += self.generate_classes(_class['type'], _class['name'], inheritance, implementation)
                file += "\n"
                file += self.generate_properties(_class['properties'])
                file += "\n"
                file += self.generate_methods(_class['methods'])
                file += "}\n" 
                self.__files.append([_class['name'], file])

            self.generate_files()
        
        except Exception as e:
            print(f"JavaCodeGenerator.generate_code ERROR: {e}")

    def generate_classes(self, class_type, class_name, extends, implements):
        """
        Generate the class header 

        Returns:
            class_header: class header string
        """

        type_of_class = "class" if class_type == "class" else class_type
        type_of_class = class_type + " class" if class_type == "abstract" else type_of_class

        class_header = f"public {type_of_class} {class_name} {extends} {implements}" + " {\n"
        class_header = re.sub(' +', ' ', class_header)
        self.__classes.append(class_header)
        return class_header
   
    def get_classes(self):
        """
        Getter for classes
        """
        print("getting all clases")
        return self.__classes
 
    def generate_properties(self, properties):
        """
        Generate properties for the class 

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

        print("getting all properties")
        return self.__properties

    def generate_methods(self, methods):
        """
        Generate methods for the class
        
        Returns:
            methods_string: string of the methods 
        """
        
        methods_string = ""
        for _, method_value in methods.items():
            m = f"\t{method_value['access']} {method_value['return_type']} {method_value['name']}() {{}}\n";
            self.__methods.append(m)
            methods_string += m

        return methods_string

    def get_methods(self):
        """
        Getter for the methods
        """

        print("getting all methods")
        return self.__methods

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

        print("getting all files")
        return self.__files
