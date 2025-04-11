# Sistema de Registro en ACKit

El sistema de registro es uno de los componentes centrales de ACKit. Este sistema gestiona automáticamente el registro y desregistro de clases de Blender, eliminando gran parte del código boilerplate típico en el desarrollo de addons.

## Conceptos Básicos

### AddonLoader

`AddonLoader` (accesible vía `from .ackit import AddonLoader`) es la clase principal que gestiona el ciclo de vida completo del addon:

```python
# En el __init__.py principal de tu addon
from .ackit import AddonLoader, AutoCode # AutoCode es opcional

# Inicialización (descubre módulos y clases)
AddonLoader.init_modules(
    # Opciones como auto_code
)

# Registro (registra clases y llama callbacks 'register')
def register():
    AddonLoader.register_modules()

# Desregistro (desregistra clases y llama callbacks 'unregister')
def unregister():
    AddonLoader.unregister_modules()
```

### Clases Base de ACKit (`ACK.*.Generic`, etc.)

En lugar de una enumeración `BTypes`, el registro se basa en heredar de las clases base proporcionadas por la fachada `ACK`, por ejemplo:

-   `ACK.Ops.Generic`, `ACK.Ops.Action`, `ACK.Ops.Modal`
-   `ACK.UI.Panel`, `ACK.UI.Menu`, `ACK.UI.PieMenu`, `ACK.UI.Popover`, `ACK.UI.UIList`
-   `ACK.Data.PropertyGroup`, `ACK.Data.AddonPreferences`
-   `ACK.NE.Node`, `ACK.NE.NodeTree`, `ACK.NE.Socket` (base para sockets específicos)

Cuando `AddonLoader` descubre una clase que hereda de uno de estos tipos base (o tipos derivados), la gestiona automáticamente para el registro/desregistro.

## Ciclo de Vida de un Addon

ACKit define un ciclo de vida claro para los addons con callbacks específicos que puedes definir en **cualquier módulo** dentro de tu directorio `src` (o donde sea que `AddonLoader` busque):

1.  **Inicialización** (llamado por `AddonLoader.init_modules`):
    -   `init()`: Se llama durante la fase de inicialización.
    -   `late_init()`: Se llama después de la inicialización principal.

2.  **Registro** (llamado por `AddonLoader.register_modules`):
    -   `register()`: Se llama durante la fase de registro (después de registrar clases automáticamente).
    -   `late_register()`: Se llama después del registro principal.

3.  **Desregistro** (llamado por `AddonLoader.unregister_modules`):
    -   `unregister()`: Se llama durante la fase de desregistro (antes de desregistrar clases automáticamente).
    -   `late_unregister()`: Se llama después del desregistro principal.

```python
# En cualquier módulo de tu addon (e.g., src/mi_modulo.py)
def init():
    print("Inicializando mi módulo")

def register():
    print("Registrando mi módulo (después de las clases)")

def late_register():
    print("Registro tardío de mi módulo")

def unregister():
    print("Desregistrando mi módulo (antes de las clases)")
```

## Modos de Registro

ACKit proporciona diferentes enfoques para registrar componentes:

### 1. Registro Automático por Herencia (Recomendado)

El sistema detecta y registra automáticamente todas las clases que heredan de las clases base de ACKit (`ACK.Ops.*`, `ACK.UI.*`, etc.).

```python
from ...ackit import ACK
from ...ackit.enums.operator import OpsReturn

# Esta clase se registrará automáticamente
class MyOperator(ACK.Ops.Generic):
    bl_idname = "object.my_operator"
    bl_label = "Mi Operador"
    
    def execute(self, context):
        return OpsReturn.FINISH
```

### 2. Registro a partir de Funciones (`ACK.UI.create_*`)

Para componentes UI simples como paneles o menús, puedes utilizar decoradores para crear y registrar clases automáticamente a partir de funciones:

```python
from ...ackit import ACK

# Esto crea y registra un panel automáticamente
@ACK.UI.create_panel_from_func.VIEW_3D(tab="Mi Tab")
def my_panel(context, layout):
    layout.label(text="Mi Panel")
    layout.operator("object.my_operator")
```

### 3. Registro Manual de Propiedades (`ACK.Data.register_property`)

Para registrar propiedades (definidas con `ACK.PropTyped` o `ACK.Prop`) en tipos de Blender existentes (`bpy.types.Scene`, `bpy.types.Object`, etc.), usa `ACK.Data.register_property` o `ACK.Data.batch_register_properties` desde una función `register()`.

```python
from ...ackit import ACK
import bpy

# Definir propiedad con PropTyped (recomendado)
my_scene_prop = ACK.PropTyped.Float("Mi Propiedad", default=0.5).min(0.0).max(1.0)

def register():
    # Registrar una propiedad en la clase Scene
    ACK.Data.register_property(
        bpy_type=bpy.types.Scene, 
        property_idname="mi_propiedad_ack", # Nombre único para la propiedad
        property=my_scene_prop, # Pasar el descriptor PropTyped
        remove_on_unregister=True # Buena práctica
    )
    
    # Ejemplo con batch y Prop (menos común)
    ACK.Data.batch_register_properties(
        bpy.types.Object, 
        remove_on_unregister=True,
        mi_objeto_int=ACK.Prop.INT(name="Entero Objeto"),
        mi_objeto_bool=ACK.Prop.BOOL(name="Booleano Objeto")
    )

def unregister():
    # La desregistro es automático si remove_on_unregister=True
    pass
```

## Orden de Registro

ACKit ordena automáticamente las clases a registrar en función de sus dependencias (e.g., `PropertyGroup` antes que `PointerProperty` que lo usa). Sin embargo, el registro manual con `register_property` ocurre **después** del registro automático de clases, dentro de las funciones `register()` de tus módulos.

## Persistencia de Datos entre Sesiones

Para que los datos persistan entre sesiones, **debes** registrarlos en tipos de datos de Blender que se guarden en el archivo `.blend`, como `bpy.types.Scene`, `bpy.types.Object`, `bpy.types.Material`, etc., usando `ACK.Data.register_property` como se mostró anteriormente.

Las propiedades definidas en `AddonPreferences` persisten en la configuración de usuario de Blender, no en el archivo `.blend`.

## Ejemplo Completo de Registro

```python
# __init__.py principal
from .ackit import AddonLoader

AddonLoader.init_modules()

def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()
```

```python
# src/props/prefs.py
from ...ackit import ACK

# Se registra automáticamente por herencia
class MyAddonPreferences(ACK.Data.AddonPreferences):
    bl_idname = __package__.split('.')[0] # Necesario para Prefs
    
    debug_mode: ACK.PropTyped.Bool("Modo Debug", default=False)
    theme: ACK.PropTyped.Enum("Tema", items=[
        ("LIGHT", "Claro", "Tema claro"),
        ("DARK", "Oscuro", "Tema oscuro")
    ]).default("LIGHT")
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "debug_mode")
        layout.prop(self, "theme")
```

```python
# src/props/scene_props.py
from ...ackit import ACK
import bpy

# Definir el grupo de propiedades (se registra automáticamente)
class MySceneSettings(ACK.Data.PropertyGroup):
    mi_addon_enabled: ACK.PropTyped.Bool("Habilitado", default=True)
    mi_addon_valor: ACK.PropTyped.Float("Valor", default=0.5)

# Registrar una instancia de este grupo en la Escena
def register():
    bpy.types.Scene.my_scene_settings = bpy.props.PointerProperty(type=MySceneSettings)

def unregister():
    del bpy.types.Scene.my_scene_settings
```

## Consideraciones para Blender 4.0+

Con la introducción de Extension Platform en Blender 4.0, es importante tener en cuenta:

1.  La organización del código para compatibilidad con el sistema de extensiones.
2.  La definición de un archivo `blender_manifest.toml` apropiado.
3.  La declaración de permisos requeridos por tu addon.

ACKit se adapta automáticamente a estos cambios, pero debes asegurarte de configurar correctamente el archivo de manifiesto. Consulta la [guía de Extension Platform](extension-platform.md) para más detalles. 