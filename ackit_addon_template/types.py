""" File generated automatically by ackit (Addon Creator Kit). """
import numpy
import typing
from typing import List, Set, Tuple, Dict, Any

import bpy
import bpy_types
import bl_ext
from bpy.types import Context


""" Addon-Defined PropertyGroup: """
class ACKITADDONTEMPLATE_AddonPreferences:
	bl_idname: str


# ++++++++++++++++++++++++++++++++++++++++++++++++++
""" Extended bpy.types classes by the addon: """

# ++++++++++++++++++++++++++++++++++++++++++++++++++
""" Root PropertyGroups (linked directly to any bpy.types): """
class RootPG:
	@staticmethod
	def Preferences(context: bpy.types.Context) -> ACKITADDONTEMPLATE_AddonPreferences:
		return context.preferences.addons['bl_ext.vscode_development.ackit_addon_template'].preferences


# Alias:
ackit_addon_template_types = RootPG

# ++++++++++++++++++++++++++++++++++++++++++++++++++
