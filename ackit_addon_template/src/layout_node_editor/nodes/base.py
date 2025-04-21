from typing import Dict, Any, Optional, List
import bpy
from bpy import types as bpy_types


class BaseNode:
    label: str
    inputs: List[bpy_types.NodeSocket]

    def apply_layout_properties(self, layout: bpy_types.UILayout):
        pass

    def _execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        context, root_layout = args
        parent_layout: Optional[bpy_types.UILayout] = kwargs.get('parent_layout', None)
        if not parent_layout:
            print(f"Warning: Node '{self.label}' executed without 'parent_layout' in kwargs.")
        parent_layout = parent_layout or root_layout
        ret = self.execute(context, parent_layout)
        if ret is None:
            return None
        self.apply_layout_properties(ret if isinstance(ret, bpy_types.UILayout) else ret['parent_layout'])
        if isinstance(ret, dict):
            if 'parent_layout' in ret:
                return ret
            else:
                # TODO: Handle other types of return values
                # here we suppose it's a dict with sockets as keys and values as return values for those sockets
                return ret
            '''elif isinstance(list(ret.keys())[0], NodeSocket):
                ret_d = {}
                for idx, input in enumerate(self.inputs):
                    ret_d[input] = ret[idx]
                return ret_d'''
        elif isinstance(ret, bpy_types.UILayout):
            ret = {'parent_layout': ret}
        elif isinstance(ret, tuple):
            ret_d = {}
            for idx, input in enumerate(self.inputs):
                ret_d[input] = ret[idx]
            ret = ret_d
        return ret

    # Default execute - subclasses should override to create specific layout type
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout):
        print(f"Warning: LayoutNodeBase execute called directly for {self.label}. Subclass should override.")
        return layout
