from pprint import pprint


def introspection_info(obj):

    obj_type = type(obj).__name__

    obj_module = obj.__module__ if hasattr(obj, '__module__') else 'built-in'

    all_attributes = dir(obj)

    attributes = [attr for attr in all_attributes if not callable(getattr(obj, attr))]
    methods = [method for method in all_attributes if callable(getattr(obj, method))]

    info = {
        'type': obj_type,
        'module': obj_module,
        'attributes': attributes,
        'methods': methods
    }

    return info


class SampleClass:
    def __init__(self, value):
        self.value = value

    def example_method(self):
        return self.value


sample_object = SampleClass('world')

object_info = introspection_info(sample_object)
pprint(object_info)
