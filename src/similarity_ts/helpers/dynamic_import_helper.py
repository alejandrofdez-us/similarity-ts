import importlib
import os


def find_available_classes(folder_path, parent_class, package):
    available_classes = {}
    for _, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.py'):
                module_name = file_name[:-3]
                module = importlib.import_module(f'similarity_ts.{package}.{module_name}', package=package)
                if __is_module_subclass(module, module_name, parent_class):
                    available_class = getattr(module, __to_camel_case(module_name))()
                    available_classes[available_class.name] = available_class
    return available_classes


def __is_module_subclass(module, module_name, parent_class):
    if module is not None:
        class_name = __to_camel_case(module_name)
        if parent_class.__name__ != module_name.capitalize():
            return hasattr(module, class_name) and issubclass(getattr(module, class_name), parent_class)
    return False



def __to_camel_case(snake_str):
    components = snake_str.split('_')
    return ''.join(x.capitalize() for x in components)
