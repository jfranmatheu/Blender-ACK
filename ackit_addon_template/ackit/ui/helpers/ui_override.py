from ..btypes.base import DrawExtension
from ...globals import GLOBALS


class UIOverride:
    _cache = {}

    @classmethod
    def restore_all(cls):
        for orig_cls, orig_data in cls._cache.items():
            for attr_name, attr_value in orig_data.items():
                setattr(orig_cls, attr_name, attr_value)

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()

    @classmethod
    def get_attr_from_cache(cls, target_cls, attr: str, fallback=None):
        if target_cls not in cls._cache:
            return fallback
        return cls._cache[target_cls].get(attr, fallback)

    @classmethod
    def save_backup(cls, cls_to_backup):
        cls._cache[cls_to_backup] = cls_to_backup.__dict__.copy()

    @staticmethod
    def decodecorator(bl_ui_class_to_override, poll) -> DrawExtension:
        # Backup of the original methods from bl ui class.
        UIOverride.save_backup(bl_ui_class_to_override)

        def method_decorator(fun):
            def wrapper(self, context, *args, **kwargs):
                if not fun.poll(context):
                    return fun.original_fun(self, context, *args, **kwargs)
                if fun.__name__.startswith('draw'):
                    fargs = (self, context, self.layout)
                else:
                    fargs = (self, context)
                return fun(*fargs, *args, **kwargs)
            return wrapper

        def decowrap(_decorated_cls):
            ''' cls is the decorated class. '''
            decorated_cls = type(
                GLOBALS.ADDON_MODULE_UPPER + '_OVERRIDE_' + _decorated_cls.__name__,
                (_decorated_cls, DrawExtension),
                {}
            )
            # Add reference of the original class.
            # setattr(decorated_cls, 'original_class', bl_ui_class_to_override)
            # Override original methods.
            for attribute_name in dir(decorated_cls):
                potential_fun = getattr(decorated_cls, attribute_name)
                # Check that it is callable
                # Filter all dunder (__ prefix) methods
                if callable(potential_fun) and not attribute_name.startswith('__'):
                    setattr(bl_ui_class_to_override, attribute_name, potential_fun)

                    # HACK. Add fake poll func to the original class method...
                    setattr(getattr(bl_ui_class_to_override, attribute_name), 'poll', poll)
                    # HACK. Add old func reference to the override method...
                    setattr(
                        getattr(bl_ui_class_to_override, attribute_name),
                        'original_fun',
                        UIOverride.get_attr_from_cache(bl_ui_class_to_override, attribute_name)
                    )
                    # Add decorator for the context:
                    setattr(
                        bl_ui_class_to_override,
                        attribute_name,
                        method_decorator(getattr(bl_ui_class_to_override, attribute_name))
                    )
            return decorated_cls
        return decowrap


def unregister():
    UIOverride.clear_cache()
