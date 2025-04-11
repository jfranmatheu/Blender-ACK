# Sistema de Polling en ACKit

El sistema de polling en ACKit proporciona una forma elegante y flexible de controlar cuándo están disponibles los operadores, paneles y otros elementos de la interfaz de usuario en Blender.

## Introducción

En Blender, el "polling" se refiere al mecanismo que determina si un elemento de la interfaz de usuario (como un operador o un panel) debe estar disponible o habilitado en un contexto específico. Por ejemplo, un operador que modifica vértices de una malla podría estar disponible solo cuando hay un objeto malla seleccionado y se está en modo edición.

ACKit simplifica la implementación de estas verificaciones de disponibilidad mediante un sistema de decoradores predefinidos y personalizables accesibles principalmente a través de `ACK.Poll`.

## Estructura del Sistema de Polling

El sistema de polling de ACKit está organizado jerárquicamente bajo la clase `ACK.Poll` (un alias de `ackit.utils.polling.Polling`):

```python
# Importar la fachada
from .ackit import ACK

ACK.Poll
├── custom               # Decorador para funciones de polling personalizadas
├── make_poll_decorator  # Decorador para crear decoradores para polling personalizados (uso avanzado)
├── ACTIVE_OBJECT        # Verificaciones relacionadas con el objeto activo
│   ├── ANY              # Requiere cualquier objeto activo
│   ├── MESH             # Requiere objeto malla activo
│   ├── CURVE            # Requiere objeto curva activo
│   ├── ARMATURE         # Requiere objeto armature activo
│   └── ...              # Otros tipos de objetos (ver autocompletado o código fuente)
├── MODE                 # Verificaciones relacionadas con el modo de edición
│   ├── OBJECT           # Requiere modo objeto
│   ├── EDIT_MESH        # Requiere modo edición de malla
│   ├── POSE             # Requiere modo pose
│   ├── WEIGHT_PAINT     # Requiere modo weight paint
│   └── ...              # Otros modos (ver autocompletado o código fuente)
├── ACTIVE_BRUSH         # Verifica si hay un pincel activo en el modo actual (si aplica)
# ... Otros polling helpers pueden existir o añadirse en ackit.utils.polling ...
```

## Uso Básico de los Decoradores de Polling

Los decoradores de polling se aplican directamente a las clases que heredan de los tipos base de `ackit` (como `ACK.Ops.Generic`, `ACK.UI.Panel`, etc.):

```python
from ..ackit import ACK
from ..ackit.enums.operator import OpsReturn

# Operador que requiere un objeto malla activo
@ACK.Poll.ACTIVE_OBJECT.MESH
class MeshOperator(ACK.Ops.Generic):
    bl_idname = "object.mesh_operator"
    bl_label = "Operador de Malla"
    
    def execute(self, context):
        # Implementación...
        return OpsReturn.FINISH
```

## Combinación de Decoradores

Puedes aplicar múltiples decoradores para crear condiciones más específicas (se evalúan de abajo hacia arriba):

```python
from ..ackit import ACK
from ..ackit.enums.operator import OpsReturn

# Operador que requiere un objeto malla activo y modo edición de malla
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.EDIT_MESH
class EditMeshOperator(ACK.Ops.Generic):
    bl_idname = "object.edit_mesh_operator"
    bl_label = "Operador de Edición de Malla"
    
    def execute(self, context):
        # Implementación...
        return OpsReturn.FINISH
```

## Decoradores de Polling Personalizados

Puedes crear funciones de polling personalizadas utilizando el decorador `ACK.Poll.custom`:

```python
from ..ackit import ACK
from ..ackit.enums.operator import OpsReturn

# Función de polling personalizada (nota: recibe el contexto como argumento)
def my_custom_poll(context):
    # Verificar si hay al menos un objeto con nombre que comienza con "Prefix_"
    return any(obj.name.startswith("Prefix_") for obj in context.scene.objects)

# Aplicar la función personalizada como decorador
@ACK.Poll.custom(my_custom_poll)
class CustomPollOperator(ACK.Ops.Generic):
    bl_idname = "object.custom_poll_operator"
    bl_label = "Operador con Polling Personalizado"
    
    def execute(self, context):
        # Implementación...
        return OpsReturn.FINISH
```

## Polling en Paneles y Otros Elementos de UI

Los decoradores de polling funcionan igual con paneles (tanto definidos como clases que heredan de `ACK.UI.Panel`, como los creados desde funciones con `ACK.UI.create_panel_from_func`):

```python
from ..ackit import ACK

# Panel (clase) que se muestra solo cuando hay un objeto armature activo
@ACK.Poll.ACTIVE_OBJECT.ARMATURE
class ArmaturePanel(ACK.UI.Panel):
    bl_idname = "VIEW3D_PT_armature_panel"
    bl_label = "Panel de Armature"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mi Addon"
    
    def draw_ui(self, context, layout):
        layout.label(text="Controles de Armature")
        # Implementación...

# Panel (función) que se muestra solo en modo edición
@ACK.Poll.MODE.EDIT_MESH # Ser específico con el modo si es necesario
@ACK.UI.create_panel_from_func.VIEW_3D(tab="Mi Addon")
def edit_mode_panel(context, layout):
    layout.label(text="Herramientas de Edición")
    # Implementación...
```

## Polling para Propiedades

El control de visibilidad/habilitación de propiedades individuales **no** se gestiona directamente con `ACK.Poll`. Se debe implementar lógica en el método `draw` o `draw_ui` de la clase contenedora (Panel, Operator, PropertyGroup, etc.) para mostrar u ocultar propiedades condicionalmente usando `layout.prop` o `layout.active`:

```python
from ..ackit import ACK
import bpy

class MySettings(ACK.Data.PropertyGroup):
    enable_advanced: ACK.PropTyped.Bool("Opciones Avanzadas", default=False)
    strength: ACK.PropTyped.Float("Intensidad", default=0.5)
    detail: ACK.PropTyped.Int("Detalle", default=2)

@ACK.UI.create_panel_from_func.PROPERTIES(context='scene', tab="Mi Addon")
def settings_panel(context, layout):
    settings = context.scene.my_addon_settings # Asumiendo que registras MySettings en la escena
    
    layout.prop(settings, "enable_advanced")
    
    # Mostrar propiedades avanzadas solo si enable_advanced es True
    if settings.enable_advanced:
        box = layout.box()
        box.label(text="Avanzado:")
        box.prop(settings, "strength")
        box.prop(settings, "detail")
    # También puedes deshabilitar una propiedad:
    row = layout.row()
    row.active = settings.enable_advanced # Habilitar/deshabilitar fila basado en el bool
    row.prop(settings, "strength", text="Intensidad (si habilitado)")
```
*(Nota: El ejemplo anterior de `PropertyPolling` en la v1 ya no es aplicable en la estructura refactorizada.)*

## Operadores con Disponibilidad Dinámica

Para lógica de polling muy compleja que no se cubre con los decoradores, puedes sobreescribir el método de clase `poll` directamente en tu operador o panel:

```python
from ..ackit import ACK
from ..ackit.enums.operator import OpsReturn
import bpy

class DynamicOperator(ACK.Ops.Generic):
    bl_idname = "object.dynamic_operator"
    bl_label = "Operador Dinámico"
    
    @classmethod
    def poll(cls, context):
        # Lógica de polling personalizada más compleja
        if not context.active_object:
            cls.poll_message_set("Se requiere un objeto activo.")
            return False
        if context.active_object.type != 'MESH':
             cls.poll_message_set("El objeto activo debe ser una Malla.")
             return False
        if len(context.active_object.data.uv_layers) == 0:
             cls.poll_message_set("La malla activa no tiene UV Maps.")
             return False
        return True
    
    def execute(self, context):
        # Implementación...
        self.report({'INFO'}, "Operador dinámico ejecutado!")
        return OpsReturn.FINISH
```

Recuerda usar `cls.poll_message_set("Mensaje")` dentro del método `poll` para proporcionar feedback al usuario sobre por qué un operador no está disponible.

## Decoradores de Polling Específicos para Áreas

Para controlar la disponibilidad en áreas específicas:

```python
from ...ackit import ACK

# Operador disponible solo en el editor de imágenes y cuando hay una imagen
@ACK.Poll.SPACE.IMAGE_EDITOR
@ACK.Poll.custom(lambda cls, context: context.edit_image is not None)
class ImageOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "image.my_operator"
    bl_label = "Mi Operador de Imágenes"
    
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

## Mensajes de Error en Polling

Puedes proporcionar mensajes de error útiles cuando un operador no está disponible:

```python
from ...ackit import ACK

def custom_poll_with_message(cls, context):
    if context.active_object is None:
        cls.poll_message_set("No hay objeto activo")
        return False
    if context.active_object.type != 'MESH':
        cls.poll_message_set("El objeto activo debe ser una malla")
        return False
    return True

@ACK.Poll.custom(custom_poll_with_message)
class MessageOperator(ACK.Register.Types.Ops.Generic):
    # Implementación...
```

## Creación de Nuevos Decoradores de Polling

Puedes extender el sistema de polling con tus propios decoradores utilizando `Polling.make_poll_decorator`:

```python
from ...ackit import ACK, Polling

# Función básica de polling
def has_material(context):
    """Verifica si el objeto activo tiene un material activo."""
    return (context.active_object and 
            context.active_object.active_material is not None)

# Crear un decorador a partir de la función
HAS_MATERIAL = Polling.make_poll_decorator(has_material)

# Usar el decorador personalizado
@HAS_MATERIAL
class MaterialOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.material_operator"
    bl_label = "Operador de Material"
    
    def execute(self, context):
        # Implementación...
        return {'FINISHED'}
```

Este enfoque te permite crear decoradores reutilizables que puedes aplicar en múltiples clases y compartir entre diferentes módulos.

## Polling Personalizado con el Decorador Custom

Para casos de uso único donde no necesitas crear un decorador reutilizable, puedes usar el método `Polling.custom`:

```python
from ...ackit import ACK, Polling

# Aplicar una función de polling personalizada directamente
@Polling.custom(lambda context: context.active_object and len(context.active_object.material_slots) > 2)
class MultiMaterialOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.multi_material_operator"
    bl_label = "Operador Multi-Material"
    
    def execute(self, context):
        # Este operador solo está disponible cuando el objeto activo tiene más de 2 slots de material
        self.report({'INFO'}, f"Procesando {len(context.active_object.material_slots)} materiales")
        return {'FINISHED'}
```

Esta es una forma sencilla de aplicar condiciones de polling personalizadas sin tener que definir una función separada.

## Mejores Prácticas para Polling

1. **Usa decoradores predefinidos** cuando sea posible para mantener el código limpio y consistente.
2. **Combina decoradores** para condiciones complejas en lugar de escribir funciones de polling largas.
3. **Proporciona mensajes de error útiles** para ayudar a los usuarios a entender por qué un operador no está disponible.
4. **Mantén las funciones de polling eficientes** ya que se llaman con frecuencia durante la interacción del usuario.
5. **Agrupa operadores con condiciones de polling similares** para mantener una estructura de código coherente.

## Referencias

- [API de Decoradores de Polling](../api/polling_decorators.md)
- [Tutorial: Operadores Contextuales](../tutorials/contextual_operators.md)
- [Referencia: Contexto de Blender](../reference/blender_context.md) 