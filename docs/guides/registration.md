# Sistema de Registro en ACKit

El sistema de registro es uno de los componentes centrales de ACKit. Este sistema gestiona automáticamente el registro y desregistro de clases de Blender, eliminando gran parte del código boilerplate típico en el desarrollo de addons.

## Conceptos Básicos

### AddonLoader

`AddonLoader` es la clase principal que gestiona el ciclo de vida completo del addon:

```python
from .ackit import AddonLoader

# Inicialización
AddonLoader.init_modules()

# Registro
def register():
    AddonLoader.register_modules()

# Desregistro
def unregister():
    AddonLoader.unregister_modules()
```

### BTypes

`BTypes` es una enumeración que define los tipos de clases de Blender que pueden ser registrados:

- `Operator`: Operadores estándar
- `Macro`: Operadores macro
- `Panel`: Paneles de UI
- `Menu`: Menús
- `UIList`: Listas personalizadas
- `PropertyGroup`: Grupos de propiedades
- `AddonPreferences`: Preferencias del addon
- `NodeTree`: Árboles de nodos
- `NodeSocket`: Sockets de nodos
- `Node`: Nodos
- `Gizmo`: Gizmos
- `GizmoGroup`: Grupos de gizmos

## Ciclo de Vida de un Addon

ACKit define un ciclo de vida claro para los addons con callbacks específicos:

1. **Inicialización**:
   - `init`: Se llama durante la fase de inicialización
   - `late_init`: Se llama después de la inicialización principal

2. **Registro**:
   - `register`: Se llama durante la fase de registro
   - `late_register`: Se llama después del registro principal

3. **Desregistro**:
   - `unregister`: Se llama durante la fase de desregistro
   - `late_unregister`: Se llama después del desregistro principal

Puedes definir estos callbacks en cualquier módulo de tu addon:

```python
# En cualquier módulo de tu addon
def init():
    print("Inicializando mi módulo")

def register():
    print("Registrando mi módulo")

def late_register():
    print("Registro tardío de mi módulo")

def unregister():
    print("Desregistrando mi módulo")
```

## Modos de Registro

ACKit proporciona diferentes enfoques para registrar clases:

### 1. Registro Automático

El sistema detecta y registra automáticamente todas las clases que heredan de las clases base de ACKit:

```python
from ...ackit import ACK

# Esta clase se registrará automáticamente
class MyOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.my_operator"
    bl_label = "Mi Operador"
    
    def execute(self, context):
        return {'FINISHED'}
```

### 2. Registro a partir de Funciones

Para componentes simples como paneles o menús, puedes utilizar decoradores para crear clases a partir de funciones:

```python
from ...ackit import ACK

# Esto crea un panel registrado automáticamente
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Tab")
def my_panel(context, layout):
    layout.label(text="Mi Panel")
    layout.operator("object.my_operator")
```

### 3. Registro Manual de Propiedades

Para registrar propiedades en clases existentes (como Scene, Object, etc.), utiliza los métodos de registro de propiedades:

```python
from ...ackit import ACK
import bpy

def register():
    # Registrar una propiedad en la clase Scene
    ACK.Register.Property(
        bpy.types.Scene, 
        "mi_propiedad", 
        ACK.PropsWrapped.Float("Mi Propiedad").default(0.0).min(0.0).max(1.0)
    )
```

## Orden de Registro

ACKit ordena automáticamente las clases a registrar en función de sus dependencias. Esto significa que puedes definir clases en cualquier orden, y ACKit se asegurará de que:

1. Los `PropertyGroup` se registren antes de las clases que los utilizan
2. Las clases padre se registren antes que las clases hijas
3. Las clases con dependencias indirectas se registren en el orden correcto

## Persistencia de Datos entre Sesiones

Para que los datos persistan entre sesiones, debes:

1. Registrar propiedades en tipos de Blender como Scene, Object, Mesh, etc.
2. Usar correctamente el sistema de preferencias de addons

Ejemplo de registro de propiedades persistentes:

```python
from ...ackit import ACK
import bpy

def register():
    # Registrar propiedades en la escena (persistentes con el archivo .blend)
    ACK.Register.Properties(
        bpy.types.Scene,
        {
            "mi_entero": ACK.PropsWrapped.Int("Mi Entero").default(5),
            "mi_texto": ACK.PropsWrapped.String("Mi Texto").default("Valor predeterminado")
        }
    )
```

## Ejemplo Completo de Registro

Este es un ejemplo más completo que muestra las diferentes partes del sistema de registro:

```python
# __init__.py principal
from .ackit import AddonLoader, AutoCode

# Inicializar ACKit
AddonLoader.init_modules(
    auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}
)

def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()
```

```python
# src/props/preferences.py
from ...ackit import ACK

class AddonPreferences(ACK.Register.Types.Data.AddonPreferences):
    """Preferencias del addon."""
    
    debug_mode = ACK.PropsWrapped.Bool("Modo Debug").default(False)
    theme = ACK.PropsWrapped.Enum("Tema").items(
        ("LIGHT", "Claro", "Tema claro"),
        ("DARK", "Oscuro", "Tema oscuro")
    ).default("LIGHT")
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "debug_mode")
        layout.prop(self, "theme")
```

```python
# src/props/scene_props.py
from ...ackit import ACK
import bpy

def register():
    # Registrar propiedades en la escena
    ACK.Register.Properties(
        bpy.types.Scene,
        {
            "mi_addon_enabled": ACK.PropsWrapped.Bool("Habilitado").default(True),
            "mi_addon_valor": ACK.PropsWrapped.Float("Valor").default(0.5)
        }
    )

def unregister():
    # ACKit elimina automáticamente las propiedades registradas
    pass
```

## Consideraciones para Blender 4.0+

Con la introducción de Extension Platform en Blender 4.0, es importante tener en cuenta:

1. La organización del código para compatibilidad con el sistema de extensiones
2. La definición de un archivo `blender_manifest.toml` apropiado
3. La declaración de permisos requeridos por tu addon

ACKit se adapta automáticamente a estos cambios, pero debes asegurarte de configurar correctamente el archivo de manifiesto. Consulta la [guía de Extension Platform](extension-platform.md) para más detalles. 