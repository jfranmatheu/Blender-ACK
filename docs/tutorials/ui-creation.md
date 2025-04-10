# Creación de Interfaces de Usuario con ACKit

Este tutorial te guiará en la creación de interfaces de usuario para addons de Blender utilizando ACKit.

## Introducción

ACKit proporciona varias herramientas y abstracciones para simplificar la creación de interfaces de usuario en Blender, incluyendo paneles, menús y popups.

## Paneles

Los paneles son contenedores de UI que se muestran en diferentes áreas de la interfaz de Blender.

### Paneles Simples con Funciones

La forma más sencilla de crear un panel es utilizando el decorador `ACK.Register.FromFunction.PANEL`:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def simple_panel(context, layout):
    layout.label(text="Este es mi panel")
    layout.operator("object.select_all").action = 'SELECT'
    layout.operator("object.select_all").action = 'DESELECT'
```

Este decorador soporta varios parámetros:

- `tab`: La pestaña donde aparecerá el panel (en la barra lateral)
- `region`: La región donde se mostrará el panel ('UI', 'TOOLS', 'HEADER', etc.)
- `order`: El orden de aparición del panel
- `flags`: Flags de comportamiento del panel (como `ACK.Flags.PANEL.DEFAULT_CLOSED`)

### Paneles en Diferentes Áreas

ACKit proporciona varios decoradores para diferentes áreas de Blender:

```python
# Panel en la vista 3D
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Pestaña")
def panel_3d(context, layout):
    # Contenido del panel...

# Panel en el editor de propiedades
@ACK.Register.FromFunction.PANEL.PROPERTIES()
def panel_properties(context, layout):
    # Contenido del panel...

# Panel en el editor de shader nodes
@ACK.Register.FromFunction.PANEL.NODE_EDITOR()
def panel_nodes(context, layout):
    # Contenido del panel...

# Panel en el editor de imágenes
@ACK.Register.FromFunction.PANEL.IMAGE_EDITOR()
def panel_image(context, layout):
    # Contenido del panel...
```

### Paneles como Clases

También puedes crear paneles como clases para casos más complejos:

```python
from ...ackit import ACK

class MyPanel(ACK.Register.Types.UI.Panel):
    bl_label = "Mi Panel"
    bl_idname = "VIEW3D_PT_my_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mi Addon"
    
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Operaciones:")
        row = layout.row()
        row.operator("object.select_all", text="Seleccionar").action = 'SELECT'
        row.operator("object.select_all", text="Deseleccionar").action = 'DESELECT'
        
        # Acceso a propiedades del objeto
        if context.object:
            layout.prop(context.object, "name")
```

### Organización del Layout

ACKit facilita la organización de tu interfaz con helpers para el layout:

```python
def draw(self, context):
    layout = self.layout
    
    # Columnas
    col = layout.column()
    col.label(text="Columna 1")
    
    # Filas
    row = layout.row()
    row.label(text="Izquierda")
    row.label(text="Derecha")
    
    # Cajas
    box = layout.box()
    box.label(text="Contenido en caja")
    
    # Columnas alineadas
    col = layout.column(align=True)
    col.prop(context.object, "location", index=0)
    col.prop(context.object, "location", index=1)
    col.prop(context.object, "location", index=2)
    
    # Split (división)
    split = layout.split(factor=0.3)
    col1 = split.column()
    col1.label(text="Etiquetas:")
    col2 = split.column()
    col2.label(text="Valores")
```

## Menús

Los menús son interfaces desplegables que pueden aparecer en diferentes partes de Blender.

### Menús Simples con Funciones

Puedes crear menús utilizando el decorador `ACK.Register.FromFunction.MENU`:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.MENU()
def simple_menu(context, layout):
    layout.operator("object.select_all", text="Seleccionar Todo").action = 'SELECT'
    layout.operator("object.select_all", text="Deseleccionar Todo").action = 'DESELECT'
    layout.separator()
    layout.operator("object.delete", text="Eliminar Selección")
```

### Menús como Clases

Para menús más complejos, puedes usar clases:

```python
from ...ackit import ACK

class MyMenu(ACK.Register.Types.UI.Menu):
    bl_label = "Mi Menú"
    bl_idname = "VIEW3D_MT_my_menu"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("object.select_all", text="Seleccionar Todo").action = 'SELECT'
        layout.operator("object.select_all", text="Deseleccionar Todo").action = 'DESELECT'
        
        layout.separator()
        
        layout.operator("object.delete", text="Eliminar Selección")
        
        # Submenú
        layout.menu("VIEW3D_MT_object")
```

### Menús de Pie (Pie Menus)

Los menús de pie son menús circulares que aparecen alrededor del cursor:

```python
from ...ackit import ACK

class MyPieMenu(ACK.Register.Types.UI.PieMenu):
    bl_label = "Mi Menú Pie"
    bl_idname = "VIEW3D_MT_pie_my_menu"
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        # Opciones en 8 direcciones (N, NE, E, SE, S, SW, W, NW)
        pie.operator("transform.translate")
        pie.operator("transform.rotate")
        pie.operator("transform.resize")
        pie.operator("object.delete")
        pie.operator("object.duplicate_move")
        pie.operator("object.join")
        pie.operator("object.parent_set")
        pie.operator("object.parent_clear")
```

## Popovers

Los popovers son paneles desplegables que aparecen al hacer clic en un botón:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.POPOVER()
def my_popover(context, layout):
    layout.label(text="Configuración:")
    layout.prop(context.scene, "frame_start")
    layout.prop(context.scene, "frame_end")
    layout.prop(context.scene, "frame_step")

# Uso del popover en otro panel
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def main_panel(context, layout):
    layout.label(text="Herramientas:")
    
    # Añadir botón para mostrar el popover
    my_popover.draw_in_layout(layout, text="Configuración")
```

## UI Lists

Las UI Lists son listas personalizadas con elementos que pueden ser seleccionados:

```python
from ...ackit import ACK

class MY_UL_list(ACK.Register.Types.UI.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # Dibujar un elemento de la lista
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='OBJECT_DATA')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='OBJECT_DATA')

# Uso de la lista en un panel
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def list_panel(context, layout):
    row = layout.row()
    
    # Columna para la lista
    col = row.column()
    col.template_list("MY_UL_list", "", context.scene, "my_list", 
                     context.scene, "my_list_index", rows=3)
    
    # Columna para los botones
    col = row.column(align=True)
    col.operator("my_list.new_item", icon='ADD', text="")
    col.operator("my_list.delete_item", icon='REMOVE', text="")
```

## Propiedades en la UI

Para mostrar propiedades en la UI, puedes usar diferentes métodos:

```python
def draw(self, context):
    layout = self.layout
    obj = context.object
    
    # Propiedad básica
    layout.prop(obj, "name")
    
    # Propiedades con etiqueta personalizada
    layout.prop(obj, "location", text="Posición")
    
    # Propiedades en una fila
    row = layout.row()
    row.prop(obj, "scale", text="Escala")
    
    # Propiedades sin etiqueta
    layout.prop(obj, "rotation_euler", text="")
    
    # Propiedad específica (por índice)
    layout.prop(obj, "location", index=2, text="Posición Z")
    
    # Propiedades de array completo (expand=True)
    layout.prop(obj, "scale", expand=True)
    
    # Propiedad de búsqueda (para enums largos)
    layout.prop_search(obj, "material_slots", bpy.data, "materials")
```

## Operadores en la UI

Los operadores pueden mostrarse como botones:

```python
def draw(self, context):
    layout = self.layout
    
    # Operador básico
    layout.operator("object.select_all")
    
    # Operador con etiqueta personalizada
    layout.operator("object.select_all", text="Seleccionar Todo")
    
    # Operador con icono
    layout.operator("object.delete", text="Eliminar", icon='TRASH')
    
    # Operador con propiedad
    op = layout.operator("object.select_all")
    op.action = 'SELECT'
    
    # Operadores en una fila
    row = layout.row()
    row.operator("ed.undo")
    row.operator("ed.redo")
```

## Iconos

ACKit facilita el uso de iconos en la UI:

```python
def draw(self, context):
    layout = self.layout
    
    # Iconos estándar de Blender
    layout.label(text="Icono Estándar:", icon='WORLD')
    
    # Iconos personalizados
    custom_icon = context.scene.my_icons["mi_icono"]
    layout.label(text="Icono Personalizado:", icon_value=custom_icon)
```

Si utilizas `AutoCode.ICONS`, ACKit generará constantes para todos los iconos:

```python
from ...ackit import ACK
from ...auto_code.icons import Icons

def draw(self, context):
    layout = self.layout
    
    # Uso de constantes de iconos
    layout.label(text="Mundo", icon=Icons.WORLD)
```

## Contexto Dinámico

Puedes adaptar tu UI según el contexto:

```python
def draw(self, context):
    layout = self.layout
    
    # Verificar tipo de objeto
    if context.object is None:
        layout.label(text="No hay objeto seleccionado")
        return
    
    if context.object.type == 'MESH':
        layout.label(text="Objeto Mesh")
        layout.operator("object.shade_smooth")
    elif context.object.type == 'CURVE':
        layout.label(text="Objeto Curva")
        layout.prop(context.object.data, "resolution_u")
```

## Decoradores de UI

ACKit proporciona decoradores para extender paneles existentes:

```python
from ...ackit import ACK

# Añadir a un panel existente
@ACK.RegDeco.UI.APPEND('OBJECT_PT_transform')
def append_to_transform_panel(self, context):
    layout = self.layout
    layout.separator()
    layout.label(text="Mi Extensión:")
    layout.operator("my_addon.my_operator")
```

## Conclusión

ACKit proporciona una variedad de herramientas para simplificar la creación de interfaces de usuario en Blender. Desde el enfoque basado en funciones para casos simples hasta clases completas para casos más complejos, ACKit te permite crear UI consistentes y bien estructuradas con menos código.

## Recursos Adicionales

- [API de Referencia para UI](../api/ui.md)
- [Ejemplos de UI](../examples/ui_examples.md)
- [Buenas Prácticas de UI](../reference/ui_best_practices.md) 