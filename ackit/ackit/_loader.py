import sys

from bpy.utils import register_class, unregister_class

from ._globals import GLOBALS
from .utils.modules import get_all_submodules
from .utils.classes import get_ordered_classes_to_register
from ._auto_code import AutoCode


__all__ = [
    'AutoLoad',
    'AddonLoader',
]


class AutoLoad:
    """# Auto-Load

    Utility class for automatically fetching and registering Blender bpy classes.

    ## WARNING
    - Legacy method. Recommended to use `AddonLoader` instead!
    - In case of using, DO NOT use in combination with `AddonLoader` !!!

    ## HOW TO USE:
    - 1. Call `AutoLoad.init_modules()` in the root `__init__.py` file of your addon/extension.
    - 2. Call `AutoLoad.register_modules()` in a `register()` function inside your root `__init__.py`.
    - 3. Call `AutoLoad.unregister_modules()` in a `unregister()` function inside your root `__init__.py`.
    
    - In the modules of your addon you can add ``register()`` and ``unregister()`` methods
    that will be automatically called by the ``AutoLoad`` when addon registering and unregistering events occur.
    """

    modules = None
    ordered_classes = None

    @classmethod
    def init_autoload(cls):
        cls.modules = get_all_submodules(GLOBALS.ADDON_SOURCE_PATH)
        cls.ordered_classes = get_ordered_classes_to_register(cls.modules)

    @classmethod
    def register_autoload(cls):
        for cls in cls.ordered_classes:
            register_class(cls)

        for module in cls.modules:
            if hasattr(module, "register"):
                module.register()

    @classmethod
    def unregister_autoload(cls):
        for cls in reversed(cls.ordered_classes):
            unregister_class(cls)

        for module in cls.modules:
            if hasattr(module, "unregister"):
                module.unregister()


class AddonLoader:
    """# AddonLoader
    Utility class for automatically fetching and registering ACKit classes.

    ## About ACKit

    ACKit is meant as a wrapper of the bpy Blender API so Blender classes should be
    registered via ACKit ``Register`` utility so that ``AddonLoader`` can detect and
    handle them properly.

    ## HOW TO USE:
    - 1. Call `AddonLoader.init_modules()` in the root `__init__.py` file of your addon/extension.
    - 2. Call `AddonLoader.register_modules()` in a `register()` function inside your root `__init__.py`.
    - 3. Call `AddonLoader.unregister_modules()` in a `unregister()` function inside your root `__init__.py`.
    
    - In the modules of your addon you can add ``register()``, ``late_register()``, ``unregister()`` and ``late_unregister()`` methods
    that will be automatically called by the ``AddonLoader`` when addon registering and unregistering events occur.
    """

    modules = None
    registered = False
    use_autoload = False
    ordered_classes = None  # If using AutoLoad.

    @classmethod
    def init_modules(cls, use_autoload: bool = False, auto_code: set[AutoCode] = set(), auto_code_prefix: str | None = None):
        cls.use_autoload = use_autoload

        if cls.modules is not None:
            cls.cleanse_modules()

        cls.modules = get_all_submodules(GLOBALS.ADDON_SOURCE_PATH)
        if cls.use_autoload:
            cls.ordered_classes = get_ordered_classes_to_register(cls.modules)

        cls.registered = False

        for module in cls.modules:
            # When you need to initialize something specific in this module.
            if hasattr(module, "init"):
                module.init()

        for module in cls.modules:
            # When you need to initialize something that depends on another module initialization.
            if hasattr(module, "late_init"):
                module.late_init()

        sys.modules[GLOBALS.ADDON_MODULE_SHORT] = sys.modules[GLOBALS.ADDON_MODULE]

        if auto_code:
            for auto_code_func in auto_code:
                auto_code_func(filename_prefix=auto_code_prefix)

    @classmethod
    def register_modules(cls):
        if cls.modules is None:
            cls.init_modules()

        if cls.registered:
            return

        if cls.use_autoload:
            for cls in cls.ordered_classes:
                register_class(cls)

        for module in cls.modules:
            if hasattr(module, "register"):
                module.register()

        for module in cls.modules:
            if hasattr(module, "late_register"):
                module.late_register()

        cls.registered = True

    @classmethod
    def unregister_modules(cls):
        if not cls.registered:
            return

        if cls.use_autoload:
            for cls in reversed(cls.ordered_classes):
                unregister_class(cls)

        for module in cls.modules:
            if hasattr(module, "unregister"):
                module.unregister()

        for module in cls.modules:
            if hasattr(module, "late_unregister"):
                module.unregister()

        cls.registered = False

    @classmethod
    def cleanse_modules(cls):
        # Based on https://devtalk.blender.org/t/plugin-hot-reload-by-cleaning-sys-modules/20040
        sys_modules = sys.modules
        sorted_addon_modules = sorted([module.__name__ for module in cls.modules])
        for module_name in sorted_addon_modules:
            del sys_modules[module_name]
