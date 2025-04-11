# Clase ACK (API v2)

La clase `ACK` es el punto de entrada principal y unificado para la mayoría de las funcionalidades de `ackit`. Está diseñada siguiendo el patrón de diseño Facade, proporcionando una API jerárquica y organizada para acceder a las capacidades del framework agrupadas por dominio.

## Estructura

La clase `ACK` contiene clases anidadas que representan diferentes dominios de funcionalidad en Blender:

```python
# Importar la fachada
from .ackit import ACK

class ACK:
    # Acceso rápido a propiedades (alias de ACK.Data.Prop y ACK.Data.PropTyped)
    Prop = ...
    PropTyped = ...
    
    # Decoradores/Utilidades de Polling (alias de ackit.utils.polling.Polling)
    Poll = ... 

    class Ops:
        # Tipos base, creadores y configuración para Operadores
        Generic = ...       # ackit.ops.btypes.generic.Generic
        Action = ...        # ackit.ops.btypes.action.Action
        Modal = ...         # ackit.ops.btypes.modal.Modal
        
        create_action_from_func = ... # Action.from_function
        
        add_metadata = ...  # ackit.metadata.Operator
        add_flag = ...      # ackit.flags.OPERATOR
        add_modal_flag = ...# ackit.flags.MODAL
        add_run_condition = ... # Alias de ACK.Poll
        
    class UI:
        # Tipos base, creadores y configuración para Elementos UI
        Panel = ...         # ackit.ui.btypes.panel.Panel
        Menu = ...          # ackit.ui.btypes.menu.Menu
        PieMenu = ...       # ackit.ui.btypes.pie_menu.PieMenu
        Popover = ...       # ackit.ui.btypes.popover.Popover
        UIList = ...        # ackit.ui.btypes.ui_list.UIList
        
        create_panel_from_func = ... # ackit.ui.btypes.panel.PanelFromFunction o Panel.from_function
        create_menu_from_func = ...  # Menu.from_function
        # ... otros creadores ...
        
        add_panel_flag = ... # ackit.flags.PANEL
        add_display_condition = ... # Alias de ACK.Poll

    class NE: # Node Editor
        # Tipos base, creadores y configuración para el Editor de Nodos
        Node = ...          # ackit.ne.btypes.node.Node
        Tree = ...          # ackit.ne.btypes.node_tree.NodeTree
        Socket = ...        # ackit.ne.btypes.node_socket.NodeSocket (base)
        
        add_node_metadata = ...     # ackit.metadata.Node
        add_socket_metadata = ...   # ackit.metadata.NodeSocket
        add_node_to_category = ...  # ackit.flags.NODE_CATEGORY
        
        # Funciones para definir sockets en clases Node
        new_input = ...     # ackit.ne.annotations.NodeInput
        new_output = ...    # ackit.ne.annotations.NodeOutput
        
        # Módulo con tipos de socket específicos (NodeSocketFloat, etc.)
        socket_types = ...  # ackit.ne.socket_types

    class Data:
        # Tipos base, definiciones de propiedades y registro relacionado con datos
        AddonPreferences = ... # ackit.data.btypes.addon_preferences.AddonPreferences
        PropertyGroup = ...    # ackit.data.btypes.property_group.PropertyGroup
        
        # Clases para definir propiedades (con y sin tipo fuerte)
        Prop = ...          # ackit.data.props.PropertyTypes
        PropTyped = ...     # ackit.data.props.WrappedTypedPropertyTypes
        
        # Funciones helper para registro de propiedades
        register_property = ... # ackit.data.helpers.register_property
        batch_register_properties = ... # ackit.data.helpers.batch_register_properties

        # Decoradores para suscripción a cambios RNA (MsgBus)
        subscribe_to_rna = ... # ackit.data.subscriptions.subscribe_to_rna_change
        subscribe_to_rna_context = ... # ackit.data.subscriptions.subscribe_to_rna_change_based_on_context

    class App: 
        # Handlers a nivel de aplicación, Timers, etc.
        Handler = ...       # ackit.app.handlers.Handlers (Enum)
        Timer = ...         # ackit.app.timers.new_timer_as_decorator
        # Keymap = ...      # ackit.app.keymaps.RegisterKeymap (si se necesita acceso directo)
```

## Uso Principal

En lugar de importar desde subdirectorios profundos de `ackit`, la mayoría de las interacciones se realizan a través de la fachada `ACK`.

### Definición de un Operador

```python
from ..ackit import ACK
# Opcional: importar Enums directamente si se usan mucho
from ..ackit.enums.operator import OpsReturn 

@ACK.Ops.add_flag.REGISTER_UNDO
@ACK.Poll.ACTIVE_OBJECT.MESH 
class MyOperator(ACK.Ops.Action):
    bl_label = "Mi Operador de Acción"
    
    # Definir propiedades usando ACK.PropTyped
    my_value: ACK.PropTyped.Float("Valor", default=0.5).min(0.0).max(1.0)
    
    # Opcional: definir UI si es necesario
    def draw_ui(self, context, layout):
        layout.prop(self, "my_value")

    # Lógica principal
    def action(self, context):
        print("Ejecutando Mi Operador con valor:", self.my_value)
        obj = context.active_object
        if obj:
            obj.location.z += self.my_value
        # Usar OpsReturn directamente del enum importado
        return OpsReturn.FINISH 
```

### Definición de un Panel

```python
from ..ackit import ACK

# Usar decoradores de ACK.UI para crear paneles desde funciones
@ACK.UI.create_panel_from_func.VIEW_3D(tab="Mi Pestaña")
# Opcional: añadir flags del panel
@ACK.UI.add_panel_flag.DEFAULT_CLOSED 
def my_ui_panel(context, layout):
    layout.label(text="Contenido de mi panel")
    # Añadir un operador usando su bl_idname
    layout.operator("mi_addon.mi_operador_de_accion") 
```

### Definición de un Nodo

```python
from ..ackit import ACK

# Decoradores para metadatos y categoría
@ACK.NE.add_node_to_category("MiGrupo/SubGrupo")
@ACK.NE.add_node_metadata(label="Mi Nodo Sumador", icon='ADD')
class MyAddNode(ACK.NE.Node):
    
    # Definir sockets usando ACK.NE.new_input/new_output
    # y tipos de socket desde ACK.NE.socket_types
    input_a = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    input_b = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)
    
    # Lógica de evaluación
    def evaluate(self):
        # Acceder a valores de sockets directamente por su nombre de atributo
        sum_value = self.input_a.value + self.input_b.value 
        # Asignar valor al socket de salida
        self.result.value = sum_value 
```

### Definición de un PropertyGroup

```python
from ..ackit import ACK

class MyPropertyGroup(ACK.Data.PropertyGroup):
    # Usar ACK.PropTyped para propiedades con tipo fuerte
    my_int_prop: ACK.PropTyped.Int("Mi Entero", default=5).min(0).max(10)
    my_bool_prop: ACK.PropTyped.Bool("Mi Booleano", default=True)
    
    # Usar ACK.Prop para propiedades básicas (menos común)
    my_string_prop: ACK.Prop.STRING(name="Mi String Básico") 
```

### Suscripción a Cambios RNA

```python
from ..ackit import ACK
import bpy

# Suscribirse a cambios en una propiedad de la escena
@ACK.Data.subscribe_to_rna(bpy.types.Scene, "frame_current")
def on_frame_change(context, scene_data, frame_value):
    print(f"Frame cambiado a: {frame_value}")

# Suscribirse a cambios basados en un data_path del contexto
@ACK.Data.subscribe_to_rna_context("active_object.location", "x")
def on_active_object_location_x_change(context, object_data, location_x_value):
    if object_data:
        print(f"Posición X del objeto activo cambiada a: {location_x_value}")
```

### Uso de Handlers de Aplicación

```python
from ..ackit import ACK

# Registrar una función para que se ejecute después de cargar un archivo .blend
@ACK.App.Handler.LOAD_POST()
def my_load_post_handler(context):
    print("Archivo .blend cargado!")

# Registrar una función como temporizador que se ejecuta una vez después de 0.5 segundos
@ACK.App.Timer(first_interval=0.5, one_time_only=True)
def my_timer_callback():
    print("Temporizador ejecutado!")
```

## Consideraciones

*   La fachada `ACK` simplifica los imports y proporciona una estructura lógica.
*   Los módulos internos (`ackit/ops`, `ackit/ui`, etc.) contienen la implementación detallada.
*   La documentación específica de cada clase base (Operator, Panel, Node, etc.) y helper se encuentra en sus respectivos módulos o en secciones dedicadas de la API.
*   Los valores de retorno de operadores (`{'FINISHED'}`, etc.) ahora se deben usar directamente o importar desde `ackit.enums.operator.OpsReturn`.

## Patrones de Diseño Implementados

La clase `ACK` implementa varios patrones de diseño:

1. **Facade**: Proporciona una interfaz unificada y simplificada
2. **Factory**: Métodos para crear instancias de clases tipadas
3. **Builder/Fluent Interface**: API fluida para definir propiedades
4. **Decorator**: Modificadores de comportamiento a través de decoradores

## Consideraciones para el Rendimiento

Aunque la clase `ACK` añade una capa de abstracción, está diseñada para tener un impacto mínimo en el rendimiento:

- Las implementaciones subyacentes son delgadas y eficientes
- El sistema de registro ordena las clases una sola vez al inicio
- Las abstracciones proporcionan guía de tipos sin coste en tiempo de ejecución

## Extensibilidad

Puedes extender la funcionalidad de `ACK` de varias maneras:

1. Crear subclases especializadas de los tipos base
2. Implementar decoradores personalizados
3. Añadir métodos utilitarios a tus propias clases 