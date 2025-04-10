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
   bl_info = {
       "name": "Mi Addon",
       "author": "Tu Nombre",
       "version": (1, 0, 0),
       "blender": (4, 0, 0),
       "description": "Descripción de mi addon",
       "category": "3D View",
   }
   
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
    ├── ops/                   # Operadores
    ├── ui/                    # Interfaces de usuario
    └── props/                 # Propiedades
```

## Ejemplos Rápidos

### 1. Crear un Operador Simple

```python
# src/ops/simple.py
from ...ackit import ACK

class SimpleOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "object.simple_operator"
    bl_label = "Operador Simple"
    
    def execute(self, context):
        self.report({'INFO'}, "¡Operador ejecutado!")
        return ACK.Returns.Operator.FINISHED
```

### 2. Crear un Panel UI

```python
# src/ui/panel.py
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def simple_panel(context, layout):
    layout.label(text="Panel de Mi Addon")
    layout.operator('object.simple_operator')
```

### 3. Definir Propiedades

```python
# src/props/settings.py
from ...ackit import ACK

class MyAddonSettings(ACK.Register.Types.Data.PropertyGroup):
    enabled = ACK.PropsWrapped.Bool("Habilitado").default(True)
    value = ACK.PropsWrapped.Float("Valor").default(0.5).min(0.0).max(1.0)
    
    # Registra las propiedades en la escena
    @classmethod
    def register(cls):
        import bpy
        bpy.types.Scene.my_addon = ACK.Register.Property(
            bpy.props.PointerProperty(type=cls)
        )
    
    @classmethod
    def unregister(cls):
        import bpy
        del bpy.types.Scene.my_addon
```

## Características Principales a Explorar

- **Sistema de Registro Automático**: ACKit registra automáticamente todas las clases en los módulos detectados.
- **Propiedades Tipadas**: Usa `ACK.PropsWrapped` para propiedades con tipado fuerte y API fluida.
- **Decoradores**: Simplifica el código con decoradores como `@ACK.Poll.ACTIVE_OBJECT.MESH`.
- **Auto-Generación de Código**: Permite generar wrappers de operadores, iconos y tipos.

## Siguientes Pasos

Para profundizar en ACKit, consulta:

- [Guía Completa de Inicio](getting-started.md)
- [Sistema de Registro](registration.md)
- [Tutoriales Prácticos](../tutorials/basic-operator.md)
- [Referencia de API](../api/ack.md)
