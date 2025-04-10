# Estructura Recomendada para Addons con ACKit

Esta guía describe la estructura de directorios y organización de archivos recomendada para addons desarrollados con ACKit.

## Estructura Base

Una estructura bien organizada facilita el mantenimiento y la extensibilidad de tu addon. Aquí está la estructura básica recomendada:

```
mi_addon/
├── __init__.py                # Punto de entrada principal
├── blender_manifest.toml      # Para Blender 4.0+ (Extension Platform)
├── ackit/                     # Submódulo ACKit
│
├── src/                       # Código fuente del addon
│   ├── ops/                   # Operadores
│   ├── ui/                    # Interfaces de usuario
│   ├── props/                 # Propiedades
│   ├── utils/                 # Utilidades
│   ├── core/                  # Lógica central
│   └── data/                  # Definiciones de datos
│
├── resources/                 # Recursos externos
│   ├── icons/                 # Iconos
│   ├── presets/               # Presets
│   └── templates/             # Plantillas
│
└── docs/                      # Documentación interna
```

## Descripción de Cada Componente

### Archivos de Configuración

- **__init__.py**: Punto de entrada del addon que contiene las funciones `register()` y `unregister()` y la inicialización de ACKit.
- **blender_manifest.toml**: Archivo de manifiesto para Extension Platform (Blender 4.0+).

### Módulos Principales

- **src/ops/**: Contiene todos los operadores del addon.
- **src/ui/**: Contiene todo lo relacionado con la interfaz de usuario (paneles, menús, etc).
- **src/props/**: Contiene definiciones de propiedades y grupos de propiedades.
- **src/utils/**: Utilidades generales y funciones helper.
- **src/core/**: Lógica principal y algoritmos del addon.
- **src/data/**: Definiciones de estructuras de datos y modelos.

### Recursos

- **resources/icons/**: Iconos utilizados en el addon.
- **resources/presets/**: Presets predefinidos para funcionalidades del addon.
- **resources/templates/**: Plantillas para generación de contenido.

## Implementación de Ejemplo

### __init__.py

```python
bl_info = {
    "name": "Mi Addon",
    "author": "Tu Nombre",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Mi Addon",
    "description": "Descripción de mi addon",
    "category": "3D View",
}

from .ackit import AddonLoader, AutoCode

# Inicializar ACKit
AddonLoader.init_modules(
    auto_code={
        AutoCode.OPS,      # Genera wrappers para operadores
        AutoCode.ICONS,    # Genera constantes para iconos
        AutoCode.TYPES     # Genera tipos personalizados
    }
)

def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()

if __name__ == "__main__":
    register()
```

### Estructura de Submódulos

#### src/ops/

```
src/ops/
├── __init__.py           # Exporta los operadores principales
├── object_ops.py         # Operadores relacionados con objetos
├── mesh_ops.py           # Operadores relacionados con mallas
└── advanced/            # Operadores más complejos
    ├── __init__.py
    └── complex_op.py
```

Ejemplo de `src/ops/object_ops.py`:

```python
from ...ackit import ACK

class SelectRelatedObjectsOperator(ACK.Register.Types.Ops.Generic):
    bl_idname = "miaddon.select_related"
    bl_label = "Seleccionar Relacionados"
    bl_description = "Selecciona objetos relacionados por nombre"
    
    threshold = ACK.PropsWrapped.Float("Umbral").default(0.8).min(0.0).max(1.0)
    
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

#### src/ui/

```
src/ui/
├── __init__.py           # Exporta los componentes de UI principales
├── panels.py             # Paneles principales
├── menus.py              # Menús
├── popovers.py           # Popovers
└── components/          # Componentes de UI reutilizables
    ├── __init__.py
    └── custom_components.py
```

Ejemplo de `src/ui/panels.py`:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon", order=1)
def main_panel(context, layout):
    layout.label(text="Herramientas Principales")
    layout.operator("miaddon.select_related")
    
    # Sección específica para objetos mesh
    if context.object and context.object.type == 'MESH':
        box = layout.box()
        box.label(text="Herramientas de Malla")
        box.operator("miaddon.mesh_tool_1")
        box.operator("miaddon.mesh_tool_2")
```

#### src/props/

```
src/props/
├── __init__.py           # Exporta las propiedades principales
├── settings.py           # Configuraciones del addon
└── object_props.py       # Propiedades relacionadas con objetos
```

Ejemplo de `src/props/settings.py`:

```python
from ...ackit import ACK

class MyAddonSettings(ACK.Register.Types.Data.PropertyGroup):
    theme = ACK.PropsWrapped.Enum("Tema").items([
        ('LIGHT', "Claro", "Tema claro"),
        ('DARK', "Oscuro", "Tema oscuro"),
        ('CUSTOM', "Personalizado", "Tema personalizado")
    ]).default('LIGHT')
    
    detail_level = ACK.PropsWrapped.Int("Nivel de Detalle").default(3).min(1).max(5)
    
    @classmethod
    def register(cls):
        import bpy
        bpy.types.Scene.miaddon = ACK.Register.Property(
            bpy.props.PointerProperty(type=cls)
        )
    
    @classmethod
    def unregister(cls):
        import bpy
        del bpy.types.Scene.miaddon
```

## Subdivisión para Addons Grandes

Para addons más grandes, considera organizarlos en "módulos funcionales":

```
mi_addon/
├── __init__.py
├── blender_manifest.toml
├── ackit/
│
└── modules/
    ├── __init__.py             # Integración de todos los módulos
    │
    ├── module_1/               # Módulo funcional 1
    │   ├── __init__.py
    │   ├── ops/
    │   ├── ui/
    │   └── props/
    │
    ├── module_2/               # Módulo funcional 2
    │   ├── __init__.py
    │   ├── ops/
    │   ├── ui/
    │   └── props/
    │
    └── core/                   # Funcionalidad compartida entre módulos
        ├── __init__.py
        ├── utils/
        └── data/
```

Con esta estructura, cada módulo funcional es independiente pero puede acceder a funcionalidades compartidas en el módulo `core`.

## Organización de Recursos

### Iconos

Para los iconos, se recomienda seguir esta estructura:

```
resources/icons/
├── 16/                  # Iconos de 16x16 píxeles
├── 32/                  # Iconos de 32x32 píxeles
└── preview/             # Imágenes de vista previa
```

Ejemplo de carga de iconos con ACKit:

```python
from ...ackit.utils import previews

# Cargar iconos
icons = previews.create_preview_collection()
icons.load("MI_ICONO", "resources/icons/32/mi_icono.png")

# Uso en UI
def draw(self, context):
    layout = self.layout
    layout.label(text="Mi Etiqueta", icon_value=icons["MI_ICONO"].icon_id)
```

### Presets

Para los presets, es útil organizarlos por categoría:

```
resources/presets/
├── materials/           # Presets de materiales
├── node_groups/         # Presets de grupos de nodos
└── configurations/      # Presets de configuración
```

## Consejos para una Buena Estructura

1. **Separación de Responsabilidades**: Cada módulo debe tener una única responsabilidad claramente definida.
2. **Consistencia en Importaciones**: Mantén un estilo consistente para las importaciones entre módulos.
3. **Minimalismo en `__init__.py`**: Los archivos `__init__.py` deben ser principalmente para exportación, no para implementación.
4. **Nombres Claros**: Usa nombres de archivo y carpeta descriptivos que indiquen claramente su propósito.
5. **Evita la Circularidad**: Diseña tus módulos para evitar importaciones circulares.

## Acceso a Recursos

ACKit proporciona utilidades para acceder fácilmente a los recursos de tu addon:

```python
from ...ackit.utils import fs

# Obtener ruta absoluta a un recurso
icon_path = fs.get_addon_path("resources", "icons", "32", "mi_icono.png")
template_path = fs.get_addon_path("resources", "templates", "base_template.blend")

# Leer un archivo de texto
with open(fs.get_addon_path("resources", "templates", "template.txt"), 'r') as f:
    template_content = f.read()
```

## Conclusión

Una estructura bien organizada facilita el mantenimiento, la colaboración y la escalabilidad de tu addon. La estructura recomendada por ACKit no es obligatoria, pero proporciona un buen punto de partida para organizar tu código de manera efectiva. 