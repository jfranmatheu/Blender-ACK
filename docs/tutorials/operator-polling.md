# Operadores con Restricciones de Polling

Este tutorial explica cómo restringir la disponibilidad de operadores usando las capacidades de polling de ACKit.

## Introducción al Polling

El polling permite controlar cuándo un operador está disponible para el usuario. ACKit proporciona decoradores que facilitan la definición de condiciones de polling sin necesidad de sobrescribir el método `poll()` directamente.

## Ejemplo 1: Usando Decoradores de Polling Predefinidos

ACKit incluye varios decoradores de polling predefinidos que cubren los casos de uso más comunes:

```python
from your_addon.ackit import ACK, Polling
from your_addon.ackit.registry import Register

# Este operador solo estará disponible cuando:
# 1. El objeto activo sea una malla (mesh)
# 2. Blender esté en modo objeto
@Polling.ACTIVE_OBJECT.MESH   # Requiere un objeto malla activo
@Polling.MODE.OBJECT          # Requiere estar en modo objeto
@Register.OPS.GENERIC         # Registra como operador genérico
class MeshObjectOperator(ACK.Register.Types.Ops.Generic):
    """Operador que solo funciona con objetos malla en modo objeto."""
    
    bl_idname = "object.my_mesh_operator"
    bl_label = "Operación de Malla"
    bl_description = "Realiza una operación específica en objetos malla"
    
    def execute(self, context):
        # Implementación del operador
        # El polling garantiza que context.active_object es una malla
        # y estamos en modo objeto
        self.report({'INFO'}, f"Procesando malla: {context.active_object.name}")
        return {'FINISHED'}
```

## Ejemplo 2: Polling Personalizado con el Decorador Custom

Para casos que no están cubiertos por los decoradores predefinidos, puedes usar `Polling.custom()` para definir condiciones personalizadas:

```python
from your_addon.ackit import ACK, Polling
from your_addon.ackit.registry import Register

# Este operador solo estará disponible cuando:
# 1. Exista un objeto activo
# 2. El objeto tenga al menos 2 ranuras de materiales
# 3. El primer material no sea None
@Polling.custom(lambda context: (
    context.active_object is not None and 
    len(context.active_object.material_slots) >= 2 and
    context.active_object.material_slots[0].material is not None
))
@Register.OPS.GENERIC
class MultiMaterialOperator(ACK.Register.Types.Ops.Generic):
    """Operador que trabaja con objetos que tienen múltiples materiales."""
    
    bl_idname = "material.process_multi_material"
    bl_label = "Procesar Materiales Múltiples"
    bl_description = "Realiza operaciones en objetos con múltiples materiales"
    
    def execute(self, context):
        obj = context.active_object
        material_count = len(obj.material_slots)
        self.report({'INFO'}, f"Procesando {material_count} materiales en {obj.name}")
        
        # Implementación del operador para trabajar con múltiples materiales
        return {'FINISHED'}
```

## Ejemplo 3: Creando Decoradores de Polling Reutilizables

Cuando necesites la misma condición de polling en varios operadores, puedes crear un decorador personalizado con `Polling.make_poll_decorator()`:

```python
from your_addon.ackit import ACK, Polling
from your_addon.ackit.registry import Register
import bpy

# 1. Define una función de polling reutilizable
def has_animation_data(context):
    """Verifica si el objeto activo tiene datos de animación."""
    return (context.active_object is not None and 
            context.active_object.animation_data is not None and
            context.active_object.animation_data.action is not None)

# 2. Crea un decorador a partir de la función
HAS_ANIMATION = Polling.make_poll_decorator(has_animation_data)

# 3. Crea otra condición de polling para objetos con modificadores
HAS_MODIFIERS = Polling.make_poll_decorator(
    lambda context: context.active_object is not None and len(context.active_object.modifiers) > 0
)

# 4. Usa los decoradores personalizados en tus operadores

@HAS_ANIMATION
@Register.OPS.GENERIC
class AnimationOperator(ACK.Register.Types.Ops.Generic):
    """Operador que solo funciona con objetos animados."""
    
    bl_idname = "animation.process_action"
    bl_label = "Procesar Animación"
    bl_description = "Realiza operaciones en la animación del objeto activo"
    
    def execute(self, context):
        action = context.active_object.animation_data.action
        self.report({'INFO'}, f"Procesando acción: {action.name} ({len(action.fcurves)} curvas F)")
        # Implementación para procesar la animación
        return {'FINISHED'}

@HAS_MODIFIERS
@Polling.MODE.OBJECT  # Combinando con decoradores predefinidos
@Register.OPS.GENERIC
class ModifierOperator(ACK.Register.Types.Ops.Generic):
    """Operador que solo funciona con objetos que tienen modificadores."""
    
    bl_idname = "object.process_modifiers"
    bl_label = "Procesar Modificadores"
    bl_description = "Realiza operaciones en los modificadores del objeto activo"
    
    def execute(self, context):
        obj = context.active_object
        modifier_count = len(obj.modifiers)
        self.report({'INFO'}, f"Procesando {modifier_count} modificadores en {obj.name}")
        # Implementación para trabajar con modificadores
        return {'FINISHED'}
```

## Combinando Múltiples Condiciones

Puedes combinar múltiples decoradores de polling para crear condiciones complejas:

```python
@Polling.ACTIVE_OBJECT.MESH
@Polling.MODE.EDIT_MESH
@HAS_MODIFIERS
@Polling.custom(lambda context: context.edit_object.data.vertices and len(context.edit_object.data.vertices) > 10)
@Register.OPS.GENERIC
class ComplexMeshOperator(ACK.Register.Types.Ops.Generic):
    """Operador con múltiples condiciones de polling."""
    
    bl_idname = "mesh.complex_operation"
    bl_label = "Operación Compleja en Malla"
    
    def execute(self, context):
        # Este operador solo está disponible cuando:
        # 1. El objeto activo es una malla
        # 2. Estamos en modo edición
        # 3. El objeto tiene modificadores
        # 4. La malla tiene más de 10 vértices
        self.report({'INFO'}, "Todas las condiciones cumplidas")
        return {'FINISHED'}
```

## Consejos y Mejores Prácticas

1. **Mantén las funciones de polling ligeras:** Estas funciones se ejecutan frecuentemente en la interfaz, así que evita cálculos pesados.

2. **Separa la lógica compleja:** Si necesitas verificaciones complejas, considera mover parte de la lógica al método `execute()`.

3. **Proporciona retroalimentación al usuario:** Cuando un operador no está disponible, los usuarios deberían poder entender por qué a través de etiquetas desactivadas o mensajes en la interfaz.

4. **Combina con la API de Register:** Utiliza los decoradores de polling junto con la API de Register para un código más limpio y mantenible.

5. **Usa funciones descriptivas:** Nombra tus funciones y decoradores de polling de manera que describan claramente la condición que verifican.

## Conclusión

El sistema de polling de ACKit proporciona una forma elegante y modular de controlar cuándo están disponibles los operadores en la interfaz de Blender. Usando los decoradores predefinidos, el decorador `custom()` o creando tus propios decoradores con `make_poll_decorator()`, puedes implementar restricciones complejas sin sobrecargar el código de la interfaz.
