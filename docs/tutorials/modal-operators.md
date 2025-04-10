# Operadores Modales con ACKit

Este tutorial te guiará en la creación de operadores modales interactivos utilizando ACKit.

## ¿Qué son los Operadores Modales?

Los operadores modales son operadores que mantienen un estado y continúan ejecutándose hasta que son explícitamente terminados o cancelados. Se utilizan para interacciones complejas como herramientas de dibujo, manipulaciones de objetos en tiempo real, o cualquier operación que requiera múltiples pasos o entrada continua del usuario.

## Estructura Básica de un Operador Modal en ACKit

ACKit proporciona la clase base `ACK.Register.Types.Ops.Modal` que simplifica la creación de operadores modales:

```python
from ...ackit import ACK

class SimpleModalOperator(ACK.Register.Types.Ops.Modal):
    # 1. Método de inicialización
    def modal_enter(self, context, event):
        # Inicialización al entrar en modo modal
        self.value = 0
        
    # 2. Método de actualización (llamado continuamente)
    def modal_update(self, context, event):
        # Procesar eventos y actualizar estado
        if event.type == 'MOUSEMOVE':
            self.value = event.mouse_x
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'LEFTMOUSE':
            # Terminar con éxito
            return ACK.Returns.Modal.FINISHED
            
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            # Cancelar operación
            return ACK.Returns.Modal.CANCELLED
            
        # Continuar en modo modal
        return ACK.Returns.Modal.RUNNING_MODAL
        
    # 3. Método de finalización
    def modal_exit(self, context):
        # Limpieza al salir del modo modal
        pass
```

## Tipos de Retorno para Operadores Modales

ACKit proporciona constantes para los valores de retorno de operadores modales:

- `ACK.Returns.Modal.RUNNING_MODAL`: Continuar en modo modal
- `ACK.Returns.Modal.FINISHED`: Terminar con éxito
- `ACK.Returns.Modal.CANCELLED`: Cancelar la operación
- `ACK.Returns.Modal.PASS_THROUGH`: Pasar el evento a otros operadores

## Ejemplo: Operador Modal con Dibujo en Pantalla

Un caso de uso común para operadores modales es el dibujo en pantalla. Vamos a crear un operador que dibuje texto en el viewport:

```python
from ...ackit import ACK
import blf
import gpu
from gpu_extras.batch import batch_for_shader

@ACK.Flags.MODAL.DRAW_POST_PIXEL.VIEW_3D  # Dibujar en el viewport 3D
class DrawTextOperator(ACK.Register.Types.Ops.Modal):
    def modal_enter(self, context, event):
        self.text = "Mueve el mouse"
        self.mouse_pos = [event.mouse_region_x, event.mouse_region_y]
        self.font_size = 20
        self.font_color = (1.0, 0.8, 0.1, 1.0)  # Amarillo
        
        # También vamos a dibujar un círculo alrededor del cursor
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        self.radius = 20
        
    def modal_update(self, context, event):
        if event.type == 'MOUSEMOVE':
            self.mouse_pos = [event.mouse_region_x, event.mouse_region_y]
            self.text = f"Mouse en: {self.mouse_pos[0]}, {self.mouse_pos[1]}"
            # Forzar el redibujado de la ventana
            context.area.tag_redraw()
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'WHEELUPMOUSE':
            self.font_size += 1
            context.area.tag_redraw()
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'WHEELDOWNMOUSE':
            self.font_size = max(10, self.font_size - 1)
            context.area.tag_redraw()
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            return ACK.Returns.Modal.FINISHED
            
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return ACK.Returns.Modal.CANCELLED
            
        return ACK.Returns.Modal.PASS_THROUGH
        
    def draw_2d(self, context):
        # Dibujar texto
        blf.size(0, self.font_size)
        blf.position(0, self.mouse_pos[0] + 30, self.mouse_pos[1], 0)
        blf.color(0, *self.font_color)
        blf.draw(0, self.text)
        
        # Dibujar círculo alrededor del cursor
        self.shader.bind()
        self.shader.uniform_float("color", (1.0, 1.0, 1.0, 0.5))
        
        # Crear vértices para el círculo
        import math
        vertices = []
        segments = 32
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = self.mouse_pos[0] + self.radius * math.cos(angle)
            y = self.mouse_pos[1] + self.radius * math.sin(angle)
            vertices.append((x, y))
            
        # Dibujar el círculo
        batch = batch_for_shader(self.shader, 'LINE_LOOP', {"pos": vertices})
        batch.draw(self.shader)
```

## Agregar Propiedades al Operador Modal

Puedes agregar propiedades al operador modal como lo harías con cualquier otro operador:

```python
from ...ackit import ACK

class ModalWithPropsOperator(ACK.Register.Types.Ops.Modal):
    # Propiedades tipadas
    size = ACK.PropsWrapped.Float("Tamaño").default(1.0).min(0.1).max(10.0)
    color = ACK.PropsWrapped.FloatVector("Color").default((1.0, 0.0, 0.0)).size(3).subtype('COLOR')
    
    # Resto de la implementación...
```

## Invocación del Operador Modal

Para invocar un operador modal, necesitas usar el contexto `INVOKE_DEFAULT`:

```python
bpy.ops.my_addon.modal_operator('INVOKE_DEFAULT')
```

O si estás utilizando los wrappers generados por ACKit:

```python
from my_addon.ops import MYADDON_OT_Modal_Operator
MYADDON_OT_Modal_Operator.run_invoke()
```

## Ejemplo Completo: Herramienta de Dibujo Modal

Vamos a crear una herramienta de dibujo modal más completa que permita dibujar líneas en el viewport:

```python
from ...ackit import ACK
import bpy
import gpu
from gpu_extras.batch import batch_for_shader

@ACK.Flags.MODAL.DRAW_POST_PIXEL.VIEW_3D
class DrawingToolOperator(ACK.Register.Types.Ops.Modal):
    # Propiedades
    line_color = ACK.PropsWrapped.FloatVector("Color de Línea").default((1.0, 1.0, 1.0, 1.0)).size(4)
    line_width = ACK.PropsWrapped.Float("Grosor de Línea").default(2.0).min(1.0).max(10.0)
    
    def modal_enter(self, context, event):
        self.points = []
        self.is_drawing = False
        self.shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        self.shader.bind()
        
    def modal_update(self, context, event):
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.is_drawing = True
                self.points.append((event.mouse_region_x, event.mouse_region_y))
            elif event.value == 'RELEASE':
                self.is_drawing = False
            
            context.area.tag_redraw()
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'MOUSEMOVE' and self.is_drawing:
            self.points.append((event.mouse_region_x, event.mouse_region_y))
            context.area.tag_redraw()
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'C' and event.value == 'PRESS':
            # Limpiar puntos
            self.points = []
            context.area.tag_redraw()
            return ACK.Returns.Modal.RUNNING_MODAL
            
        elif event.type == 'RIGHTMOUSE' or event.type == 'ESC':
            # Terminar el operador
            return ACK.Returns.Modal.FINISHED
            
        return ACK.Returns.Modal.PASS_THROUGH
        
    def draw_2d(self, context):
        if len(self.points) < 2:
            return
            
        # Establecer el ancho de línea
        gpu.state.line_width_set(self.line_width)
        
        # Establecer el color
        self.shader.uniform_float("color", self.line_color)
        
        # Crear batch y dibujar
        batch = batch_for_shader(self.shader, 'LINE_STRIP', {"pos": self.points})
        batch.draw(self.shader)

# Registrar el operador mediante el decorador de keymaps
@ACK.RegDeco.KEYMAP('View3D', 'WINDOW', 'D', 'PRESS', ctrl=True)
def register_drawing_tool_keymap():
    return bpy.ops.my_addon.drawing_tool_operator.idname_for_keymap()
```

## Consejos para Operadores Modales

1. **Rendimiento**: Ten cuidado con el rendimiento en los métodos `draw_2d`, ya que se llaman en cada frame.
2. **Gestión de Estado**: Mantén un estado limpio y bien organizado en tu operador modal.
3. **Feedback Visual**: Proporciona siempre feedback visual al usuario sobre lo que está ocurriendo.
4. **Controles Intuitivos**: Usa controles estándar (ESC para cancelar, clic para confirmar) para mantener la consistencia.
5. **Modo HUD**: Considera mostrar información de ayuda en pantalla sobre los controles disponibles.

## Depuración de Operadores Modales

La depuración de operadores modales puede ser desafiante. Utiliza el sistema de depuración de ACKit:

```python
from ...ackit.debug import output

def modal_update(self, context, event):
    output.log(f"Evento: {event.type} {event.value}")
    # Resto del código...
```

## Recursos Adicionales

- [API de Referencia para Operadores Modales](../api/modal_operators.md)
- [Ejemplos de Operadores Modales](../examples/modal_examples.md)
- [Documentación de GPU de Blender](https://docs.blender.org/api/current/gpu.html) 