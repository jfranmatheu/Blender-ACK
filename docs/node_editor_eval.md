# ACK Node Editor System Analysis

This document provides a detailed analysis of the structure, execution flow, and data handling within the ACK node editor framework, based on the core files:
- `ackit/ne/btypes/node_tree.py`
- `ackit/ne/btypes/base_tree.py`
- `ackit/ne/btypes/node.py`
- `ackit/ne/btypes/base_node.py`
- `ackit/ne/btypes/node_socket.py`

## 1. Node Tree Type

-   **Graph Structure:** The system implements a **Directed Acyclic Graph (DAG)**. This is standard for node editors and implies a one-way flow of data/execution without cycles (though cycle detection isn't explicitly shown in the base code).
-   **Execution Model:** It operates primarily as a **data-flow** or **demand-driven** system. Changes initiated at certain nodes propagate forward ("downstream") to dependent nodes.

## 2. Execution Triggering Mechanisms

Evaluation of the node graph can be triggered by several events:

-   **Tree Structure Changes (`NodeTree.update()`):** This is the most comprehensive trigger. It is likely invoked by Blender's internal mechanisms whenever the node tree's structure is modified (e.g., adding/removing nodes, connecting/disconnecting links). This method initiates a full re-evaluation starting from the identified input nodes.
-   **Node Property Updates (`Node.on_property_update()`):** When a user modifies a property defined on a node instance (using `WrappedPropertyDescriptor`), this method is called. It directly calls the node's `process()` method, initiating a potentially partial re-evaluation starting from that node.
-   **Socket Property Updates (`NodeSocket.on_property_update()`):** If an *unlinked* input socket's default value is changed, or potentially an output socket's value (though less common for triggering), this method is called. It calls `self.node.process()`, triggering evaluation starting from the socket's node. A `block_property_update` flag is used internally to prevent recursive updates during value setting.

## 3. Execution Flow and Direction

-   **Direction:** Execution flows **forwards** through the graph, following the direction of the links from output sockets to input sockets.
-   **Starting Points:** The `NodeTree.update()` method explicitly finds nodes that have no *incoming* links to any of their input sockets. These "source" or "input" nodes serve as the starting points for a full graph evaluation.
-   **Node Processing (`Node.process()`):** This is the core method driving execution at the node level.
    1.  **`self.evaluate()`:** It first calls the node's own `evaluate()` method. Subclasses of `Node` *must* override this method to implement their specific computation logic (reading input socket values, performing calculations, and setting output socket values).
    2.  **`self.get_dependent_nodes()`:** It identifies all nodes directly connected to its output sockets.
    3.  **Propagation:** It iterates through these dependent nodes and recursively calls *their* `process()` methods. This ensures the execution wave travels downstream through the graph.
-   **Cycle Handling:** The provided base code does not contain explicit cycle detection or prevention mechanisms within the `process` loop or `verify_link`. If a user managed to create a cycle (e.g., Node A Output -> Node B Input -> Node B Output -> Node A Input), the recursive `process()` calls could lead to infinite recursion and a crash. Robust node systems typically prevent link creations that would form cycles.

## 4. Branching and Merging

-   **Branching:** A single output socket can be connected to multiple input sockets on different downstream nodes. When the source node processes, it triggers `process()` on *all* its immediate dependents, effectively branching the execution path.
-   **Merging:** A node with multiple input sockets inherently acts as a merge point for different data flows. Its `evaluate()` method is responsible for reading the values from all required input sockets (`input_socket.value`) and using them collectively in its computation.

## 5. Data Handling and Sockets

-   **`NodeSocket`:** Sockets are the fundamental interface points for data transfer between nodes.
    -   **Typing:** They are strongly typed using Python's `typing.Generic[T]`, allowing for type hints and potentially runtime type checks (e.g., `NodeSocket[int]`, `NodeSocket[str]`). The `value_type` property attempts to retrieve this generic type `T`.
    -   **Value Access (`get_value`, `set_value`, `.value` property):**
        -   **Input Sockets (Linked):** Retrieve the value by calling `get_value()` on the connected `from_socket`.
        -   **Input Sockets (Unlinked):** Retrieve the locally stored default value. This value can be stored either as a standard Blender property (`getattr(self, self.property_name)`) or as a custom property (`self[self.property_name]`) depending on the `use_custom_property` flag.
        -   **Output Sockets:** Return the value computed and set by the node's `evaluate()` method.
    -   **Type Casting:** The system supports automatic type casting during value retrieval across links:
        -   If the `from_socket` and `to_socket` are the exact same class, the value is passed directly.
        -   If types differ, it checks class variables `cast_from_socket` (mapping source socket class name to a casting function) and `cast_from_types` (mapping source data type to a casting function). If a valid cast function is found, it's applied to the value before returning. This allows for flexible connections, like connecting an `int` output to a `float` input.
    -   **Custom Properties:** Sockets can optionally manage their data using Blender's custom properties (`use_custom_property=True`). This allows storing more complex Python types (like `dict`, potentially `list`) that aren't directly supported by standard socket properties. Helper functions (`_get_default_value`) are used to initialize these.
    -   **UID:** Each socket instance gets a unique identifier (`uid`), likely used for robust link serialization or management.

## 6. Core Classes and Responsibilities

-   **`BaseNodeTree` / `NodeTree`:**
    -   Manages the collections of `nodes` and `links`.
    -   Handles high-level graph operations: initiating evaluation (`update`), managing link validity (`verify_link`, `tag_remove_link`, `clear_tagged_links`), serialization (`serialize`), and polling for UI context.
    -   The `update` method is the orchestrator for the primary evaluation flow.
-   **`BaseNode` / `Node`:**
    -   Represents a single computational unit in the graph.
    -   Defines core node behaviors: self-evaluation (`evaluate`), triggering downstream updates (`process`), socket initialization (`setup_sockets`), property handling and drawing (`draw_buttons*`, `on_property_update`), link validation contribution (`insert_link`), dependency finding (`get_dependent_nodes`), and serialization (`serialize`, `_get_serializable_properties`).
    -   Requires subclasses to implement `evaluate()` and define sockets/properties.
-   **`NodeSocket`:**
    -   Defines the input/output interface for a node.
    -   Manages data type (`Generic[T]`), value storage and retrieval (`value`, `get_value`, `set_value`), link state (`is_linked`), type compatibility and casting (`can_cast_*`, `cast_*`), UI drawing (`draw`, `draw_color`), and default value handling (`init`, `on_property_update`).

## 7. Customization and Extension

The framework is designed for extensibility:

-   **New Node Types:** Create subclasses of `Node`. Implement the `evaluate()` method for the node's logic. Define input and output sockets using `NodeSocketWrapper` (details likely in `annotations_internal.py`) and properties using `WrappedPropertyDescriptor`. Assign a `_node_category` for organization.
-   **New Socket Types:** Create subclasses of `NodeSocket`, usually specifying the data type via `Generic` (e.g., `class IntSocket(NodeSocket[int]): ...`). Define the `color`, default `property_name`, potentially `use_custom_property`, and add specific `cast_from_*` rules if needed.

## 8. Serialization (`BaseNodeTree.serialize`, `BaseNode.serialize`)

-   The system includes methods to serialize the node graph structure.
-   `BaseNodeTree.serialize`: Iterates through nodes and links. Calls `node.serialize()` for each node. For links, it records the `name` attribute of the connected nodes and the `identifier` attribute of the sockets involved.
-   `BaseNode.serialize`: Records the node's `name` (used as ID), `bl_idname` (type), `location`, and calls `_get_serializable_properties`.
-   `BaseNode._get_serializable_properties`: Iterates through `WrappedPropertyDescriptor` instances defined on the class, gets their current values from the node instance, handles specific Blender types (like `mathutils.Vector`, `mathutils.Matrix`) by converting them to serializable tuples, and returns a dictionary of property names and values.

## Summary

The ACK node editor provides a robust and extensible foundation for creating custom node-based interfaces and logic within Blender. It employs a standard forward-propagating DAG execution model triggered by graph or property changes. Data flow is managed through strongly-typed sockets with built-in support for type casting. Customization is achieved primarily through subclassing `Node` and `NodeSocket`. 