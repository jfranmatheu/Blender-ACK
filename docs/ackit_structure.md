# Estructura de ACKit

## Organización del Módulo

ACKit está organizado en varios submódulos especializados, cada uno con una función específica dentro del framework:

```
ackit/
├── __init__.py               # Punto de entrada principal y exportación de clases
├── _ack.py                   # Clase principal ACK que unifica la API
├── globals.py                # Variables y constantes globales
├── auto_code/                # Generación automática de código
├── registry/                 # Sistema de registro para clases de Blender
│   ├── __init__.py           # Exporta AddonLoader y AutoLoad
│   ├── addon_loader.py       # Implementación del sistema de carga moderno
│   ├── auto_load.py          # Sistema de carga legacy
│   ├── btypes.py             # Gestión de tipos de Blender
│   ├── polling.py            # Sistema de polling para UI
│   ├── metadata.py           # Gestión de metadatos
│   ├── utils.py              # Utilidades para el sistema de registro
│   ├── reg_types/            # Wrappers tipados para clases de Blender
│   ├── reg_deco/             # Decoradores para registro
│   ├── props/                # Sistema de propiedades
│   ├── flags/                # Flags y opciones para clases
│   └── reg_helpers/          # Funciones de ayuda para registro
├── types/                    # Definiciones de tipos personalizados
│   ├── __init__.py
│   ├── nodes/                # Tipos específicos para nodos
│   └── ops/                  # Tipos específicos para operadores
├── utils/                    # Utilidades generales
├── debug/                    # Herramientas de depuración
├── enums/                    # Enumeraciones y constantes
└── decorators/               # Decoradores generales
```

## Componentes Principales

### 1. ACK - Clase Central

La clase `ACK` en `_ack.py` es el punto de entrada principal para acceder a la funcionalidad de ACKit. Proporciona una API unificada a través de clases anidadas:

- `ACK.Register`: Funciones y clases para registro
- `ACK.Types`: Tipos personalizados
- `ACK.Returns`: Valores de retorno para operadores
- `ACK.Props`: Tipos de propiedades
- `ACK.Flags`: Opciones y flags para clases
- `ACK.Metadata`: Gestión de metadatos
- `ACK.Poll`: Sistema de polling para UI

### 2. Sistema de Registro

El sistema de registro es uno de los componentes más importantes de ACKit, y consta de:

#### AddonLoader

Clase principal para la carga y registro de módulos, con un ciclo de vida bien definido:

1. `init_modules()`: Inicialización de módulos
2. `register_modules()`: Registro de módulos
3. `unregister_modules()`: Desregistro de módulos

#### BTypes

Enumeración que define todos los tipos soportados por Blender que pueden ser registrados, como:

- `Operator`
- `Panel`
- `Menu`
- `PropertyGroup`
- `Node`
- etc.

Cada tipo tiene métodos para:
- Añadir clases (`add_class`)
- Obtener clases (`get_classes`)
- Ordenar clases (`sort_classes`)
- Registrar y desregistrar clases (`register_classes`, `unregister_classes`)

### 3. Sistema de Propiedades

ACKit proporciona wrappers tipados para las propiedades de Blender, facilitando su definición y uso:

- `ACK.Props`: Tipos básicos (Int, Float, String, etc.)
- `ACK.PropsWrapped`: Versiones con tipado para mejor autocompletado e información en IDEs

### 4. Gestión Global

La clase `GLOBALS` proporciona acceso centralizado a información importante:

- Información de Blender (`BLENDER_VERSION`, `IN_BACKGROUND`)
- Información del addon (`ADDON_MODULE`, `ADDON_MODULE_NAME`)
- Rutas importantes (`ADDON_SOURCE_PATH`, `ICONS_PATH`)
- Métodos de utilidad (`check_in_development`, `get_value`, `set_value`)

## Diagrama Conceptual de Clases

```
+------------------------+       +------------------------+
|          ACK           |<------|      AddonLoader      |
|------------------------|       |------------------------|
| + Register             |       | + init_modules()       |
| + Types                |       | + register_modules()   |
| + Returns              |       | + unregister_modules() |
| + Props                |       +------------------------+
| + Flags                |
| + Metadata             |       +------------------------+
| + Poll                 |<------|         BTypes         |
+------------------------+       |------------------------|
                                 | + Operator             |
+------------------------+       | + Panel                |
|        GLOBALS         |       | + Menu                 |
|------------------------|       | + PropertyGroup        |
| + ADDON_MODULE         |       | + add_class()          |
| + BLENDER_VERSION      |       | + register_classes()   |
| + ADDON_SOURCE_PATH    |       +------------------------+
| + check_in_development |
+------------------------+       +------------------------+
                                 |     PropertyTypes      |
                                 |------------------------|
                                 | + Int                  |
                                 | + Float                |
                                 | + String               |
                                 | + Collection           |
                                 +------------------------+
```

## Flujo de Ejecución

El flujo típico de ejecución cuando se utiliza ACKit en un addon es:

1. **Inicialización**:
   - Se importa `AddonLoader` en el `__init__.py` principal
   - Se llama a `AddonLoader.init_modules()` para descubrir todos los módulos
   - Se ejecutan los callbacks `init` y `late_init` en todos los módulos

2. **Registro**:
   - Cuando Blender carga el addon, se llama a `AddonLoader.register_modules()`
   - Las clases de Blender son registradas a través del sistema de BTypes
   - Se ejecutan los callbacks `register` y `late_register` en todos los módulos

3. **Uso del Addon**:
   - Las clases registradas (operadores, paneles, etc.) están disponibles para el usuario
   - Las propiedades definidas están accesibles a través de la API de Blender

4. **Desregistro**:
   - Cuando Blender desactiva el addon, se llama a `AddonLoader.unregister_modules()`
   - Las clases de Blender son desregistradas
   - Se ejecutan los callbacks `unregister` y `late_unregister` en todos los módulos

## Extensibilidad

ACKit está diseñado para ser extensible, permitiendo a los desarrolladores:

1. **Añadir nuevos tipos de clases**: Extendiendo la enumeración `BTypes`
2. **Personalizar el proceso de registro**: Implementando callbacks en sus módulos
3. **Agregar funcionalidad personalizada**: Extendiendo la clase `ACK` con nuevos métodos y propiedades

Esta estructura modular y extensible hace que ACKit sea una base sólida para el desarrollo de addons complejos para Blender. 