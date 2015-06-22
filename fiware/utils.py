from django.utils.importlib import import_module


def import_class(class_string):
    module, classname = class_string.rsplit(".", 1)
    m = import_module(module)
    return getattr(m, classname)
