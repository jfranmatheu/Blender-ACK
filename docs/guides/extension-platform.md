# Integración con Extension Platform de Blender 4.0+

Este documento explica cómo utilizar ACKit con el nuevo sistema de Extension Platform introducido en Blender 4.0.

## Introducción a Extension Platform

A partir de Blender 4.0, se ha introducido un nuevo sistema para la gestión de addons conocido como "Extension Platform". Este sistema sustituye el antiguo mecanismo basado en el diccionario `bl_info` dentro del archivo `__init__.py` por un archivo de manifiesto en formato TOML (`blender_manifest.toml`).

ACKit está diseñado para ser totalmente compatible con este nuevo sistema, permitiendo una transición suave desde addons tradicionales hacia extensiones modernas.

## Archivo de Manifiesto (blender_manifest.toml)

El primer paso para utilizar ACKit con Extension Platform es crear un archivo `blender_manifest.toml` en la raíz de tu addon:

```toml
# blender_manifest.toml
id = "miaddon"
version = "1.0.0"
name = "Mi Addon ACKit"
tagline = "Una extensión potente creada con ACKit"
maintainer = "Tu Nombre <tucorreo@ejemplo.com>"
blender_version_min = "4.0.0"
category = "3D View"

# Opciones avanzadas
permissions = ["filesystem", "network"]
deps = []
```

### Opciones del Manifiesto

Las principales opciones que puedes configurar son:

- `id`: Identificador único para tu extensión (requerido)
- `version`: Versión de tu extensión (requerido)
- `name`: Nombre visible de tu extensión (requerido)
- `tagline`: Descripción breve (requerido)
- `maintainer`: Información de contacto (requerido)
- `blender_version_min`: Versión mínima de Blender requerida (requerido)
- `category`: Categoría en la que aparecerá tu extensión
- `description`: Descripción detallada (opcional)
- `permissions`: Permisos requeridos (opcional)
- `deps`: Dependencias de otras extensiones (opcional)

## Estructura de Archivos para Extension Platform

La estructura de archivos recomendada para un addon ACKit compatible con Extension Platform es:

```
mi_addon/
├── blender_manifest.toml       # Manifiesto de extensión
├── __init__.py                 # Punto de entrada del addon
├── ackit/                      # Submódulo ACKit
└── src/                        # Código fuente del addon
    ├── ops/                    # Operadores
    ├── ui/                     # Interfaces de usuario
    └── props/                  # Propiedades
```

## Configuración del __init__.py

El archivo `__init__.py` se simplifica para Extension Platform, ya que la información del addon ahora está en el manifiesto:

```python
# __init__.py

from .ackit import AddonLoader, AutoCode

# Inicializar ACKit
AddonLoader.init_modules(
    auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}
)

# Funciones de registro obligatorias
def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()
```

## Detección Automática de Versión

ACKit detecta automáticamente si tu addon está en ejecución bajo Blender 4.0+ con Extension Platform y ajusta su comportamiento en consecuencia:

```python
# Ejemplo de código interno de ACKit (globals.py)
BLENDER_VERSION = get_blender_version()
USING_EXTENSION_PLATFORM = BLENDER_VERSION >= (4, 0, 0) and os.path.exists(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "blender_manifest.toml")
)

# Ajustes basados en la detección
ADDON_MODULE_SHORT = __main_package__.split('.')[-1] if USING_EXTENSION_PLATFORM else __main_package__
```

## Permisos en Extension Platform

Extension Platform introduce un sistema de permisos para controlar el acceso de las extensiones a funcionalidades sensibles. ACKit facilita la comprobación y solicitud de permisos:

```python
from ...ackit.utils.permissions import has_permission, request_permission

def my_function():
    # Comprobar si tenemos permiso para acceder a la red
    if has_permission('network'):
        # Realizar operaciones de red
        import requests
        response = requests.get('https://api.example.com/data')
    else:
        # Solicitar permiso
        if request_permission('network', 'Mi Addon necesita acceder a internet para descargar recursos'):
            # Permiso concedido, intentar de nuevo
            my_function()
        else:
            # Permiso denegado
            print("No se pudo completar la operación, permiso denegado")
```

## Migración de Addons Tradicionales a Extension Platform

Para migrar un addon existente que usa ACKit a Extension Platform:

1. **Crea el archivo de manifiesto**: Crea un archivo `blender_manifest.toml` en la raíz de tu addon.

2. **Transfiere la información**: Mueve la información de `bl_info` al manifiesto:
   ```python
   # Antiguo __init__.py
   bl_info = {
       "name": "Mi Addon",
       "author": "Tu Nombre",
       "version": (1, 0, 0),
       "blender": (3, 0, 0),
       "description": "Descripción del addon",
       "category": "3D View",
   }
   ```
   
   Se convierte en:
   ```toml
   # Nuevo blender_manifest.toml
   id = "miaddon"
   version = "1.0.0"
   name = "Mi Addon"
   tagline = "Descripción del addon"
   maintainer = "Tu Nombre"
   blender_version_min = "3.0.0"
   ```

3. **Adapta el código**: Asegúrate de que tu código sea compatible con Blender 4.0+.

4. **Comprueba los permisos**: Revisa si tu addon necesita permisos específicos y añádelos al manifiesto.

## Verificación de Compatibilidad

ACKit proporciona una función de verificación para comprobar si tu addon es compatible con Extension Platform:

```python
from ...ackit.utils.extension_platform import verify_compatibility

def register():
    # Verificar compatibilidad con Extension Platform
    issues = verify_compatibility()
    if issues:
        print("Problemas de compatibilidad con Extension Platform detectados:")
        for issue in issues:
            print(f"- {issue}")
    
    # Continuar con el registro si no hay problemas críticos
    AddonLoader.register_modules()
```

## Consejos para Extension Platform

1. **ID único**: Asegúrate de que el `id` en tu manifiesto sea único y descriptivo.
2. **Versionado semántico**: Usa versionado semántico (MAJOR.MINOR.PATCH) para tu extensión.
3. **Permisos mínimos**: Solicita solo los permisos que realmente necesitas.
4. **Documentación**: Proporciona una buena documentación en el campo `description`.
5. **Pruebas**: Prueba tu extensión en diferentes versiones de Blender 4.x.

## Recursos Adicionales

- [Documentación oficial de Extension Platform](https://docs.blender.org/manual/en/latest/extensions/index.html)
- [Especificación de blender_manifest.toml](https://docs.blender.org/manual/en/latest/extensions/manifest.html)
- [Guía de permisos en Extension Platform](https://docs.blender.org/manual/en/latest/extensions/permissions.html) 