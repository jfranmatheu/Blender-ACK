# Estructura de ACKit

## Organización del Módulo

ACKit está organizado en varios submódulos especializados, cada uno con una función específica dentro del framework. Esta estructura modular permite una mayor organización, mantenibilidad y extensibilidad.

```
ackit/
├── __init__.py               # Punto de entrada principal y exportación de clases
├── _ack.py                   # Clase principal ACK que unifica la API
├── globals.py                # Variables y constantes globales
│
├── auto_code/                # Generación automática de código
│   ├── __init__.py           # Define la clase AutoCode y sus métodos
│   ├── ops.py                # Generación de wrappers tipados para operadores
│   ├── icons.py              # Generación de constantes para iconos
│   └── types.py              # Generación de clases para tipos personalizados
│
├── registry/                 # Sistema de registro para clases de Blender
│   ├── __init__.py           # Exporta AddonLoader y AutoLoad
│   ├── addon_loader.py       # Sistema de carga y gestión de módulos moderno
│   ├── auto_load.py          # Sistema de carga legacy
│   ├── btypes.py             # Enumeration y gestión de tipos de Blender
│   ├── polling.py            # Sistema de polling para disponibilidad de UI/operadores
│   ├── metadata.py           # Gestión de metadatos para clases
│   ├── utils.py              # Utilidades para el sistema de registro
│   │
│   ├── reg_types/            # Wrappers tipados para clases de Blender
│   │   ├── __init__.py       # Exportación de tipos
│   │   ├── base_type.py      # Clase base para todos los tipos
│   │   ├── ops/              # Operadores
│   │   │   ├── __init__.py
│   │   │   ├── generic.py    # Operador genérico
│   │   │   ├── action.py     # Operador de acción
│   │   │   └── modal.py      # Operador modal
│   │   ├── ui/               # Elementos de interfaz de usuario
│   │   │   ├── __init__.py
│   │   │   ├── panel.py      # Paneles
│   │   │   ├── menu.py       # Menús
│   │   │   ├── pie_menu.py   # Menús circulares
│   │   │   ├── popover.py    # Popovers
│   │   │   └── ui_list.py    # Listas personalizadas
│   │   ├── data/             # Clases de datos
│   │   │   ├── __init__.py
│   │   │   ├── property_group.py # Grupos de propiedades
│   │   │   └── preferences.py    # Preferencias de addon
│   │   └── nodes/            # Sistema de nodos
│   │       ├── __init__.py
│   │       ├── node.py       # Nodos
│   │       ├── tree.py       # Árboles de nodos
│   │       ├── socket.py     # Sockets de nodos
│   │       ├── category.py   # Categorías de nodos
│   │       └── sockets/      # Implementaciones específicas de sockets
│   │           └── annotation.py # Anotaciones de sockets
│   │
│   ├── reg_deco/             # Decoradores para registro
│   │   ├── __init__.py       # Exportación de decoradores
│   │   ├── handlers.py       # Decoradores para manejadores de eventos
│   │   ├── keymaps.py        # Decoradores para mapas de teclas
│   │   ├── rna_sub.py        # Decoradores para suscripciones RNA
│   │   ├── timer.py          # Decoradores para temporizadores
│   │   ├── property_group.py # Decoradores para grupos de propiedades
│   │   └── ui/               # Decoradores específicos para UI
│   │       ├── __init__.py
│   │       ├── append.py     # Decoradores para extender paneles existentes
│   │       ├── fake_panels.py # Decoradores para paneles falsos
│   │       └── override.py   # Decoradores para sobreescribir comportamientos
│   │
│   ├── props/                # Sistema de propiedades
│   │   ├── __init__.py       # Exportación de tipos de propiedades
│   │   ├── property.py       # Definiciones base de propiedades
│   │   └── typed/            # Propiedades con tipado fuerte
│   │       ├── __init__.py
│   │       └── wrapped.py    # Wrappers para propiedades con tipado
│   │
│   ├── flags/                # Flags y opciones para clases
│   │   ├── __init__.py       # Exportación de flags
│   │   ├── operator.py       # Flags para operadores
│   │   ├── modal.py          # Flags para operadores modales
│   │   ├── panel_options.py  # Flags para paneles
│   │   └── node_category.py  # Decorador para categorías de nodos
│   │
│   └── reg_helpers/          # Funciones de ayuda para registro
│       ├── __init__.py
│       └── props.py          # Helpers para registro de propiedades
│
├── types/                    # Definiciones de tipos personalizados
│   ├── __init__.py
│   ├── nodes/                # Tipos específicos para nodos
│   └── ops/                  # Tipos específicos para operadores
│
├── utils/                    # Utilidades generales
│   ├── __init__.py           # Exportación de utilidades
│   ├── callback.py           # Clases para gestión de callbacks
│   ├── cursor.py             # Utilidades para el cursor
│   ├── fs.py                 # Utilidades de sistema de archivos
│   ├── previews.py           # Utilidades para previsualizaciones
│   ├── tool.py               # Utilidades para herramientas
│   ├── math/                 # Utilidades matemáticas
│   └── event/                # Utilidades para eventos
│
├── debug/                    # Herramientas de depuración
│   ├── __init__.py           # Exportación de funciones de debug
│   ├── output.py             # Funciones para salida de depuración
│   ├── logger.py             # Sistema de logging
│   └── profiler.py           # Herramientas de perfilado
│
├── enums/                    # Enumeraciones y constantes
│   ├── __init__.py           # Exportación de enumeraciones
│   ├── event.py              # Enumeraciones para eventos
│   └── operator.py           # Enumeraciones para operadores
│
└── decorators/               # Decoradores generales
```

## Componentes Principales

### 1. ACK - Clase Central

La clase `ACK` en `_ack.py` es el punto de entrada principal para acceder a la funcionalidad de ACKit. Proporciona una API unificada a través de clases anidadas:

- `ACK.Register`: Funciones y clases para registro
  - `ACK.Register.Types`: Wrappers tipados para clases de Blender
    - `ACK.Register.Types.Ops`: Tipos de operadores
    - `ACK.Register.Types.UI`: Tipos de UI
    - `ACK.Register.Types.Data`: Tipos de datos
    - `ACK.Register.Types.Nodes`: Tipos de nodos
  - `ACK.Register.FromFunction`: Métodos para crear clases a partir de funciones
  - `ACK.Register.Property`: Registro de propiedades
  - `ACK.Register.Properties`: Registro masivo de propiedades

- `ACK.Types`: Acceso a tipos personalizados
- `ACK.Returns`: Valores de retorno para operadores y submodos
- `ACK.Props`: Definiciones de propiedades sin tipado fuerte
- `ACK.PropsWrapped`: Definiciones de propiedades con tipado fuerte
- `ACK.Flags`: Flags y opciones para clases
  - `ACK.Flags.OPERATOR`: Flags para operadores
  - `ACK.Flags.MODAL`: Flags para operadores modales
  - `ACK.Flags.PANEL`: Opciones para paneles
  - `ACK.Flags.NODE_CATEGORY`: Decorador para categorías de nodos
- `ACK.Metadata`: Gestión de metadatos
- `ACK.Poll`: Sistema de polling para disponibilidad

### 2. Sistema de Registro

El sistema de registro es uno de los componentes más importantes de ACKit, y consta de:

#### AddonLoader

Clase principal para la carga y registro de módulos, con un ciclo de vida bien definido:

```python
AddonLoader.init_modules()      # Inicialización de módulos
AddonLoader.register_modules()   # Registro de módulos
AddonLoader.unregister_modules() # Desregistro de módulos
```

El `AddonLoader` gestiona:
- Descubrimiento de módulos del addon
- Recolección de callbacks de ciclo de vida
- Ejecución de callbacks en momentos específicos
- Limpieza de módulos
- Integración con AutoCode para generación de código

#### BTypes

Enumeración que define todos los tipos soportados por Blender que pueden ser registrados, como:

- `Operator`: Operadores estándar
- `Macro`: Operadores macro (secuencias de operadores)
- `Panel`: Paneles de interfaz de usuario
- `Menu`: Menús estándar
- `UIList`: Listas personalizadas
- `PropertyGroup`: Grupos de propiedades
- `AddonPreferences`: Preferencias de addon
- `NodeTree`: Árboles de nodos
- `NodeSocket`: Sockets de nodos
- `Node`: Nodos
- `Gizmo`: Gizmos personalizados
- `GizmoGroup`: Grupos de gizmos

Cada tipo tiene métodos para:
- Añadir clases (`add_class`)
- Obtener clases (`get_classes`)
- Ordenar clases (`sort_classes`)
- Registrar y desregistrar clases (`register_classes`, `unregister_classes`)

### 3. Sistema de Propiedades

ACKit proporciona wrappers tipados para las propiedades de Blender, facilitando su definición y uso:

#### Propiedades Básicas (ACK.Props)

Los tipos básicos de propiedades, sin tipado fuerte:
- `Int`: Propiedades de enteros
- `Float`: Propiedades de números de punto flotante
- `Bool`: Propiedades booleanas
- `String`: Propiedades de texto
- `Enum`: Propiedades de enumeración
- `Collection`: Propiedades de colección
- `Pointer`: Propiedades de puntero
- Varios tipos de vectores y colores

#### Propiedades con Tipado Fuerte (ACK.PropsWrapped)

Versiones con tipado fuerte para mejor autocompletado e información en IDEs:
- `Int`: Con método encadenado `.default()`, `.min()`, `.max()`, etc.
- `Float`: Con método encadenado `.default()`, `.min()`, `.max()`, etc.
- `Bool`: Con método encadenado `.default()`, etc.
- `String`: Con método encadenado `.default()`, etc.
- `Enum`: Con método encadenado `.items()`, `.default()`, etc.

Ejemplo:
```python
my_float = ACK.PropsWrapped.Float("Mi Valor").default(0.5).min(0.0).max(1.0)
```

#### Registro de Propiedades

Métodos para registrar propiedades en tipos de Blender:
- `ACK.Register.Property`: Registro individual
- `ACK.Register.Properties`: Registro masivo

### 4. Gestión Global

La clase `GLOBALS` en `globals.py` proporciona acceso centralizado a información importante:

- Información de Blender (`BLENDER_VERSION`, `IN_BACKGROUND`)
- Información del addon (`ADDON_MODULE`, `ADDON_MODULE_NAME`, `ADDON_MODULE_UPPER`)
- Rutas importantes (`ADDON_SOURCE_PATH`, `ADDON_DIR`, `ICONS_PATH`, `IMAGES_PATH`, `USER_CONFIG_DIR`)
- Métodos de utilidad
  - `check_in_development()`: Detecta si el addon está en modo desarrollo
  - `check_in_production()`: Detecta si el addon está en modo producción
  - `ensure_config_dir()`: Asegura que exista el directorio de configuración
  - `get_value()`: Obtiene un valor de la configuración global
  - `set_value()`: Establece un valor en la configuración global

### 5. Sistema de Polling

El sistema de polling (`polling.py`) proporciona decoradores para definir condiciones de disponibilidad para operadores y elementos de UI:

- `ACK.Poll.ACTIVE_OBJECT`: Comprueba propiedades del objeto activo
  - `ACK.Poll.ACTIVE_OBJECT.ANY`: Cualquier objeto activo
  - `ACK.Poll.ACTIVE_OBJECT.MESH`: Objeto malla activo
  - etc.
- `ACK.Poll.MODE`: Comprueba el modo actual
  - `ACK.Poll.MODE.OBJECT`: Modo objeto
  - `ACK.Poll.MODE.EDIT`: Modo edición
  - etc.
- `ACK.Poll.ACTIVE_BRUSH`: Comprueba el pincel activo en modos de pintura
- `ACK.Poll.custom()`: Polling personalizado

### 6. Generación Automática de Código

El módulo `auto_code` permite generar automáticamente código para:

- `AutoCode.OPS`: Wrappers tipados para operadores
- `AutoCode.ICONS`: Constantes para iconos
- `AutoCode.TYPES`: Clases de tipos personalizados

### 7. Decoradores y Flags

ACKit proporciona diversos decoradores y flags para modificar el comportamiento de clases:

- `ACK.Flags.OPERATOR`: Flags para operadores (REGISTER, UNDO, BLOCKING, etc.)
- `ACK.Flags.MODAL`: Flags para operadores modales (DRAW_POST_PIXEL, etc.)
- `ACK.Flags.PANEL`: Opciones para paneles (HIDE_HEADER, DEFAULT_CLOSED, etc.)
- `ACK.Flags.NODE_CATEGORY`: Decorador para especificar categorías de nodos
- Decoradores de registro en `reg_deco` (handlers, keymaps, timers, etc.)

## Diagrama Conceptual de Clases

```
+------------------------+       +------------------------+
|          ACK           |<------|      AddonLoader      |
|------------------------|       |------------------------|
| + Register             |       | + init_modules()       |
| + Types                |       | + register_modules()   |
| + Returns              |       | + unregister_modules() |
| + Props                |       | + fetch_module_callbacks|
| + PropsWrapped         |       | + cleanse_modules()    |
| + Flags                |       +------------------------+
| + Metadata             |
| + Poll                 |       +------------------------+
+------------------------+       |         BTypes         |
         ^                       |------------------------|
         |                       | + Operator             |
         |                       | + Panel                |
+------------------------+       | + Menu                 |
|     auto_code          |       | + PropertyGroup        |
|------------------------|       | + add_class()          |
| + OPS                  |       | + get_classes()        |
| + ICONS                |       | + register_classes()   |
| + TYPES                |       | + unregister_classes() |
+------------------------+       +------------------------+
         ^                                 ^
         |                                 |
+------------------------+       +------------------------+
|        GLOBALS         |       |     PropertyTypes      |
|------------------------|       |------------------------|
| + ADDON_MODULE         |       | + Int                  |
| + BLENDER_VERSION      |       | + Float                |
| + ADDON_SOURCE_PATH    |       | + String               |
| + check_in_development |       | + Collection           |
| + get_value()          |       +------------------------+
| + set_value()          |                 ^
+------------------------+                 |
                                  +------------------------+
                                  | WrappedPropertyTypes   |
                                  |------------------------|
                                  | + Int().default().min()|
                                  | + Float()              |
                                  | + String()             |
                                  +------------------------+
```

## Flujo de Ejecución

El flujo típico de ejecución cuando se utiliza ACKit en un addon es:

1. **Inicialización**:
   - Se importa `AddonLoader` en el `__init__.py` principal
   - Se llama a `AddonLoader.init_modules()` para descubrir todos los módulos
   - Se ejecutan los callbacks `init` y `late_init` en todos los módulos
   - Se genera código automáticamente si se especifica con `auto_code`

2. **Registro**:
   - Cuando Blender carga el addon, se llama a `AddonLoader.register_modules()`
   - Las clases de Blender son registradas a través del sistema de BTypes
   - Se ejecutan los callbacks `register` y `late_register` en todos los módulos

3. **Uso del Addon**:
   - Las clases registradas (operadores, paneles, etc.) están disponibles para el usuario
   - Las propiedades definidas están accesibles a través de la API de Blender
   - Los sistemas de polling determinan cuándo están disponibles operadores y elementos de UI

4. **Desregistro**:
   - Cuando Blender desactiva el addon, se llama a `AddonLoader.unregister_modules()`
   - Las clases de Blender son desregistradas en orden inverso
   - Se ejecutan los callbacks `unregister` y `late_unregister` en todos los módulos
   - Se limpia la caché de clases

## Extensibilidad

ACKit está diseñado para ser extensible, permitiendo a los desarrolladores:

1. **Añadir nuevos tipos de clases**: Extendiendo la enumeración `BTypes`
2. **Personalizar el proceso de registro**: Implementando callbacks en sus módulos
3. **Agregar funcionalidad personalizada**: Extendiendo la clase `ACK` con nuevos métodos y propiedades
4. **Crear decoradores personalizados**: Para comportamientos específicos
5. **Integrar con otros sistemas**: Mediante el uso de la API de callbacks

Esta estructura modular y extensible hace que ACKit sea una base sólida para el desarrollo de addons complejos para Blender, proporcionando una abstracción poderosa y tipada sobre la API nativa de Blender. 