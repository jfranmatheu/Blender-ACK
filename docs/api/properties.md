# Sistema de Propiedades en ACKit

ACKit ofrece un sistema de propiedades mejorado sobre la API estándar de Blender, proporcionando una sintaxis más limpia, tipado fuerte y funcionalidad de descriptor.

## Introducción

Las propiedades en Blender se utilizan para definir datos configurables para operadores, paneles, grupos de propiedades, nodos, etc. ACKit proporciona dos formas principales de definir propiedades a través de la fachada `ACK`:

1.  **`ACK.Prop`**: (Referencia a `ackit.data.props.PropertyTypes`) Proporciona acceso rápido a las funciones de propiedades de Blender (`bpy.props.*Property`) y algunas factorías convenientes (e.g., `ANGLE_DEGREE`, `FACTOR`, `COLOR_RGB`). Se usa principalmente para registrar propiedades manualmente o en contextos donde no se necesita la funcionalidad de descriptor/tipado fuerte.
2.  **`ACK.PropTyped`**: (Referencia a `ackit.data.props.WrappedTypedPropertyTypes`) Proporciona un sistema basado en descriptores con **tipado fuerte**, sintaxis fluida (encadenamiento de métodos) y gestión automática de callbacks `update`. **Este es el método recomendado** para definir propiedades en clases como `ACK.Ops.Generic`, `ACK.Data.PropertyGroup`, `ACK.NE.Node`, etc.

## Propiedades Tipadas (`ACK.PropTyped`) - Recomendado

Este sistema es el preferido por sus ventajas:

1.  **Tipado Fuerte**: Mejor experiencia en IDEs (autocompletado, comprobaciones de tipo).
2.  **Sintaxis Fluida**: Permite encadenar métodos (`.default()`, `.min()`, `.max()`, `.description()`, `.update()`) para configurar la propiedad.
3.  **Funcionalidad de Descriptor**: Permite definir propiedades directamente como atributos de clase con tipo anotado.
4.  **Gestión de `update`**: Simplifica el uso de callbacks `update`.

```python
from ..ackit import ACK

# Ejemplo de definición en un PropertyGroup
class MySettings(ACK.Data.PropertyGroup):
    # Se define como un atributo de clase
    my_int: ACK.PropTyped.Int("Mi Entero", default=5).min(0).max(10)
    my_float: ACK.PropTyped.Float("Mi Float", default=0.5).min(0.0).max(1.0)
    my_bool: ACK.PropTyped.Bool("Mi Bool", default=True)
    my_string: ACK.PropTyped.String("Mi String", default="Hola")
    my_enum: ACK.PropTyped.Enum("Mi Enum", items=[
                      ('OPT1', "Opción 1", "Descripción 1"),
                      ('OPT2', "Opción 2", "Descripción 2")
                  ]).default('OPT1')
    my_object: ACK.PropTyped.Data.Object("Mi Objeto") # Propiedad Puntero
```

### Tipos Comunes con `ACK.PropTyped`

| Método              | Tipo Retornado (Hint) | `bpy.props` Equivalente | Notas                                            |
| :------------------ | :-------------------- | :---------------------- | :----------------------------------------------- |
| `Int()`             | `int`                 | `IntProperty`           | Entero.                                          |
| `Float()`           | `float`               | `FloatProperty`         | Punto flotante.                                  |
| `Bool()`            | `bool`                | `BoolProperty`          | Booleano.                                        |
| `String()`          | `str`                 | `StringProperty`        | Cadena de texto.                                 |
| `DirPath()`         | `str`                 | `StringProperty`        | Subtipo `DIR_PATH`.                              |
| `FilePath()`        | `str`                 | `StringProperty`        | Subtipo `FILE_PATH`.                             |
| `FileName()`        | `str`                 | `StringProperty`        | Subtipo `FILE_NAME`.                             |
| `Enum()`            | `str` / `set[str]`    | `EnumProperty`          | `multiple_selection=True` devuelve `set[str]`. |
| `Vector()`          | `Vector`              | `*VectorProperty`       | Vector matemático (`mathutils.Vector`).        |
| `Color()`           | `Color`               | `FloatVectorProperty`   | Color (`mathutils.Color`), subtipo `COLOR`.      |
| `Matrix3x3()`       | `Matrix`              | `FloatVectorProperty`   | Matriz 3x3 (`mathutils.Matrix`).               |
| `Matrix4x4()`       | `Matrix`              | `FloatVectorProperty`   | Matriz 4x4 (`mathutils.Matrix`).               |
| `Angle()`           | `float`               | `FloatProperty`         | Subtipo `ANGLE`, unidad `ROTATION`.              |
| `Factor()`          | `float`               | `FloatProperty`         | Valor entre 0.0 y 1.0.                           |
| `Data.Pointer()`    | `bpy.types.ID`        | `PointerProperty`       | Puntero genérico (especificar `type`).         |
| `Data.Object()`     | `bpy.types.Object`    | `PointerProperty`       | Puntero a `bpy.types.Object`.                  |
| `Data.Material()`   | `bpy.types.Material`  | `PointerProperty`       | Puntero a `bpy.types.Material`.                |
| `Data.Collection()` | `bpy.types.Collection` | `CollectionProperty`    | Colección (requiere `type=MyPropertyGroup`).   |
| *(Otros punteros)*  | *(Varios)*            | `PointerProperty`       | `Mesh`, `Texture`, `Scene`, `Image`, etc.        |

### Métodos de Configuración (Encadenables)

- `.default(value)`: Establece el valor predeterminado.
- `.min(value)`: Valor mínimo (numérico).
- `.max(value)`: Valor máximo (numérico).
- `.description(text)`: Texto para el tooltip.
- `.update(callback_func)`: Añade una función callback que se ejecuta al cambiar el valor. La función recibe `(self, context)`.
- `.items(list_of_tuples)`: Para `Enum`, define los ítems. Formato: `[(id, name, desc, icon, number), ...]`.
- `.size(int_or_tuple)`: Para `Vector` y `Matrix`, define las dimensiones.
- `type(bpy_type)`: Para `Pointer` y `Collection`, especifica el tipo de Blender referenciado.

### Uso en Clases

Se definen como atributos de clase con anotación de tipo:

```python
from ..ackit import ACK

class MyOperator(ACK.Ops.Action):
    bl_idname = "object.my_operator"
    bl_label = "Mi Operador"
    
    # Propiedades del operador
    scale: ACK.PropTyped.Float("Escala").default(1.0).min(0.1).max(10.0)
    name: ACK.PropTyped.String("Nombre").default("Objeto")
    
    def action(self, context):
        # Acceso directo a través de self
        print(f"Escala: {self.scale}, Nombre: {self.name}")
        # ... lógica del operador ...
        return {'FINISHED'}
```

## Propiedades Básicas (`ACK.Prop`)

Este sistema es una capa fina sobre `bpy.props`. Es útil para registro manual o cuando no se necesita/desea la funcionalidad de descriptor.

```python
from ..ackit import ACK
import bpy

# Definición de propiedades básicas (equivalente a bpy.props.*)
my_int_prop_func = ACK.Prop.INT # Equivale a bpy.props.IntProperty
my_float_prop_func = ACK.Prop.Float # Equivale a bpy.props.FloatProperty

# Ejemplo de registro manual en un tipo de Blender
def register():
    bpy.types.Scene.my_basic_int = my_int_prop_func(name="Entero Básico", default=10)
    bpy.types.Scene.my_basic_float = ACK.Prop.FACTOR(name="Factor Básico") # Usa factoría

def unregister():
    del bpy.types.Scene.my_basic_int
    del bpy.types.Scene.my_basic_float
```

### Tipos y Factorías Comunes con `ACK.Prop`

- `FLOAT`, `INT`, `BOOL`, `STRING`, `ENUM`, `FLOAT_VECTOR`, `INT_VECTOR`, `BOOL_VECTOR`, `POINTER_CUSTOM`, `COLLECTION`: Equivalentes directos a `bpy.props.*`.
- `ANGLE_DEGREE`, `FACTOR`: Factorías para Floats con subtipos/rangos comunes.
- `IVECTOR_2/3/XY/XYZ/N`, `VECTOR_2/3/XY/XYZ/AXISANGLE/N`: Factorías para Vectores.
- `COLOR_RGB/RGBA`: Factorías para Colores.
- `MATRIX_2/3/4/N`: Factorías para Matrices.
- `DIRPATH`, `FILEPATH`: Factorías para Strings con subtipo path.
- `POINTER.OBJECT/MESH/etc`: Factorías para Pointers a tipos comunes.
- `POINTER.CUSTOM(name, type, **kwargs)`: Para Pointers a tipos personalizados.

## Funciones de Actualización (`update`)

Con `ACK.PropTyped`, se añade fácilmente una función `update`:

```python
from ..ackit import ACK

def my_update_callback(self, context):
    print(f"Propiedad '{self.name}' actualizada a: {self.value}")

class MySettings(ACK.Data.PropertyGroup):
    value: ACK.PropTyped.Float("Valor").default(0.5).update(my_update_callback)
```

**Importante:** La función `update` recibe `(self, context)`, donde `self` es la instancia de la clase contenedora (e.g., la instancia de `MySettings`).

## Registro Manual de Propiedades (`ACK.Data.register_property`)

Aunque `ACK.PropTyped` maneja el registro automáticamente cuando se usa como atributo de clase en tipos registrados por `ackit` (como `PropertyGroup`), a veces necesitas registrar una propiedad `ACK.PropTyped` en un tipo de Blender existente (`bpy.types.Scene`, `bpy.types.Object`, etc.). Para esto se usa `ACK.Data.register_property` o `ACK.Data.batch_register_properties` desde la función `register()` de tu addon.

```python
from ..ackit import ACK
import bpy

# Definir la propiedad como descriptor (pero no como atributo de clase)
my_global_prop = ACK.PropTyped.String("Propiedad Global", default="Test")

def register():
    # Registrarla manualmente en bpy.types.Scene
    ACK.Data.register_property(
        bpy_type=bpy.types.Scene, 
        property_idname="my_global_ack_prop", 
        property=my_global_prop, # Pasar el descriptor
        remove_on_unregister=True # Opcional: eliminarla al desregistrar
    )

def unregister():
    # La eliminación es automática si remove_on_unregister=True
    pass
```

## Buenas Prácticas

1.  **Prefiere `ACK.PropTyped`**: Para propiedades en tus clases (`PropertyGroup`, `Operator`, `Node`, `Panel`, etc.) por su tipado y sintaxis.
2.  **Usa `ACK.Prop` o `bpy.props`**: Para registro manual directo en `bpy.types` si no necesitas las características de `PropTyped`.
3.  **Consistencia**: Elige un estilo y mantenlo.
4.  **Documenta**: Usa `.description()` con `PropTyped` o el argumento `description=` con `Prop`.
5.  **Valida Rangos**: Usa `.min()` y `.max()`.
6.  **Subtipos**: Usa subtipos (`subtype='COLOR'`, etc.) para mejorar la UI.

## Referencia Completa

Para una lista completa de parámetros y métodos disponibles en cada tipo de propiedad, consulta la [documentación de API completa](./api_reference.md). 