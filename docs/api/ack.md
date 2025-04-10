# Clase ACK

La clase `ACK` es el punto de entrada principal para todas las funcionalidades de ACKit. Está diseñada siguiendo el patrón de diseño Facade, proporcionando una API unificada, jerárquica y bien organizada para acceder a todas las capacidades del framework.

## Estructura

La clase `ACK` contiene varias clases y métodos anidados organizados jerárquicamente:

```python
class ACK:
    class Register:
        # Métodos y clases de registro
        
    class Types:
        # Tipos personalizados
        
    class Returns:
        # Valores de retorno para operadores
        
    class Props:
        # Propiedades sin tipado fuerte
        
    class PropsWrapped:
        # Propiedades con tipado fuerte
        
    class Flags:
        # Flags y opciones para clases
        
    # Otras propiedades y métodos
```

## Métodos Principales

### ACK.Register

La clase `ACK.Register` contiene métodos y subclases para registrar componentes:

```python
# Registro directo de propiedades
ACK.Register.Property(cls, name, property_definition)
ACK.Register.Properties(cls, properties_dict)

# Tipos disponibles para heredar
class ACK.Register.Types.Ops.Generic    # Operador genérico
class ACK.Register.Types.Ops.Action     # Operador de acción
class ACK.Register.Types.Ops.Modal      # Operador modal
class ACK.Register.Types.UI.Panel       # Panel
class ACK.Register.Types.UI.Menu        # Menú
class ACK.Register.Types.UI.PieMenu     # Menú circular
class ACK.Register.Types.UI.Popover     # Popover
class ACK.Register.Types.UI.UIList      # Lista personalizada
class ACK.Register.Types.Data.PropertyGroup  # Grupo de propiedades
class ACK.Register.Types.Data.AddonPreferences  # Preferencias de addon
class ACK.Register.Types.Nodes.Node     # Nodo
class ACK.Register.Types.Nodes.Tree     # Árbol de nodos
class ACK.Register.Types.Nodes.Socket   # Socket de nodo

# Decoradores para crear clases a partir de funciones
ACK.Register.FromFunction.ACTION        # Crear operador de acción
ACK.Register.FromFunction.PANEL         # Crear panel
ACK.Register.FromFunction.MENU          # Crear menú
ACK.Register.FromFunction.PIE_MENU      # Crear menú circular
ACK.Register.FromFunction.POPOVER       # Crear popover
```

### ACK.Props y ACK.PropsWrapped

Estas clases contienen definiciones para propiedades de Blender:

```python
# Propiedades básicas (sin tipado fuerte)
my_bool = ACK.Props.Bool("Mi Booleano")
my_int = ACK.Props.Int("Mi Entero")
my_float = ACK.Props.Float("Mi Flotante")
my_string = ACK.Props.String("Mi Texto")
my_enum = ACK.Props.Enum("Mi Enum", items=[("A", "A", ""), ("B", "B", "")])
my_collection = ACK.Props.Collection("Mi Colección")
my_pointer = ACK.Props.Pointer("Mi Puntero", type=SomePropertyGroup)

# Propiedades con tipado fuerte (recomendadas)
my_bool = ACK.PropsWrapped.Bool("Mi Booleano").default(True)
my_int = ACK.PropsWrapped.Int("Mi Entero").default(5).min(0).max(10)
my_float = ACK.PropsWrapped.Float("Mi Flotante").default(1.5).min(0.0).max(10.0)
my_string = ACK.PropsWrapped.String("Mi Texto").default("Valor predeterminado")
my_enum = ACK.PropsWrapped.Enum("Mi Enum").items(
    ("A", "Opción A", "Descripción A"),
    ("B", "Opción B", "Descripción B")
).default("A")
```

### ACK.Flags

La clase `ACK.Flags` contiene decoradores para modificar el comportamiento de clases:

```python
# Flags para operadores
@ACK.Flags.OPERATOR.REGISTER_UNDO      # Añadir a historia de deshacer
@ACK.Flags.OPERATOR.INTERNAL           # Operador interno
@ACK.Flags.OPERATOR.BLOCKING           # Bloquear interfaz durante ejecución
@ACK.Flags.OPERATOR.PRESET             # Permitir presets

# Flags para operadores modales
@ACK.Flags.MODAL.DRAW_POST_PIXEL.VIEW_3D  # Dibujar en viewport 3D
@ACK.Flags.MODAL.USE_MOUSE               # Usar eventos de ratón

# Flags para paneles
@ACK.Flags.PANEL.HIDE_HEADER            # Panel con cabecera oculta
@ACK.Flags.PANEL.DEFAULT_CLOSED         # Panel cerrado por defecto
@ACK.Flags.PANEL.INSTANCED              # Panel con instancias

# Flags para nodos
@ACK.Flags.NODE_CATEGORY("Mi Categoría")  # Asignar categoría a un nodo
```

### ACK.Poll

La clase `ACK.Poll` contiene decoradores para definir condiciones de disponibilidad:

```python
# Verificación de objeto activo
@ACK.Poll.ACTIVE_OBJECT.ANY       # Cualquier objeto activo
@ACK.Poll.ACTIVE_OBJECT.MESH      # Solo objetos mesh activos
@ACK.Poll.ACTIVE_OBJECT.ARMATURE  # Solo armaduras activas

# Verificación de modo
@ACK.Poll.MODE.OBJECT             # Solo en modo objeto
@ACK.Poll.MODE.EDIT               # Solo en modo edición
@ACK.Poll.MODE.POSE               # Solo en modo pose

# Polling personalizado
@ACK.Poll.custom(lambda cls, context: context.scene.render.engine == 'CYCLES')
```

### ACK.Returns

La clase `ACK.Returns` contiene constantes para valores de retorno:

```python
# Valores de retorno para operadores
ACK.Returns.Operator.FINISH       # {'FINISHED'}
ACK.Returns.Operator.CANCEL       # {'CANCELLED'}
ACK.Returns.Operator.PASS         # {'PASS_THROUGH'}
ACK.Returns.Operator.RUNNING      # {'RUNNING_MODAL'}

# Valores de retorno para submodos
ACK.Returns.Submodal.FINISH       # Finalizar submodo
ACK.Returns.Submodal.CANCEL       # Cancelar submodo
ACK.Returns.Submodal.RUNNING      # Continuar submodo
```

### Métodos para Sistema de Nodos

La clase `ACK` también proporciona métodos para trabajar con nodos:

```python
# Definición de sockets de nodo
input_socket = ACK.NodeInput(ACK.Types.NodeSocketFloat)  # Socket de entrada
output_socket = ACK.NodeOutput(ACK.Types.NodeSocketFloat)  # Socket de salida
```

## Ejemplos de Uso

### Creación de un Operador de Acción

```python
from ...ackit import ACK

@ACK.Flags.OPERATOR.REGISTER_UNDO
@ACK.Poll.ACTIVE_OBJECT.MESH
class MyActionOperator(ACK.Register.Types.Ops.Action):
    label = "Mi Operador"
    tooltip = "Hace algo interesante"
    
    # Propiedades
    value = ACK.PropsWrapped.Float("Valor").default(0.5).min(0.0).max(1.0)
    
    # UI del operador
    def draw_ui(self, context, layout):
        layout.prop(self, "value", text="Intensidad")
    
    # Lógica del operador
    def action(self, context):
        obj = context.active_object
        # Hacer algo con obj y self.value
        self.report_info(f"Operación realizada con valor {self.value}")
```

### Creación de un Panel

```python
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def my_panel(context, layout):
    layout.label(text="Panel de Mi Addon")
    
    # Añadir botones
    row = layout.row()
    row.operator("object.my_action_operator")
    row.operator("object.another_operator")
    
    # Añadir propiedades
    layout.prop(context.scene, "mi_addon_valor")
```

### Trabajando con Nodos

```python
from ...ackit import ACK

@ACK.Flags.NODE_CATEGORY("Math")
class AddNode(ACK.Register.Types.Nodes.Node):
    bl_label = "Add"
    
    # Definir sockets
    input_a = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    input_b = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)
    
    # Lógica de evaluación
    def evaluate(self):
        self.result.value = self.input_a.value + self.input_b.value
```

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