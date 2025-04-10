# Primeros Pasos con ACKit

Esta guía te ayudará a comenzar a utilizar ACKit en tus proyectos de addons para Blender.

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- Blender 4.0 o superior
- Conocimientos básicos de Python
- Conocimientos básicos de desarrollo de addons para Blender

## Instalación

ACKit está diseñado para ser integrado como un submódulo dentro de tu propio addon. Existen varias formas de incluirlo:

### 1. Usando Git Submodules (Recomendado)

Si utilizas Git para gestionar tu proyecto, puedes incluir ACKit como un submódulo:

```bash
# En la raíz de tu proyecto de addon
git submodule add https://github.com/jfranmatheu/Blender-ACKit.git ackit
```

### 2. Descarga Manual

Alternativamente, puedes descargar ACKit directamente y colocarlo en un directorio `ackit` dentro de tu proyecto:

1. Descarga el repositorio desde [GitHub](https://github.com/jfranmatheu/Blender-ACKit)
2. Descomprime el archivo
3. Copia el contenido a una carpeta llamada `ackit` en la raíz de tu proyecto

## Estructura de Directorios Recomendada

Recomendamos organizar tu addon con una estructura similar a la siguiente:

```
mi_addon/
├── __init__.py                # Punto de entrada principal
├── blender_manifest.toml      # Manifiesto para Extension Platform (Blender 4.0+)
├── ackit/                     # Módulo ACKit (submódulo)
└── src/                       # Código fuente del addon
    ├── ops/                   # Operadores
    ├── ui/                    # Interfaces de usuario
    ├── props/                 # Propiedades
    └── utils/                 # Utilidades
```

## Configuración Básica

Para empezar a utilizar ACKit, configura tu archivo `__init__.py` principal de la siguiente manera:

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

# Inicializar ACKit con opciones de generación automática de código
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
```

## Tu Primer Operador con ACKit

Crea un archivo `src/ops/simple.py` con el siguiente contenido:

```python
from ...ackit import ACK

@ACK.Poll.ACTIVE_OBJECT.ANY  # Solo disponible cuando hay un objeto activo
class SimpleOperator(ACK.Register.Types.Ops.Generic):
    # Definición de propiedades con tipado fuerte
    message = ACK.PropsWrapped.String("Mensaje").default("Hola desde ACKit")

    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}
```

## Tu Primer Panel con ACKit

Crea un archivo `src/ui/panel.py` con el siguiente contenido:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def simple_panel(context, layout):
    layout.label(text="Mi Primer Panel con ACKit")
    layout.operator('object.simple_operator')
```

## Probando Tu Addon

1. Instala tu addon en Blender usando el gestor de addons
2. Activa el addon
3. Abre la barra lateral en el Viewport 3D (tecla N)
4. Deberías ver una pestaña "Mi Addon" con tu panel y un botón para ejecutar el operador

## Siguientes Pasos

Ahora que ya tienes tu configuración básica funcionando, puedes explorar más características de ACKit:

- [Guía de Estructura de Addons](addon-structure.md)
- [Sistema de Registro](registration.md)
- [Creación de Operadores](../tutorials/basic-operator.md)
- [Creación de Interfaces de Usuario](../tutorials/ui-creation.md)
- [Sistema de Propiedades](../tutorials/properties.md)

## Solución de Problemas

### Problemas Comunes

- **Error "No module named 'ackit'"**: Asegúrate de que la carpeta `ackit` esté correctamente ubicada en la raíz de tu addon
- **Clases no se registran**: Verifica que estás utilizando las clases base de ACKit y que `AddonLoader.init_modules()` se llama antes de registrar

### Obteniendo Ayuda

Si encuentras problemas o tienes preguntas:

- Consulta la [documentación completa](../index.md)
- Revisa la sección de [FAQ](../reference/faq.md)
- Reporta problemas en el [repositorio de GitHub](https://github.com/jfranmatheu/Blender-ACKit/issues) 