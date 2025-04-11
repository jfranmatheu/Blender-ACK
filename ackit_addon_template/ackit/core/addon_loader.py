import sys
from collections import defaultdict

from bpy.utils import register_class, unregister_class

from ..globals import GLOBALS
from .reg_utils import get_all_submodules
from .reg_utils import get_ordered_classes_to_register
from ..auto_code import AutoCode
from ..utils.callback import CallbackDict
from ..debug import print_debug


__all__ = [
    'AddonLoader',
]


callback_ids = ['init', 'late_init', 'register', 'late_register', 'unregister', 'late_unregister']


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
    module_callbacks = CallbackDict()

    @classmethod
    def init_modules(cls, use_autoload: bool = False, auto_code: set[AutoCode] = set()):
        print_debug("Initializing...")
        cls.use_autoload = use_autoload

        if cls.modules is not None:
            print_debug("Cleaning old modules!")
            cls.cleanse_modules()

        cls.modules = get_all_submodules(GLOBALS.ADDON_SOURCE_PATH)
        cls.fetch_module_callbacks()
        if cls.use_autoload:
            cls.ordered_classes = get_ordered_classes_to_register(cls.modules)

        cls.registered = False

        cls.module_callbacks.call_callbacks('init')
        cls.module_callbacks.call_callbacks('late_init')

        if auto_code:
            for auto_code_func in auto_code:
                auto_code_func()

    @classmethod
    def register_modules(cls):
        print_debug("Registering...")

        if cls.modules is None:
            cls.init_modules()

        if cls.registered:
            print_debug("Trying to register but it is already registered!")
            return

        if cls.use_autoload:
            for cls in cls.ordered_classes:
                if not hasattr(cls, 'bl_rna'):
                    register_class(cls)

        cls.module_callbacks.call_callbacks('register')
        cls.module_callbacks.call_callbacks('late_register')

        cls.registered = True

    @classmethod
    def unregister_modules(cls):
        print_debug("Unregistering...")

        if not cls.registered:
            print_debug("Trying to unregister but it is not registered!")
            return

        if cls.use_autoload:
            for cls in reversed(cls.ordered_classes):
                if hasattr(cls, 'bl_rna'):
                    unregister_class(cls)

        cls.module_callbacks.call_callbacks('unregister')
        cls.module_callbacks.call_callbacks('late_unregister')

        cls.registered = False
    
    @classmethod
    def fetch_module_callbacks(cls):
        for module in cls.modules:
            for callback_id in callback_ids:
                if hasattr(module, callback_id):
                    cls.module_callbacks.add_callback(callback_id, getattr(module, callback_id))

    @classmethod
    def cleanse_modules(cls):
        cls.module_callbacks.clear_callbacks()

        # Based on https://devtalk.blender.org/t/plugin-hot-reload-by-cleaning-sys-modules/20040
        sys_modules = sys.modules
        sorted_addon_modules = sorted([module.__name__ for module in cls.modules])
        for module_name in sorted_addon_modules:
            del sys_modules[module_name]
