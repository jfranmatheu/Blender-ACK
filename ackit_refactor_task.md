# ACKIT Module Refactoring Plan (v4)

## Objective

Reorganize the `ackit` Python module structure to align with the logical domains in `ackit/_ack.py` (`ACK`). Move code from `registry` and `types` into new domain directories (`ops`, `ui`, `ne`, `data`, `app`) and `core`/`utils`. **Crucially, within each domain (`ops`, `ui`, `ne`, `data`), create a `btypes` subdirectory to hold individual files for each core ACKit base class.** Functionality must be preserved.

## Analysis Summary

*   Current structure mixes technical concerns (registration, types, flags).
*   Target structure uses domains (`Ops`, `UI`, `NE`, `Data`, `App`) from `_ack.py`, plus `core`, `utils`, `flags`, `metadata`.
*   **Key Change:** Base `ackit` classes (e.g., `Operator`, `Panel`, `Node`) will reside in separate files within `[domain]/btypes/` subdirectories (e.g., `ackit/ops/btypes/generic.py` for `Operator`). Creator methods stay with their base class.
*   `core/btypes.py` (original low-level Blender type hints) is distinct from `[domain]/btypes/` (ackit classes).
*   `NodeInput`/`NodeOutput` functions move from `_ack.py` to `ne/annotations.py`, using internal logic moved to `ne/annotations_internal.py`.
*   Other domain-specific helpers (`data/helpers.py`, `ne/categories.py`, etc.) remain in their planned locations at the domain level.
*   Central `flags.py`, `metadata.py` are retained.
*   `docs/api/ack.md` needs updating post-refactor.

## Current Structure (Relevant Parts - Simplified)

```text
ackit/
├── _ack.py             # Defines TARGET facade, includes NodeInput/Output funcs
├── registry/
│   ├── addon_loader.py # -> core/
│   ├── auto_load.py    # -> core/
│   ├── btypes.py       # -> core/btypes.py (Low-level types)
│   ├── flags/          # -> flags.py
│   ├── metadata.py     # -> metadata.py
│   ├── polling.py      # -> utils/polling.py
│   ├── props/          # -> data/props.py
│   ├── reg_deco/       # -> app/, data/subscriptions.py
│   ├── reg_helpers/    # -> data/helpers.py
│   ├── reg_types/      # Contains base ACKit classes
│   │   ├── data/       # -> data/btypes/
│   │   │   ├── prefs.py
│   │   │   └── prop_group.py
│   │   ├── nodes/      # -> ne/btypes/, ne/categories.py
│   │   │   ├── node.py
│   │   │   ├── node_cats.py
│   │   │   ├── node_socket.py
│   │   │   ├── node_tree.py
│   │   │   └── sockets/
│   │   │       └── annotation.py # -> ne/annotations_internal.py
│   │   ├── ops/        # -> ops/btypes/
│   │   │   ├── action.py
│   │   │   ├── generic.py
│   │   │   └── modal.py
│   │   └── ui/         # -> ui/btypes/
│   │       ├── menu.py
│   │       ├── panel.py
│   │       ├── pie_menu.py
│   │       ├── popover.py
│   │       └── ui_list.py
│   └── utils.py        # -> core/reg_utils.py
├── types/
│   └── nodes/
│       └── socket_types.py # -> ne/socket_types.py
└── ...
```

## Target Structure (Proposed - v4)

```text
ackit/
├── __init__.py
├── _ack.py             # Facade - Imports updated
├── app/                # App Handlers, Timers, Keymaps
│   ├── __init__.py
│   ├── handlers.py
│   ├── keymaps.py
│   └── timers.py
├── core/               # Core loading, registration utils, base Blender type hints
│   ├── __init__.py
│   ├── addon_loader.py
│   ├── auto_load.py
│   ├── btypes.py       # Original low-level Blender type hints/wrappers
│   └── reg_utils.py
├── data/               # Properties, Preferences, RNA Subscriptions
│   ├── __init__.py
│   ├── btypes/         # ACKIT base classes for data types
│   │   ├── __init__.py
│   │   ├── addon_preferences.py # Moved from registry/reg_types/data/prefs.py
│   │   └── property_group.py    # Moved from registry/reg_types/data/prop_group.py
│   ├── helpers.py      # Property registration helpers
│   ├── props.py        # Property definitions
│   └── subscriptions.py # RNA decorators
├── enums/              # Existing
├── flags.py            # Centralized flags
├── globals.py          # Existing - Review later
├── metadata.py         # Centralized metadata
├── ne/                 # Node Editor components
│   ├── __init__.py
│   ├── annotations.py  # Public NodeInput/Output functions (from _ack.py)
│   ├── annotations_internal.py # Internal _NodeSocket... (from registry...annotation.py)
│   ├── btypes/         # ACKIT base classes for NE types
│   │   ├── __init__.py
│   │   ├── node.py        # Moved from registry/reg_types/nodes/node.py
│   │   ├── node_socket.py # Moved from registry/reg_types/nodes/node_socket.py
│   │   └── node_tree.py   # Moved from registry/reg_types/nodes/node_tree.py
│   ├── categories.py   # Node category logic (from registry...node_cats.py)
│   └── socket_types.py # Socket type definitions (from types...socket_types.py)
├── ops/                # Operators
│   ├── __init__.py
│   └── btypes/         # ACKIT base classes for Ops + creators
│       ├── __init__.py
│       ├── action.py     # Moved from registry/reg_types/ops/action.py
│       ├── generic.py    # Moved from registry/reg_types/ops/generic.py
│       └── modal.py      # Moved from registry/reg_types/ops/modal.py
├── ui/                 # UI Elements
│   ├── __init__.py
│   └── btypes/         # ACKIT base classes for UI + creators
│       ├── __init__.py
│       ├── menu.py       # Moved from registry/reg_types/ui/menu.py
│       ├── panel.py      # Moved from registry/reg_types/ui/panel.py
│       ├── pie_menu.py   # Moved from registry/reg_types/ui/pie_menu.py
│       ├── popover.py    # Moved from registry/reg_types/ui/popover.py
│       └── ui_list.py    # Moved from registry/reg_types/ui/ui_list.py
└── utils/              # General Utilities
    ├── __init__.py
    └── polling.py      # Moved from registry/polling.py
```
*(Note: `registry`, `types`, empty `decorators` directories removed after refactor).*

## Tasks

1.  **Create New Directories & Subdirectories:**
    *   `ackit/app/`
    *   `ackit/core/`
    *   `ackit/data/`, `ackit/data/btypes/`
    *   `ackit/ne/`, `ackit/ne/btypes/`
    *   `ackit/ops/`, `ackit/ops/btypes/`
    *   `ackit/ui/`, `ackit/ui/btypes/`
    *   Ensure `ackit/utils/` exists.

2.  **Move & Consolidate Files (More Granular):**
    *   **App:** Move `handlers.py`, `timer.py`, `keymaps.py` from `registry/reg_deco/` to `app/`.
    *   **Core:** Move `addon_loader.py`, `auto_load.py`, `btypes.py`, `utils.py` (rename to `reg_utils.py`) from `registry/` to `core/`.
    *   **Data:**
        *   Move `registry/reg_types/data/prefs.py` to `data/btypes/addon_preferences.py`.
        *   Move `registry/reg_types/data/prop_group.py` to `data/btypes/property_group.py`.
        *   Merge `registry/props/property.py` and `registry/props/typed/` contents into `data/props.py`.
        *   Move `registry/reg_helpers/props.py` to `data/helpers.py`.
        *   Move `registry/reg_deco/rna_sub.py` to `data/subscriptions.py`.
    *   **Flags:** Create `ackit/flags.py`. Consolidate definitions from files in `registry/flags/`.
    *   **Metadata:** Move `registry/metadata.py` to `ackit/metadata.py`.
    *   **NE:**
        *   Move `registry/reg_types/nodes/node.py` to `ne/btypes/node.py`.
        *   Move `registry/reg_types/nodes/node_tree.py` to `ne/btypes/node_tree.py`.
        *   Move `registry/reg_types/nodes/node_socket.py` to `ne/btypes/node_socket.py`.
        *   Move `registry/reg_types/nodes/node_cats.py` to `ne/categories.py`.
        *   Move `registry/reg_types/nodes/sockets/annotation.py` to `ne/annotations_internal.py`.
        *   Move `types/nodes/socket_types.py` to `ne/socket_types.py`.
        *   **Create `ne/annotations.py` and move `NodeInput`/`NodeOutput` function definitions from `_ack.py` into it.**
    *   **Ops:**
        *   Move `registry/reg_types/ops/generic.py` to `ops/btypes/generic.py`.
        *   Move `registry/reg_types/ops/action.py` to `ops/btypes/action.py`.
        *   Move `registry/reg_types/ops/modal.py` to `ops/btypes/modal.py`.
    *   **UI:**
        *   Move `registry/reg_types/ui/panel.py` to `ui/btypes/panel.py`.
        *   Move `registry/reg_types/ui/menu.py` to `ui/btypes/menu.py`.
        *   Move `registry/reg_types/ui/pie_menu.py` to `ui/btypes/pie_menu.py`.
        *   Move `registry/reg_types/ui/popover.py` to `ui/btypes/popover.py`.
        *   Move `registry/reg_types/ui/ui_list.py` to `ui/btypes/ui_list.py`.
    *   **Utils:** Move `registry/polling.py` to `utils/polling.py`.

3.  **Update Imports & Code:**
    *   In `ne/annotations.py`, import internal logic relatively: `from .annotations_internal import _NodeSocketInput, _NodeSocketOutput`.
    *   In `ackit/_ack.py`:
        *   Remove `NodeInput`/`NodeOutput` definitions.
        *   Replace *all* old imports with correct, specific imports from the new structure. Examples: `from .ops.btypes.generic import Operator`, `from .ui.btypes.panel import Panel`, `from .ne.annotations import NodeInput, NodeOutput`, `from .flags import OPERATOR`, `from .data.props import PropertyTypes`.
    *   Go through *all other moved files* and meticulously update their internal imports. Use relative imports (`.`, `..`) extensively. Examples:
        *   `ops/btypes/action.py` might need `from .generic import Operator`.
        *   `ui/btypes/panel.py` might need `from ...flags import PANEL`.
        *   Files in `[domain]/btypes/` might need `from ...core.btypes import BpyPropertyGroup`.
        *   `data/helpers.py` might need `from .props import ...`.
        *   `ne/annotations_internal.py` might need `from .btypes.node_socket import NodeSocket`.
    *   Update `__init__.py` in each directory (`app`, `core`, `data`, `ne`, `ops`, `ui`, `utils`) and subdirectory (`data/btypes`, `ne/btypes`, `ops/btypes`, `ui/btypes`) to expose necessary elements for internal use and for the facade.
        *   E.g., `ops/btypes/__init__.py` imports `Action`, `Operator`, `Modal`.
        *   E.g., `ops/__init__.py` imports from `.btypes`.
    *   Revise `ackit/__init__.py` (Minimal: `from ._ack import ACK`, `from . import enums`).

4.  **Update Example Usage (`ackit_addon_template`):**
    *   Update external imports in files like `ackit_addon_template/ops.py` to use `from .ackit import ACK`.

5.  **Cleanup:**
    *   Delete `ackit/registry/`, `ackit/types/`, empty `ackit/decorators/`.
    *   Delete any other empty files/dirs.
    *   Review `ackit/globals.py`.

6.  **Testing:**
    *   Linters/type checkers.
    *   Install and test thoroughly in Blender.
