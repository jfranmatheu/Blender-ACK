# Creación de Operadores Básicos

Este tutorial te guiará a través del proceso de creación de diferentes tipos de operadores usando ACKit.

## Introducción a los Operadores en Blender

Los operadores son la forma principal de añadir funcionalidad interactiva a Blender. En ACKit, los operadores se manejan a través de clases que heredan de alguno de los tres tipos principales:

- **Generic**: Operadores estándar con comportamiento básico
- **Action**: Operadores con UI integrada y estructura simplificada
- **Modal**: Operadores interactivos que mantienen un estado mientras están activos

## Operador Genérico

### Estructura Básica

Los operadores genéricos (`ACK.Register.Types.Ops.Generic`) son la forma más básica de operadores en Blender. Heredan directamente del tipo `bpy.types.Operator`.

```python
from ...ackit import ACK

class SimpleOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.simple_operator"  # Identificador único del operador
    bl_label = "Operador Simple"          # Nombre visible para el usuario
    bl_description = "Un operador simple" # Descripción para tooltips
    
    # Definición de propiedades
    message = ACK.PropsWrapped.String("Mensaje").default("Hola desde ACKit")
    
    # El método principal que Blender llama al ejecutar el operador
    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}  # También puedes usar ACK.Returns.Operator.FINISH
```

### Añadiendo Condiciones de Disponibilidad

Puedes controlar cuándo está disponible un operador usando los decoradores de polling:

```python
from ...ackit import ACK

@ACK.Poll.ACTIVE_OBJECT.MESH  # Solo disponible cuando hay un objeto malla activo
@ACK.Poll.MODE.OBJECT         # Solo disponible en modo objeto
class MeshOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.mesh_operator"
    bl_label = "Operador de Malla"
    
    def execute(self, context):
        # Acceder al objeto malla activo de forma segura
        mesh = context.active_object.data
        self.report({'INFO'}, f"La malla tiene {len(mesh.vertices)} vértices")
        return {'FINISHED'}
```

### Métodos Importantes

Los operadores genéricos soportan varios métodos importantes:

```python
from ...ackit import ACK

class CompleteOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.complete_operator"
    bl_label = "Operador Completo"
    
    # Propiedades del operador
    value = ACK.PropsWrapped.Float("Valor").default(0.5).min(0.0).max(1.0)
    
    # Llamado cuando se invoca el operador con 'INVOKE_DEFAULT'
    def invoke(self, context, event):
        # Preparación antes de mostrar la UI o ejecutar
        return self.execute(context)  # O return context.window_manager.invoke_props_dialog(self)
    
    # Implementación principal del operador
    def execute(self, context):
        self.report({'INFO'}, f"Ejecutando con valor: {self.value}")
        return {'FINISHED'}
    
    # Dibuja la UI del operador para diálogos y paneles de propiedades
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "value")
```

## Operador de Acción

Los operadores de acción (`ACK.Register.Types.Ops.Action`) son una abstracción que simplifica la creación de operadores con UI.

```python
from ...ackit import ACK

@ACK.Flags.OPERATOR.REGISTER_UNDO  # Añadir el operador a la historia de deshacer
class ActionOperator(ACK.Register.Types.Ops.Action):
    label = "Test Action"          # Equivalente a bl_label
    tooltip = "Hace algo útil"     # Equivalente a bl_description
    
    # Propiedades con tipado fuerte
    enable = ACK.PropsWrapped.Bool("Habilitar").default(True)
    z_location = ACK.PropsWrapped.Float("Z").default(0.0).min(-10.0).max(10.0)
    
    # Método para dibujar la UI del operador (reemplaza a draw)
    def draw_ui(self, context, layout):
        col = layout.column()
        col.prop(self, 'enable', text="Habilitar Característica")
        col.prop(self, 'z_location', text="Posición Z")
    
    # Método principal (reemplaza a execute)
    def action(self, context) -> None:
        if self.enable:
            obj = context.active_object
            if obj:
                obj.location.z = self.z_location
                # Helper para reporte (equivalente a self.report({'INFO'}, msg))
                self.report_info(f"Posición Z establecida a {self.z_location}")
            else:
                self.report_error("No hay objeto activo")
```

### Creación a partir de Funciones

También puedes crear operadores de acción directamente a partir de funciones:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.ACTION(
    label="Acción desde Función",
    tooltip="Operador creado a partir de una función"
)
def mi_accion(context):
    # Implementación de la acción
    if context.active_object:
        context.active_object.location.z = 1.0
        return {'FINISHED'}
    return {'CANCELLED'}
```

## Operador Modal

Los operadores modales (`ACK.Register.Types.Ops.Modal`) son utilizados para operaciones interactivas que mantienen el estado y continúan ejecutándose hasta que se completan o cancelan.

```python
from ...ackit import ACK, OpsReturn
from ...ackit.utils import IsEventType, IsEventValue

@ACK.Poll.ACTIVE_OBJECT.ANY
class SimpleModalOperator(ACK.Register.Types.Ops.Modal):
    # Inicialización al entrar en modo modal
    def modal_enter(self, context, event):
        self.initial_location = context.active_object.location.copy()
        self.offset = 0.0
        context.window_manager.modal_handler_add(self)
        # No necesitas devolver nada aquí
    
    # Llamado en cada actualización de evento
    def modal_update(self, context, event) -> OpsReturn:
        # Manejar eventos
        if event.type == 'MOUSEMOVE':
            # Actualizar el estado basado en el movimiento del ratón
            self.offset += event.mouse_x - event.mouse_prev_x
            context.active_object.location.x = self.initial_location.x + self.offset * 0.01
            context.area.tag_redraw()  # Actualizar la vista
            return OpsReturn.RUN  # Continuar el modo modal
            
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            # Finalizar el operador con éxito
            self.report_info("Operación completada")
            return OpsReturn.FINISH
            
        elif event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
            # Cancelar y restaurar el estado original
            context.active_object.location = self.initial_location
            self.report_info("Operación cancelada")
            return OpsReturn.CANCEL
            
        elif event.type == 'ESC' and event.value == 'RELEASE':
            # Otra forma de cancelar
            context.active_object.location = self.initial_location
            return OpsReturn.CANCEL
            
        # Pasar el evento a otros manejadores
        return OpsReturn.PASS
    
    # Limpieza al salir del modo modal (opcional)
    def modal_exit(self, context, cancelled):
        # Limpiar cualquier estado del operador
        if cancelled:
            self.report_info("Operación cancelada y limpiada")
        else:
            self.report_info("Operación finalizada y limpiada")
```

### Operador Modal con Dibujado en Pantalla

Puedes añadir dibujado personalizado en el viewport utilizando el flag `DRAW_POST_PIXEL`:

```python
from ...ackit import ACK, OpsReturn
import blf  # Módulo de Blender para dibujar texto

@ACK.Flags.MODAL.DRAW_POST_PIXEL.VIEW_3D  # Habilitar dibujado en el viewport 3D
@ACK.Poll.ACTIVE_OBJECT.ANY
class ModalDrawOperator(ACK.Register.Types.Ops.Modal):
    def modal_enter(self, context, event):
        self.text = "Arrastra para mover"
        self.mouse_x = 0
        self.mouse_y = 0
        context.window_manager.modal_handler_add(self)
    
    def modal_update(self, context, event) -> OpsReturn:
        if event.type == 'MOUSEMOVE':
            self.mouse_x = event.mouse_x
            self.mouse_y = event.mouse_y
            self.tag_redraw(context)  # Helper para forzar redibujado
            return OpsReturn.RUN
            
        elif event.type == 'ESC':
            return OpsReturn.FINISH
            
        return OpsReturn.PASS
    
    # Este método se llama automáticamente para dibujar en el viewport
    def draw_2d(self, context):
        # Configurar el dibujado de texto
        blf.size(0, 20)  # Font id 0, tamaño 20
        blf.position(0, self.mouse_x, self.mouse_y, 0)
        blf.color(0, 1.0, 0.0, 0.0, 1.0)  # Color rojo
        blf.draw(0, self.text)  # Dibujar el texto
        
        # También puedes dibujar líneas, rectángulos, etc. usando el módulo gpu
```

## Invocación de Operadores

### Desde la Interfaz de Usuario

Para incluir tu operador en la UI, puedes añadirlo a un panel o menú:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def my_panel(context, layout):
    layout.label(text="Mi Panel de Operadores")
    
    # Añadir un botón para el operador
    layout.operator("object.simple_operator")
    
    # Añadir un operador con propiedades preconfiguradas
    op = layout.operator("object.mesh_operator")
    op.some_property = "Valor predefinido"
```

### Desde Código

Si has habilitado `AutoCode.OPS` en la inicialización, puedes invocar operadores de forma tipada:

```python
# Desde cualquier parte de tu código
from ops import MYPREFIX_OT_Simple_Operator

# Ejecutar con valores predeterminados o personalizados
MYPREFIX_OT_Simple_Operator.run()
MYPREFIX_OT_Simple_Operator.run(message="Mi mensaje personalizado")

# Invocar con UI (equivalente a 'INVOKE_DEFAULT')
MYPREFIX_OT_Simple_Operator.run_invoke()
```

## Prácticas Recomendadas

1. **Usa el tipo adecuado para cada caso**:
   - `Generic`: Para operadores simples sin UI personalizada
   - `Action`: Para operadores con UI integrada y estructura clara
   - `Modal`: Para operaciones interactivas que requieren varios pasos

2. **Implementa adecuadamente el método `poll`** (o usa decoradores):
   - Verifica que el operador solo esté disponible cuando puede ejecutarse correctamente
   - Previene errores y mejora la experiencia del usuario

3. **Utiliza el sistema de reporte apropiadamente**:
   - `self.report_info()`: Para información general
   - `self.report_warning()`: Para advertencias que no impiden la operación
   - `self.report_error()`: Para errores que detienen la operación

4. **Añade deshacer para operaciones que modifican datos**:
   - Usa el decorador `@ACK.Flags.OPERATOR.REGISTER_UNDO`

5. **Utiliza operadores modales para operaciones complejas**:
   - Divide la lógica en fases claras (inicio, actualización, finalización)
   - Responde adecuadamente a eventos del usuario
   - Proporciona retroalimentación visual cuando sea apropiado 