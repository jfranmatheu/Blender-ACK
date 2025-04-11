# Guía Rápida de ACKit

Esta guía está diseñada para ayudarte a comenzar a usar ACKit rápidamente en tus addons para Blender.

## Instalación Rápida

1. **Añade ACKit a tu proyecto**:
   ```bash
   # Como submódulo de Git (recomendado)
   git submodule add https://github.com/jfranmatheu/Blender-ACKit.git ackit
   
   # O descárgalo manualmente y colócalo en una carpeta llamada 'ackit'
   ```

2. **Configura tu `__init__.py`**:
   ```python
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

## Estructura Mínima Recomendada

```
mi_addon/
├── __init__.py                # Punto de entrada principal
├── blender_manifest.toml      # Para Blender 4.0+
├── ackit/                     # Submódulo ACKit
└── src/                       # Código fuente del addon
    ├── __init__.py            # Puede estar vacío o importar/registrar
    ├── ops/                   # Operadores
    ├── ui/                    # Interfaces de usuario
    ├── props/                 # Grupos de Propiedades
    ├── node_editor/           # Nodos y Árboles (si aplica)
    └── ...                    # Otros módulos (handlers, etc.)
```

## Ejemplos Rápidos

### 1. Crear un Operador Simple

```python
# src/ops/simple.py
from ...ackit import ACK
from ...ackit.enums.operator import OpsReturn

class SimpleOperator(ACK.Ops.Generic):
    bl_idname = "object.simple_operator"
    bl_label = "Operador Simple"
    
    def execute(self, context):
        self.report({'INFO'}, "¡Operador ejecutado!")
        return OpsReturn.FINISH
```

### 2. Crear un Panel UI

```python
# src/ui/panel.py
from ...ackit import ACK

# Usar creador desde función
@ACK.UI.create_panel_from_func.VIEW_3D(tab="Mi Addon")
def simple_panel(context, layout):
    layout.label(text="Panel de Mi Addon")
    # Llamar operador por su bl_idname
    layout.operator('object.simple_operator') 
```

### 3. Definir Propiedades

```python
# src/props/settings.py
from ...ackit import ACK
import bpy

class MyAddonSettings(ACK.Data.PropertyGroup):
    # Usar PropTyped para definición
    enabled: ACK.PropTyped.Bool("Habilitado").default(True)
    value: ACK.PropTyped.Float("Valor").default(0.5).min(0.0).max(1.0)
    
    # Registra las propiedades en la escena
    # Esto ahora se haría en la función register() del __init__.py principal
    # o en una función register() dentro de este módulo si AddonLoader la detecta.

# Ejemplo de cómo registrarlo en __init__.py o un módulo src/__init__.py
# def register():
#     # ... otro código de registro ...
#     bpy.types.Scene.my_addon_settings = bpy.props.PointerProperty(type=MyAddonSettings)

# def unregister():
#     # ... otro código de desregistro ...
#     del bpy.types.Scene.my_addon_settings
```

## Características Principales a Explorar

- **Fachada `ACK`**: Punto de entrada unificado (`ACK.Ops`, `ACK.UI`, `ACK.NE`, `ACK.Data`, `ACK.App`, `ACK.Poll`).
- **Propiedades Tipadas**: Usa `ACK.PropTyped` para propiedades con tipado fuerte y API fluida.
- **Decoradores**: Simplifica el código con decoradores como `@ACK.Poll.ACTIVE_OBJECT.MESH`, `@ACK.Ops.add_flag.UNDO`, `@ACK.NE.add_node_to_category()`, etc.
- **Sistema de Registro Automático**: `AddonLoader` registra clases y llama funciones `register`/`unregister` en módulos.
- **Auto-Generación de Código**: Permite generar wrappers de operadores, iconos y tipos (`ackit.AutoCode`).

## Siguientes Pasos

Para profundizar en ACKit, consulta:

- [Guía Completa de Inicio](getting-started.md)
- [Sistema de Registro](registration.md)
- [Tutoriales Prácticos](../tutorials/basic-operator.md)
- [Referencia de API](../api/ack.md)
