# Visión General de la API de ACKit

ACKit proporciona una API completa y tipada para el desarrollo de addons en Blender. Esta guía ofrece una visión general de los componentes principales de la API.

## Estructura de la API

ACKit está diseñado con un enfoque modular y jerárquico, centralizando el acceso a través de la clase `ACK`. Esta estructura facilita el descubrimiento y el uso de las diferentes funcionalidades.

```
ACK
├── Register                # Sistema de registro
│   ├── Types               # Wrappers tipados para clases de Blender
│   ├── FromFunction        # Creación de clases a partir de funciones
│   ├── Property/Properties # Registro de propiedades
│
├── Props                   # Propiedades básicas
├── PropsWrapped            # Propiedades con tipado fuerte
├── Returns                 # Valores de retorno para operadores
├── Flags                   # Flags y opciones para clases
├── Poll                    # Sistema de polling (disponibilidad)
└── Metadata                # Gestión de metadatos
```

## Componentes Principales

### 1. Sistema de Registro (`ACK.Register`)

El centro de ACKit es su sistema de registro, que maneja la inicialización, registro y desregistro de todas las clases y módulos del addon.

```python
# Registro de módulos a través de AddonLoader
from .ackit import AddonLoader

def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()
```

### 2. Tipos Tipados (`ACK.Register.Types`)

ACKit proporciona wrappers tipados para las clases de Blender, organizados en categorías:

```python
# Operadores
from .ackit import ACK

class MyOperator(ACK.Register.Types.Ops.Generic):
    # Implementación...

# Paneles
class MyPanel(ACK.Register.Types.UI.Panel):
    # Implementación...

# Propiedades
class MyPropertyGroup(ACK.Register.Types.Data.PropertyGroup):
    # Implementación...

# Nodos
class MyNode(ACK.Register.Types.Nodes.Node):
    # Implementación...
```

### 3. Sistema de Propiedades (`ACK.Props` y `ACK.PropsWrapped`)

ACKit ofrece dos sistemas de propiedades:

```python
# Propiedades básicas (sin tipado fuerte)
my_int = ACK.Props.Int(name="Mi Entero", default=5, min=0, max=10)

# Propiedades con tipado fuerte (recomendado)
my_int = ACK.PropsWrapped.Int("Mi Entero").default(5).min(0).max(10)
```

### 4. Sistema de Polling (`ACK.Poll`)

Simplifica la definición de condiciones de disponibilidad para operadores y UI:

```python
@ACK.Poll.ACTIVE_OBJECT.MESH  # Disponible solo con objetos mesh activos
@ACK.Poll.MODE.EDIT           # Disponible solo en modo edición
class MeshEditOperator(ACK.Register.Types.Ops.Generic):
    # Implementación...
```

### 5. Flags y Valores de Retorno (`ACK.Flags` y `ACK.Returns`)

Constantes y flags para configurar el comportamiento:

```python
@ACK.Flags.OPERATOR.REGISTER_UNDO  # Permite deshacer la operación
class UndoableOperator(ACK.Register.Types.Ops.Generic):
    def execute(self, context):
        # Implementación...
        return ACK.Returns.Operator.FINISHED
```

### 6. Creación de Tipos a partir de Funciones (`ACK.Register.FromFunction`)

Permite crear clases de Blender a partir de funciones simples:

```python
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Tab")
def my_panel(context, layout):
    layout.label(text="Mi Panel Simple")
```

## Módulos Adicionales

Además de la API principal, ACKit proporciona módulos adicionales:

### Generación Automática de Código (`auto_code`)

Genera wrappers para operadores, iconos y tipos:

```python
from .ackit import AddonLoader, AutoCode

AddonLoader.init_modules(
    auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}
)
```

### Utilidades (`utils`)

Conjunto de utilidades para tareas comunes:

```python
from .ackit.utils import fs, cursor, previews

# Ejemplos de uso
file_path = fs.get_addon_path("resources", "templates")
cursor.set_cursor("WAIT")
preview = previews.load_preview("my_icon.png")
```

### Depuración (`debug`)

Herramientas para depuración y registro:

```python
from .ackit.debug import output, logger

output.log("Mensaje de información")
logger.info("Operación completada")
```

## Guías de API Detalladas

Para más información sobre componentes específicos, consulta:

- [API Principal ACK](ack.md)
- [Sistema de Registro](register.md)
- [Propiedades](properties.md)
- [Sistema de Polling](polling.md)
- [Decoradores y Flags](decorators.md)
- [Utilidades](utils.md)
- [Depuración](debug.md) 