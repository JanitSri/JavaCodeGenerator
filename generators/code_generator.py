from abc import ABC, abstractmethod

class CodeGeneratorInterface(ABC):
    """
    Interface contract for code generation
    """

    @abstractmethod
    def generate_code():
        pass

    @abstractmethod
    def generate_classes():
        pass

    @abstractmethod
    def get_classes():
        pass
    
    @abstractmethod
    def generate_properties():
        pass
    
    @abstractmethod
    def get_properties():
        pass

    @abstractmethod
    def generate_methods():
        pass

    @abstractmethod
    def get_methods():
        pass

    @abstractmethod
    def generate_files():
        pass
    
    @abstractmethod
    def get_files():
        pass
