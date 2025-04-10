# Sistema de Polling en ACKit

El sistema de polling en ACKit proporciona una forma elegante y flexible de controlar cuándo están disponibles los operadores, paneles y otros elementos de la interfaz de usuario en Blender.

## Introducción

En Blender, el "polling" se refiere al mecanismo que determina si un elemento de la interfaz de usuario (como un operador o un panel) debe estar disponible o habilitado en un contexto específico. Por ejemplo, un operador que modifica vértices de una malla podría estar disponible solo cuando hay un objeto malla seleccionado y se está en modo edición.

ACKit simplifica la implementación de estas verificaciones de disponibilidad mediante un sistema de decoradores predefinidos y personalizables.

## Estructura del Sistema de Polling

El sistema de polling de ACKit está organizado jerárquicamente bajo la clase `ACK.Poll`:

```
ACK.Poll
├── custom                # Decorador para funciones de polling personalizadas
├── ACTIVE_OBJECT        # Verificaciones relacionadas con el objeto activo
│   ├── ANY              # Requiere cualquier objeto activo
│   ├── MESH             # Requiere objeto malla activo
│   ├── CURVE            # Requiere objeto curva activo
│   ├── ARMATURE         # Requiere objeto armature activo
│   └── ...              # Otros tipos de objetos
├── MODE                 # Verificaciones relacionadas con el modo de edición
│   ├── OBJECT           # Requiere modo objeto
│   ├── EDIT             # Requiere modo edición (cualquier tipo)
│   ├── EDIT_MESH        # Requiere modo edición de malla
│   ├── WEIGHT_PAINT     # Requiere modo weight paint
│   └── ...              # Otros modos
├── SELECTION            # Verificaciones relacionadas con la selección
│   ├── HAS_SELECTED     # Requiere al menos un objeto seleccionado
│   └── MULTIPLE         # Requiere múltiples objetos seleccionados
└── SPACE                # Verificaciones relacionadas con espacios específicos
    ├── VIEW_3D          # Requiere estar en el espacio View3D
    ├── PROPERTIES       # Requiere estar en el espacio Properties
    ├── NODE_EDITOR      # Requiere estar en el espacio Node Editor
    └── ...              # Otros espacios
```

## Uso Básico de los Decoradores de Polling

Los decoradores de polling se aplican a clases de operadores, paneles u otros elementos registrables:

```python
from ...ackit import ACK

# Operador que requiere un objeto malla activo
@ACK.Poll.ACTIVE_OBJECT.MESH
class MeshOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.mesh_operator"
    bl_label = "Operador de Malla"
    
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

## Combinación de Decoradores

Puedes aplicar múltiples decoradores para crear condiciones más específicas:

```python
from ...ackit import ACK

# Operador que requiere un objeto malla activo y modo edición
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.EDIT
class EditMeshOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.edit_mesh_operator"
    bl_label = "Operador de Edición de Malla"
    
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

Los decoradores se aplican en orden, de abajo hacia arriba. En el ejemplo anterior, primero se verifica si estamos en modo edición, y luego si el objeto activo es una malla.

## Decoradores de Polling Personalizados

Puedes crear funciones de polling personalizadas utilizando el decorador `ACK.Poll.custom`:

```python
from ...ackit import ACK

# Función de polling personalizada
def my_custom_poll(cls, context):
    # Verificar si hay al menos un objeto con nombre que comienza con "Prefix_"
    return any(obj.name.startswith("Prefix_") for obj in context.scene.objects)

# Aplicar la función personalizada como decorador
@ACK.Poll.custom(my_custom_poll)
class CustomPollOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.custom_poll_operator"
    bl_label = "Operador con Polling Personalizado"
    
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

## Polling en Paneles y Otros Elementos de UI

Los decoradores de polling también funcionan con paneles y otros elementos de UI:

```python
from ...ackit import ACK

# Panel que se muestra solo cuando hay un objeto armature activo
@ACK.Poll.ACTIVE_OBJECT.ARMATURE
class ArmaturePanel(ACK.Register.Types.UI.Panel):
    bl_idname = "VIEW3D_PT_armature_panel"
    bl_label = "Panel de Armature"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mi Addon"
    
    def draw(self, context):
        layout = self.layout
        # Implementación...
```

## Polling con Paneles a partir de Funciones

También puedes aplicar condiciones de polling a los paneles creados a partir de funciones:

```python
from ...ackit import ACK

# Panel que se muestra solo en modo edición
@ACK.Poll.MODE.EDIT
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def edit_mode_panel(context, layout):
    layout.label(text="Herramientas de Edición")
    # Implementación...
```

## Polling para Propiedades

Puedes controlar la visibilidad y habilitación de propiedades basándote en estados:

```python
from ...ackit import ACK, bpy

class MyPropertyGroup(ACK.Register.Types.Data.PropertyGroup):
    enable_feature = ACK.PropsWrapped.Bool("Habilitar Característica").default(False)
    
    # Esta propiedad solo está visible si enable_feature es True
    feature_strength = ACK.PropsWrapped.Float("Intensidad").default(0.5).min(0).max(1)
    
    # Función para determinar si feature_strength debe estar visible
    @classmethod
    def poll_feature_strength(cls, context):
        return context.scene.my_props.enable_feature
    
    # Registrar el grupo de propiedades
    @classmethod
    def register(cls):
        bpy.types.Scene.my_props = ACK.Register.Property(bpy.props.PointerProperty(type=cls))
        
        # Registrar la función de polling para la propiedad
        ACK.Register.PropertyPolling(cls, "feature_strength", cls.poll_feature_strength)
    
    @classmethod
    def unregister(cls):
        del bpy.types.Scene.my_props
```

## Métodos Auxiliares para Polling

ACKit proporciona varios métodos auxiliares para crear condiciones de polling complejas:

```python
from ...ackit import ACK
from ...ackit.registry.polling import combine_polls, invert_poll

# Combinar múltiples condiciones (AND lógico)
combined_poll = combine_polls(
    ACK.Poll.ACTIVE_OBJECT.MESH.poll_function,
    ACK.Poll.MODE.EDIT.poll_function
)

# Invertir una condición (NOT lógico)
not_in_edit_mode = invert_poll(ACK.Poll.MODE.EDIT.poll_function)

# Aplicar la condición combinada
@ACK.Poll.custom(combined_poll)
class ComplexPollOperator(ACK.Register.Types.Ops.Generic):
    # Implementación...
```

## Operadores con Disponibilidad Dinámica

Para casos más complejos, puedes sobreescribir el método `poll` directamente:

```python
from ...ackit import ACK

class DynamicOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.dynamic_operator"
    bl_label = "Operador Dinámico"
    
    @classmethod
    def poll(cls, context):
        # Verificar si el objeto activo tiene al menos una UV Map
        if context.active_object and context.active_object.type == 'MESH':
            mesh = context.active_object.data
            return len(mesh.uv_layers) > 0
        return False
    
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

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

Puedes extender el sistema de polling con tus propios decoradores:

```python
from ...ackit import ACK
from ...ackit.registry.polling import make_decorator

# Función básica de polling
def poll_has_material(cls, context):
    return (context.active_object and 
            context.active_object.active_material is not None)

# Crear un decorador a partir de la función
HAS_MATERIAL = make_decorator(poll_has_material)

# Usar el decorador personalizado
@HAS_MATERIAL
class MaterialOperator(ACK.Register.Types.Ops.Generic):
    # Implementación...
```

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