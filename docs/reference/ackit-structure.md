# Estructura de ACKit

Este documento proporciona una referencia completa de la estructura de directorios y organización del código de ACKit, para ayudar a los desarrolladores a entender y navegar por el framework.

## Visión General

ACKit está organizado en un conjunto de módulos especializados, cada uno con una función específica dentro del framework. Esta estructura modular permite una mayor organización, mantenibilidad y extensibilidad.

## Estructura de Directorios

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
│   │   ├── ui/               # Elementos de interfaz de usuario
│   │   ├── data/             # Clases de datos
│   │   └── nodes/            # Sistema de nodos
│   │
│   ├── reg_deco/             # Decoradores para registro
│   │   ├── __init__.py       # Exportación de decoradores
│   │   ├── handlers.py       # Decoradores para manejadores de eventos
│   │   ├── keymaps.py        # Decoradores para mapas de teclas
│   │   ├── rna_sub.py        # Decoradores para suscripciones RNA
│   │   ├── timer.py          # Decoradores para temporizadores
│   │   ├── property_group.py # Decoradores para grupos de propiedades
│   │   └── ui/               # Decoradores específicos para UI
│   │
│   ├── props/                # Sistema de propiedades
│   │   ├── __init__.py       # Exportación de tipos de propiedades
│   │   ├── property.py       # Definiciones base de propiedades
│   │   └── typed/            # Propiedades con tipado fuerte
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

### 1. Núcleo de ACKit

#### _ack.py

La clase `ACK` en `_ack.py` es el punto de entrada principal para acceder a la funcionalidad de ACKit. Implementa el patrón de diseño Facade, proporcionando una API unificada a través de clases anidadas.

```python
class ACK:
    class Register:
        # Sistema de registro
        
    class Props:
        # Propiedades básicas
        
    class PropsWrapped:
        # Propiedades tipadas
        
    class Returns:
        # Valores de retorno para operadores
        
    class Flags:
        # Flags y opciones para clases
        
    class Poll:
        # Sistema de polling
```

#### globals.py

El módulo `globals.py` define variables y constantes globales que son utilizadas a través de todo el framework:

```python
class GLOBALS:
    # Información del addon
    ADDON_MODULE = __main_package__
    ADDON_MODULE_SHORT = __main_package__.split('.')[-1]
    ADDON_NAME = "ACKit"
    
    # Rutas
    ADDON_SOURCE_PATH = os.path.dirname(os.path.dirname(__file__))
    ICONS_PATH = os.path.join(ADDON_SOURCE_PATH, "icons")
    
    # Sistema de versiones
    BLENDER_VERSION = get_blender_version()
    PYTHON_VERSION = get_python_version()
```

### 2. Sistema de Registro

#### registry/addon_loader.py

El `AddonLoader` gestiona el ciclo de vida completo de los módulos de un addon:

```python
class AddonLoader:
    @classmethod
    def init_modules(cls, use_autoload=False, auto_code=None):
        # Inicialización de módulos y configuración
        
    @classmethod
    def register_modules(cls):
        # Registro de módulos y clases
        
    @classmethod
    def unregister_modules(cls):
        # Desregistro de módulos y clases
```

#### registry/btypes.py

El módulo `btypes.py` define la enumeración `BTypes` que contiene todos los tipos soportados por Blender que pueden ser registrados:

```python
class BTypes(Enum):
    Operator = 1
    Macro = 2
    Panel = 3
    Menu = 4
    # ... más tipos ...
```

#### registry/polling.py

El sistema de polling proporciona decoradores para establecer condiciones de disponibilidad para operadores y UI:

```python
class Poll:
    @staticmethod
    def custom(poll_func):
        # Decorador para función de polling personalizada
        
    class ACTIVE_OBJECT:
        @staticmethod
        def ANY(cls):
            # Disponible cuando hay un objeto activo
            
        @staticmethod
        def MESH(cls):
            # Disponible cuando el objeto activo es un mesh
```

### 3. Tipos Registrables

#### registry/reg_types/

Los wrappers tipados para clases de Blender se encuentran en este directorio, organizados por categoría:

##### registry/reg_types/ops/

Wrappers para operadores:

```python
class Operator(bpy.types.Operator, BaseType):
    # Implementación base para operadores
    
class Action(Operator):
    # Operador con estructura para acciones
    
class Modal(Operator):
    # Operador modal con estructura para interacciones continuas
```

##### registry/reg_types/ui/

Wrappers para elementos de interfaz de usuario:

```python
class Panel(bpy.types.Panel, BaseType):
    # Implementación base para paneles
    
class Menu(bpy.types.Menu, BaseType):
    # Implementación base para menús
    
class PieMenu(bpy.types.Menu, BaseType):
    # Implementación base para menús circulares
```

### 4. Sistema de Propiedades

#### registry/props/

El sistema de propiedades define las propiedades estándar y tipadas:

```python
class PropertyTypes:
    # Propiedades básicas sin tipado fuerte
    @staticmethod
    def Int(**kwargs):
        return bpy.props.IntProperty(**kwargs)
        
    @staticmethod
    def Float(**kwargs):
        return bpy.props.FloatProperty(**kwargs)
```

#### registry/props/typed/

Propiedades con tipado fuerte:

```python
class WrappedTypedPropertyTypes:
    # Propiedades con tipado fuerte
    @staticmethod
    def Int(name, **kwargs):
        return IntPropWrapper(name, **kwargs)
        
    @staticmethod
    def Float(name, **kwargs):
        return FloatPropWrapper(name, **kwargs)
```

### 5. Decoradores

#### registry/reg_deco/

Decoradores para registro automatizado:

```python
class RegDeco:
    class HANDLER:
        @staticmethod
        def LOAD_PRE(persistent=False):
            # Decorador para funciones que se ejecutan antes de cargar un archivo
            
        @staticmethod
        def LOAD_POST(persistent=False):
            # Decorador para funciones que se ejecutan después de cargar un archivo
    
    class KEYMAP:
        @staticmethod
        def register_keymap(idname, space_type, region_type, key, event_type, **modifiers):
            # Registrar un atajo de teclado
```

### 6. Generación Automática de Código

#### auto_code/

Módulos para generación automática de código:

```python
class AutoCode(Enum):
    OPS = 1    # Genera wrappers para operadores
    ICONS = 2  # Genera constantes para iconos
    TYPES = 3  # Genera tipos personalizados
```

#### auto_code/ops.py

Genera wrappers para facilitar la invocación de operadores desde código:

```python
def generate_ops_wrapper(ops_classes):
    # Genera un archivo Python con wrappers para todos los operadores
    # Ejemplo de wrapper generado:
    # class MY_OT_operator:
    #     @staticmethod
    #     def run(**kwargs):
    #         return bpy.ops.my.operator(**kwargs)
    #     @staticmethod
    #     def run_invoke():
    #         return bpy.ops.my.operator('INVOKE_DEFAULT')
```

### 7. Utilidades

#### utils/

Colección de utilidades para tareas comunes:

```python
# utils/fs.py
def get_addon_path(*subpath):
    # Obtener ruta dentro del addon
    
# utils/cursor.py
def set_cursor(cursor_type='DEFAULT'):
    # Cambiar el cursor de Blender
    
# utils/previews.py
def load_preview(image_path, name=None):
    # Cargar una imagen como preview
```

### 8. Depuración

#### debug/

Herramientas para depuración y logging:

```python
# debug/output.py
def log(message, level='INFO'):
    # Imprimir mensaje en la consola
    
# debug/logger.py
class Logger:
    def info(self, message):
        # Registrar mensaje informativo
        
    def warning(self, message):
        # Registrar advertencia
        
    def error(self, message):
        # Registrar error
```

## Patrones de Diseño Utilizados

ACKit implementa varios patrones de diseño que mejoran su estructura y funcionamiento:

### Patrón Singleton

Utilizado en la clase `GLOBALS` para proporcionar un punto de acceso centralizado a la configuración:

```python
class GLOBALS:
    # Propiedades y métodos...
```

### Patrón Facade

La clase `ACK` actúa como una fachada que simplifica el acceso a la funcionalidad subyacente:

```python
class ACK:
    # Clases y métodos anidados que exponen funcionalidad
```

### Patrón Factory

Implementado en varios lugares para crear instancias de clases de Blender:

```python
class FromFunction:
    @staticmethod
    def ACTION(label, **kwargs):
        # Crea un operador de acción a partir de una función
```

### Patrón Decorator

Utilizado extensivamente para modificar el comportamiento de clases y funciones:

```python
@ACK.Poll.ACTIVE_OBJECT.MESH
class MyOperator(ACK.Register.Types.Ops.Generic):
    # La clase ahora tiene una función poll que verifica si el objeto activo es un mesh
```

## Flujo de Datos y Ejecución

### Ciclo de Vida del Addon

1. **Inicialización**:
   ```python
   AddonLoader.init_modules(auto_code={AutoCode.OPS, AutoCode.ICONS})
   ```
   
2. **Registro**:
   ```python
   AddonLoader.register_modules()
   ```
   
   - Descubre módulos y clases
   - Genera código automático
   - Registra clases en Blender
   - Ejecuta callbacks de registro

3. **Ejecución**: El addon se ejecuta normalmente

4. **Desregistro**:
   ```python
   AddonLoader.unregister_modules()
   ```
   
   - Ejecuta callbacks de desregistro
   - Desregistra clases de Blender
   - Limpia recursos

## Mejores Prácticas de Código

ACKit sigue varias mejores prácticas que se reflejan en su estructura:

1. **Modularidad**: Código organizado en módulos con responsabilidades claras
2. **Encapsulación**: Detalles de implementación ocultos detrás de interfaces limpias
3. **Tipado Fuerte**: Uso extensivo de anotaciones de tipo para mejorar el desarrollo
4. **Documentación integrada**: Docstrings y nombres claros para facilitar el entendimiento
5. **Extensibilidad**: Diseño que permite extender funcionalidades sin modificar el código existente 