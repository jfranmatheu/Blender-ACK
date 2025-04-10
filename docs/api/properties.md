# Sistema de Propiedades en ACKit

ACKit ofrece un sistema de propiedades mejorado sobre la API estándar de Blender, proporcionando una sintaxis más limpia y tipado fuerte.

## Introducción

Las propiedades en Blender se utilizan para definir datos configurables para operadores, paneles y objetos. ACKit proporciona dos sistemas de propiedades:

1. **Propiedades Básicas** (`ACK.Props`): Compatibles con la API estándar de Blender
2. **Propiedades Tipadas** (`ACK.PropsWrapped`): Con tipado fuerte y sintaxis fluida

## Propiedades Básicas (ACK.Props)

El sistema de propiedades básicas proporciona una interfaz consistente con la API estándar de Blender:

```python
from ...ackit import ACK

# Definición de propiedades básicas
my_int = ACK.Props.Int(name="Mi Entero", default=5, min=0, max=10)
my_float = ACK.Props.Float(name="Mi Float", default=0.5, min=0.0, max=1.0)
my_bool = ACK.Props.Bool(name="Mi Bool", default=True)
my_string = ACK.Props.String(name="Mi String", default="Hola")
my_enum = ACK.Props.Enum(name="Mi Enum", 
                         items=[
                             ('OPT1', "Opción 1", "Descripción de opción 1"),
                             ('OPT2', "Opción 2", "Descripción de opción 2")
                         ],
                         default='OPT1')
```

## Propiedades Tipadas (ACK.PropsWrapped)

El sistema de propiedades tipadas proporciona varias ventajas sobre el sistema básico:

1. **Tipado Fuerte**: Mejor experiencia en IDEs con autocompletado y comprobaciones de tipo
2. **Sintaxis Fluida**: Permite encadenar métodos para configurar propiedades
3. **Validación en Tiempo de Desarrollo**: Detecta errores de configuración antes de la ejecución

```python
from ...ackit import ACK

# Definición de propiedades tipadas
my_int = ACK.PropsWrapped.Int("Mi Entero").default(5).min(0).max(10)
my_float = ACK.PropsWrapped.Float("Mi Float").default(0.5).min(0.0).max(1.0)
my_bool = ACK.PropsWrapped.Bool("Mi Bool").default(True)
my_string = ACK.PropsWrapped.String("Mi String").default("Hola")
my_enum = ACK.PropsWrapped.Enum("Mi Enum").items([
              ('OPT1', "Opción 1", "Descripción de opción 1"),
              ('OPT2', "Opción 2", "Descripción de opción 2")
          ]).default('OPT1')
```

## Tipos de Propiedades Disponibles

ACKit proporciona los siguientes tipos de propiedades, tanto en `ACK.Props` como en `ACK.PropsWrapped`:

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `Int` | Números enteros | `ACK.PropsWrapped.Int("Cantidad").default(1).min(0)` |
| `Float` | Números de punto flotante | `ACK.PropsWrapped.Float("Escala").default(1.0)` |
| `Bool` | Valores booleanos | `ACK.PropsWrapped.Bool("Activado").default(True)` |
| `String` | Cadenas de texto | `ACK.PropsWrapped.String("Nombre").default("")` |
| `Enum` | Enumeraciones | `ACK.PropsWrapped.Enum("Tipo").items(items_list)` |
| `Collection` | Colecciones de elementos | `ACK.PropsWrapped.Collection("Items")` |
| `FloatVector` | Vectores de punto flotante | `ACK.PropsWrapped.FloatVector("Color").size(4)` |
| `IntVector` | Vectores de enteros | `ACK.PropsWrapped.IntVector("Resolución").size(2)` |
| `PointerProperty` | Referencias a otros objetos | `ACK.PropsWrapped.Pointer("Objeto").type(MyClass)` |

## Configuración de Propiedades

Cada tipo de propiedad tiene diferentes opciones de configuración. Algunos ejemplos comunes:

### Propiedad Float

```python
my_float = ACK.PropsWrapped.Float("Mi Float")
    .default(0.5)      # Valor predeterminado
    .min(0.0)          # Valor mínimo
    .max(1.0)          # Valor máximo
    .precision(3)      # Precisión decimal
    .subtype('FACTOR') # Subtipo de la propiedad
    .unit('LENGTH')    # Unidad de medida
    .description("Descripción detallada") # Descripción para tooltips
```

### Propiedad Enum

```python
my_enum = ACK.PropsWrapped.Enum("Mi Enum")
    .items([
        ('OPT1', "Opción 1", "Descripción de opción 1", 'WORLD', 0),
        ('OPT2', "Opción 2", "Descripción de opción 2", 'OBJECT', 1)
    ])
    .default('OPT1')           # Valor predeterminado
    .update(my_update_func)    # Función de actualización
```

### Propiedad Collection

```python
my_collection = ACK.PropsWrapped.Collection("Mi Colección")
    .type(MyPropertyClass)     # Tipo de elementos en la colección
```

## Uso en Clases

Las propiedades se utilizan comúnmente en clases de Blender como operadores, paneles, y grupos de propiedades:

### En Operadores

```python
from ...ackit import ACK

class MyOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.my_operator"
    bl_label = "Mi Operador"
    
    # Propiedades del operador
    scale = ACK.PropsWrapped.Float("Escala").default(1.0).min(0.1).max(10.0)
    name = ACK.PropsWrapped.String("Nombre").default("Objeto")
    
    def execute(self, context):
        # Acceso a propiedades
        scale_value = self.scale
        name_value = self.name
        return ACK.Returns.Operator.FINISHED
```

### En Grupos de Propiedades

```python
from ...ackit import ACK

class MySettings(ACK.Register.Types.Data.PropertyGroup):
    enabled = ACK.PropsWrapped.Bool("Habilitado").default(True)
    value = ACK.PropsWrapped.Float("Valor").default(0.5)
    
    # Registro en la escena
    @classmethod
    def register(cls):
        import bpy
        bpy.types.Scene.my_settings = ACK.Register.Property(
            bpy.props.PointerProperty(type=cls)
        )
    
    @classmethod
    def unregister(cls):
        import bpy
        del bpy.types.Scene.my_settings
```

## Acceso a Propiedades

Una vez registradas, las propiedades se pueden acceder de diferentes maneras:

### En Operadores (durante la ejecución)

```python
def execute(self, context):
    # Acceso directo
    value = self.my_property
    
    # Modificación
    self.my_property = new_value
    
    return ACK.Returns.Operator.FINISHED
```

### En Grupos de Propiedades (registradas en objetos de Blender)

```python
# Acceso a propiedades registradas en la escena
value = context.scene.my_settings.value

# Modificación
context.scene.my_settings.value = 0.7
```

## Registro Manual de Propiedades

Además de definir propiedades en clases, puedes registrar propiedades manualmente en tipos de Blender:

```python
from ...ackit import ACK
import bpy

# Registrar una propiedad en la escena
ACK.Register.Property(
    bpy.props.FloatProperty(name="Mi Propiedad Global"),
    bpy.types.Scene,
    "mi_propiedad_global"
)

# Registrar múltiples propiedades
ACK.Register.Properties({
    "mi_int": bpy.props.IntProperty(name="Mi Int"),
    "mi_float": bpy.props.FloatProperty(name="Mi Float")
}, bpy.types.Object)
```

## Funciones de Actualización

Las propiedades pueden tener funciones de actualización que se ejecutan cuando el valor cambia:

```python
from ...ackit import ACK

def update_value(self, context):
    print(f"Valor actualizado a: {self.value}")

class MySettings(ACK.Register.Types.Data.PropertyGroup):
    value = ACK.PropsWrapped.Float("Valor").default(0.5).update(update_value)
```

## Propiedades Anidadas y Funciones de Get/Set

Para casos más complejos, puedes usar funciones personalizadas para obtener y establecer valores:

```python
from ...ackit import ACK

def get_custom_value(self):
    # Lógica compleja para obtener el valor
    return self.get("_custom_value", 0.0)

def set_custom_value(self, value):
    # Lógica compleja para establecer el valor
    self["_custom_value"] = value * 2

class ComplexSettings(ACK.Register.Types.Data.PropertyGroup):
    # Propiedad con funciones get/set personalizadas
    custom_value = ACK.PropsWrapped.Float("Valor Personalizado").default(0.0).get(get_custom_value).set(set_custom_value)
```

## Buenas Prácticas

1. **Usa `ACK.PropsWrapped` para Nuevos Desarrollos**: Proporciona mejor tipado y validación
2. **Mantén la Consistencia**: Usa el mismo sistema de propiedades en todo tu addon
3. **Documenta tus Propiedades**: Usa el campo `description` para proporcionar información
4. **Valida Rangos**: Define siempre `min` y `max` para propiedades numéricas cuando sea posible
5. **Usa Subtipos Apropiados**: Facilita la edición con subtipos como 'COLOR', 'ANGLE', etc.

## Referencia Completa

Para una lista completa de parámetros y métodos disponibles en cada tipo de propiedad, consulta la [documentación de API completa](./api_reference.md). 