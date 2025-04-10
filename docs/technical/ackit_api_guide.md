# Guía de Referencia de la API ACKit

Esta guía proporciona ejemplos prácticos y referencias para utilizar ACKit en el desarrollo de addons para Blender, basados en el template de addon para ACKit.

## Tabla de Contenidos

- [Guía de Referencia de la API ACKit](#guía-de-referencia-de-la-api-ackit)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Configuración Inicial del Addon](#configuración-inicial-del-addon)
  - [Creación de Operadores](#creación-de-operadores)
    - [Operadores Genéricos](#operadores-genéricos)
    - [Operadores de Acción](#operadores-de-acción)
    - [Operadores Modales](#operadores-modales)
  - [Creación de Interfaces de Usuario](#creación-de-interfaces-de-usuario)
    - [Paneles](#paneles)
    - [Popovers](#popovers)
    - [Menús](#menús)
  - [Sistema de Propiedades](#sistema-de-propiedades)
    - [Propiedades Básicas](#propiedades-básicas)
    - [Propiedades Avanzadas](#propiedades-avanzadas)
    - [Registro de Propiedades](#registro-de-propiedades)
  - [Sistema de Polling](#sistema-de-polling)
    - [Creación de Decoradores de Polling Personalizados](#creación-de-decoradores-de-polling-personalizados)
    - [Polling Personalizado para Casos Específicos](#polling-personalizado-para-casos-específicos)
  - [Sistema de Registro](#sistema-de-registro)
    - [BTypes](#btypes)
    - [AddonLoader](#addonloader)
    - [Ciclo de Vida del Addon](#ciclo-de-vida-del-addon)
  - [Decoradores y Flags](#decoradores-y-flags)
    - [Decoradores de Operadores](#decoradores-de-operadores)
    - [Decoradores de UI](#decoradores-de-ui)
    - [Otros Decoradores](#otros-decoradores)
  - [Integración con Extension Platform](#integración-con-extension-platform)
  - [Generación Automática de Código](#generación-automática-de-código)
    - [Generación de Operadores (OPS)](#generación-de-operadores-ops)
    - [Generación de Iconos (ICONS)](#generación-de-iconos-icons)
    - [Generación de Tipos (TYPES)](#generación-de-tipos-types)
  - [Sistema de Debugging](#sistema-de-debugging)
  - [Prácticas Recomendadas](#prácticas-recomendadas)

## Configuración Inicial del Addon

Para comenzar a utilizar ACKit en tu addon, debes configurar el archivo `__init__.py` principal:

```python
from .ackit import AddonLoader, AutoCode

# Inicializar ACKit con opciones de generación automática de código
AddonLoader.init_modules(
    use_autoload=False,  # No usar el sistema legacy de AutoLoad
    auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}  # Generar código para operadores, iconos y tipos
)

def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()
```

El parámetro `auto_code` permite especificar qué código se generará automáticamente:
- `AutoCode.OPS`: Genera wrappers para operadores que facilitan su invocación desde código
- `AutoCode.ICONS`: Genera constantes para iconos
- `AutoCode.TYPES`: Genera tipos personalizados

## Creación de Operadores

ACKit proporciona tres tipos principales de operadores con diferentes propósitos:

### Operadores Genéricos

Los operadores genéricos (`ACK.Register.Types.Ops.Generic`) son la forma más básica de operadores en Blender. Son adecuados para operaciones simples.

```python
from ...ackit import ACK

@ACK.Poll.ACTIVE_OBJECT.ANY  # Decorador para establecer condición de polling
class GenericOperator(ACK.Register.Types.Ops.Generic):
    # Definición de propiedades con tipado fuerte
    new_name = ACK.PropsWrapped.String("Object Name").default("Best Name Ever")

    def invoke(self, context, event) -> None:
        context.active_object.name = self.new_name
        self.report({'INFO'}, f"New Name {self.new_name}")
        return ACK.Returns.Operator.FINISH
```

Los operadores genéricos generados automáticamente pueden ser invocados desde código utilizando los métodos `run()` o `run_invoke()`:

```python
# Ejecutar directamente
from ops import ACKITADDONTEMPLATE_OT_Generic_Operator
ACKITADDONTEMPLATE_OT_Generic_Operator.run(new_name="Mi Nuevo Nombre")

# Ejecutar con modo INVOKE (muestra la UI del operador si existe)
ACKITADDONTEMPLATE_OT_Generic_Operator.run_invoke()
```

### Operadores de Acción

Los operadores de acción (`ACK.Register.Types.Ops.Action`) son una extensión de los operadores genéricos que proporcionan una estructura más organizada para operadores con UI.

```python
from ...ackit import ACK

@ACK.Flags.OPERATOR.REGISTER_UNDO  # Activar registro en historia de deshacer
@ACK.Poll.ACTIVE_OBJECT.MESH       # Solo disponible con objetos mesh activos
@ACK.Poll.MODE.OBJECT              # Solo disponible en modo objeto
class ActionOperator(ACK.Register.Types.Ops.Action):
    label = "Test Action"          # Etiqueta del operador
    tooltip = "Transforms active mesh object location in Z axis"  # Descripción/tooltip

    # Propiedades con tipado fuerte
    enable = ACK.PropsWrapped.Bool("Enable")
    z_location = ACK.PropsWrapped.Float("Z")

    # Método para dibujar la UI del operador
    def draw_ui(self, context, layout):
        row = layout.row()
        row.prop(self, 'enable', text="Enable Feature")
        row.prop(self, 'z_location', text="Z Location")

    # Método principal que implementa la acción
    def action(self, context) -> None:
        if self.enable:
            context.active_object.location.z = self.z_location
            self.report_info(f"Value {self.z_location}")  # Helper para self.report
```

También es posible crear operadores de acción directamente a partir de funciones:

```python
@ACK.Register.FromFunction.ACTION("Mi Acción", tooltip="Descripción de la acción")
def mi_accion(context):
    context.active_object.location.z = 1.0
```

### Operadores Modales

Los operadores modales (`ACK.Register.Types.Ops.Modal`) son utilizados para operaciones interactivas que mantienen el estado y continúan ejecutándose hasta que se completan o cancelan.

```python
from ...ackit import ACK, OpsReturn
from ...ackit.utils import IsEventType, IsEventValue

import blf

@ACK.Flags.MODAL.DRAW_POST_PIXEL.VIEW_3D  # Dibujar en el viewport 3D
@ACK.Poll.ACTIVE_OBJECT.ANY
class ModalDrawOperator(ACK.Register.Types.Ops.Modal):
    # Se llama al inicio del modo modal
    def modal_enter(self, context, event):
        self.text = "Hello, world!"

    # Se llama en cada actualización del evento modal
    def modal_update(self, context, event) -> OpsReturn:
        if event.type == 'ESC':
            return OpsReturn.FINISH
        if event.unicode:
            self.text += event.unicode
            self.tag_redraw(context)  # Helper para forzar redibujado
            return OpsReturn.RUN
        elif IsEventType.BACK_SPACE and IsEventValue.RELEASE and self.text != '':
            self.text = self.text[:-1]
            self.tag_redraw(context)
            return OpsReturn.RUN
        return OpsReturn.PASS

    # Método para dibujar en 2D en el viewport (cuando se usa el flag DRAW_POST_PIXEL)
    def draw_2d(self, context):
        blf.size(0, 12)
        blf.position(0, 100, 50, 0)
        blf.color(0, 1, 0, 0, 1)
        blf.draw(0, self.text)
```

Los operadores modales ofrecen una estructura clara con:
- `modal_enter`: Inicialización al entrar en modo modal
- `modal_update`: Manejador de eventos principal (se llama continuamente)
- `modal_exit`: Limpieza al finalizar el modo modal
- `draw_2d`: Dibujo en pantalla (si se usa el flag `DRAW_POST_PIXEL`)

## Creación de Interfaces de Usuario

ACKit simplifica la creación de interfaces de usuario mediante decoradores y funciones.

### Paneles

Puedes crear paneles utilizando decoradores de función para un enfoque más conciso:

```python
from ...ackit import ACK

# Panel en la vista 3D con pestaña personalizada y orden específico
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", order=1)
def my_panel(context, layout):
    layout.label(text="My Panel")
    layout.operator('render.render', text="Render")
```

También puedes aplicar flags a los paneles para modificar su comportamiento:

```python
# Panel con cabecera oculta
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", flags=(ACK.Flags.PANEL.HIDE_HEADER,))
def my_panel_no_header(context, layout):
    layout.label(text="Panel sin cabecera")

# Panel cerrado por defecto
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", flags=(ACK.Flags.PANEL.DEFAULT_CLOSED,))
def my_panel_collapsed(context, layout):
    layout.label(text="Panel inicialmente cerrado")
```

### Popovers

Los popovers son ventanas emergentes que puedes crear fácilmente:

```python
from ...ackit import ACK

@ACK.Register.FromFunction.POPOVER()
def my_popover(context, layout):
    layout.label(text="My Popover")
    layout.prop(context.object, "name")

# En otro panel, puedes mostrar el popover
@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab")
def my_panel(context, layout):
    layout.label(text="Mi Panel Principal")
    # Usar el helper para mostrar el popover
    my_popover.draw_in_layout(layout, text="Abrir Popover")
```

### Menús

Puedes crear menús mediante funciones decoradas:

```python
from ...ackit import ACK

# Menú estándar
@ACK.Register.FromFunction.MENU()
def my_menu(context, layout):
    layout.label(text="Mi Menú")
    layout.operator('object.select_all')

# Menú circular (pie menu)
@ACK.Register.FromFunction.PIE_MENU()
def my_pie_menu(context, layout):
    pie = layout.menu_pie()
    pie.operator('mesh.primitive_cube_add', text="Añadir Cubo")
    pie.operator('mesh.primitive_uv_sphere_add', text="Añadir Esfera")
```

## Sistema de Propiedades

ACKit proporciona un sistema de propiedades con tipado fuerte, facilitando la definición de propiedades para operadores y grupos de propiedades.

### Propiedades Básicas

```python
# Propiedades básicas
my_int = ACK.Props.Int("Mi Entero")
my_float = ACK.Props.Float("Mi Flotante")
my_bool = ACK.Props.Bool("Mi Booleano")
my_string = ACK.Props.String("Mi Texto")

# Propiedades con tipado fuerte (recomendadas)
my_int = ACK.PropsWrapped.Int("Mi Entero").default(5).min(0).max(10)
my_float = ACK.PropsWrapped.Float("Mi Flotante").default(1.5).min(0.0).max(10.0)
my_bool = ACK.PropsWrapped.Bool("Mi Booleano").default(True)
my_string = ACK.PropsWrapped.String("Mi Texto").default("Valor predeterminado")
```

Las propiedades con tipado fuerte (`ACK.PropsWrapped`) proporcionan mejor soporte para autocompletado e información de tipo en IDEs.

### Propiedades Avanzadas

```python
# Enumeración
my_enum = ACK.PropsWrapped.Enum("Mi Enum").items(
    ("OP1", "Opción 1", "Descripción de la opción 1"),
    ("OP2", "Opción 2", "Descripción de la opción 2")
).default("OP1")

# Colección
my_collection = ACK.PropsWrapped.Collection("Mi Colección")

# Vector y Color
my_vector = ACK.PropsWrapped.FloatVector("Mi Vector", size=3).default((0.0, 0.0, 0.0))
my_color = ACK.PropsWrapped.FloatColor("Mi Color").default((1.0, 1.0, 1.0, 1.0))
```

### Registro de Propiedades

Para registrar propiedades en tipos de Blender (como Scene, Object, etc.), puedes usar el sistema `ACK.Register.Property`:

```python
from ...ackit import ACK
import bpy

# En la función register() de un módulo
def register():
    # Registrar una propiedad en la clase Scene
    ACK.Register.Property(
        bpy.types.Scene, 
        "mi_propiedad", 
        ACK.PropsWrapped.Float("Mi Propiedad").default(0.0).min(0.0).max(1.0),
        remove_on_unregister=True  # Eliminar la propiedad al desregistrar
    )

    # Registrar múltiples propiedades
    ACK.Register.Properties(
        bpy.types.Object,
        {
            "prop1": ACK.PropsWrapped.Bool("Propiedad 1"),
            "prop2": ACK.PropsWrapped.Int("Propiedad 2").default(5)
        }
    )
```

## Sistema de Polling

ACKit proporciona decoradores para establecer condiciones de polling (disponibilidad) para operadores y paneles:

```python
# Verificación de objeto activo
@ACK.Poll.ACTIVE_OBJECT.ANY       # Cualquier objeto activo
@ACK.Poll.ACTIVE_OBJECT.MESH      # Solo objetos mesh activos
@ACK.Poll.ACTIVE_OBJECT.ARMATURE  # Solo armaduras activas

# Verificación de modo
@ACK.Poll.MODE.OBJECT            # Solo en modo objeto
@ACK.Poll.MODE.EDIT              # Solo en modo edición
@ACK.Poll.MODE.POSE              # Solo en modo pose

# Verificación de pincel activo (para modos de pintura/escultura)
@ACK.Poll.ACTIVE_BRUSH           # Solo cuando hay un pincel activo

# Combinaciones
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.EDIT              # Solo en modo edición con objetos mesh activos

# Polling personalizado para casos de uso único
@ACK.Poll.custom(lambda context: context.scene.render.engine == 'CYCLES')
```

El sistema de polling se implementa internamente como un conjunto de funciones que se verifican en el método `poll` de la clase. Todas las condiciones deben cumplirse para que el operador esté disponible.

### Creación de Decoradores de Polling Personalizados

Para condiciones que necesitas reutilizar en varios operadores, puedes crear tus propios decoradores de polling:

```python
# Definir una función de polling
def has_animation_data(context):
    return (context.active_object is not None and 
            context.active_object.animation_data is not None and 
            context.active_object.animation_data.action is not None)

# Crear un decorador a partir de la función
HAS_ANIMATION = ACK.Poll.make_poll_decorator(has_animation_data)

# Usar el decorador personalizado
@HAS_ANIMATION
class AnimationOperator(ACK.Register.Types.Ops.Generic):
    # Implementación...
```

### Polling Personalizado para Casos Específicos

Para casos de uso único, puedes utilizar el método `custom` directamente:

```python
# Aplicar una condición de polling única 
@ACK.Poll.custom(lambda context: len(context.selected_objects) >= 3)
class MultiObjectOperator(ACK.Register.Types.Ops.Generic):
    # Solo disponible cuando hay al menos 3 objetos seleccionados
    # Implementación...
```

## Sistema de Registro

El sistema de registro de ACKit gestiona automáticamente la inicialización, registro y desregistro de clases y módulos.

### BTypes

La clase `BTypes` es una enumeración que define todos los tipos de Blender que pueden ser registrados:

```python
# Ejemplo interno de BTypes (no es código que escribirías directamente)
class BTypes(Enum):
    Operator = auto()
    Macro = auto()
    UIList = auto()
    Menu = auto()
    Panel = auto()
    PropertyGroup = auto()
    AddonPreferences = auto()
    NodeTree = auto()
    NodeSocket = auto()
    Node = auto()
    Gizmo = auto()
    GizmoGroup = auto()
```

Cada tipo en `BTypes` tiene métodos para:
- Añadir clases (`add_class`)
- Obtener clases (`get_classes`)
- Ordenar clases (`sort_classes`)
- Registrar y desregistrar clases (`register_classes`, `unregister_classes`)

### AddonLoader

El `AddonLoader` es la clase principal para gestionar el ciclo de vida del addon:

```python
# En __init__.py
from .ackit import AddonLoader

AddonLoader.init_modules()  # Inicializar módulos
AddonLoader.register_modules()  # Registrar módulos
AddonLoader.unregister_modules()  # Desregistrar módulos
```

Internamente, `AddonLoader` descubre todos los módulos de tu addon, recopila funciones de callback, y gestiona el registro y desregistro de clases a través del sistema `BTypes`.

### Ciclo de Vida del Addon

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

## Decoradores y Flags

ACKit proporciona numerosos decoradores y flags para modificar el comportamiento de clases y funciones.

### Decoradores de Operadores

```python
# Añadir a la historia de deshacer
@ACK.Flags.OPERATOR.REGISTER_UNDO
class MiOperador(ACK.Register.Types.Ops.Generic):
    pass

# Operador interno (no aparece en búsquedas)
@ACK.Flags.OPERATOR.INTERNAL
class MiOperadorInterno(ACK.Register.Types.Ops.Generic):
    pass

# Bloquear interfaz durante ejecución
@ACK.Flags.OPERATOR.BLOCKING
class MiOperadorBloqueo(ACK.Register.Types.Ops.Generic):
    pass

# Permitir presets
@ACK.Flags.OPERATOR.PRESET
class MiOperadorConPresets(ACK.Register.Types.Ops.Generic):
    pass
```

### Decoradores de UI

```python
# Panel con cabecera oculta
@ACK.Flags.PANEL.HIDE_HEADER
class MiPanel(ACK.Register.Types.UI.Panel):
    pass

# Panel cerrado por defecto
@ACK.Flags.PANEL.DEFAULT_CLOSED
class MiPanelCerrado(ACK.Register.Types.UI.Panel):
    pass

# Panel con instancias (para uso con templates_list)
@ACK.Flags.PANEL.INSTANCED
class MiPanelInstanciado(ACK.Register.Types.UI.Panel):
    pass
```

### Otros Decoradores

```python
# Categoría de nodo
@ACK.Flags.NODE_CATEGORY("Mi Categoría")
class MiNodo(ACK.Register.Types.Nodes.Node):
    pass

# Manejador de eventos (persistent significa que se mantiene al recargar un archivo)
@ACK.RegisterHandler.LOAD_PRE(persistent=True)
def on_file_load(context):
    print("Archivo cargado")

# Mapa de teclas
@ACK.RegDeco.KEYMAP("3D View", "Object Mode")
def register_keymap():
    return [
        ("object.select_all", {"type": 'A', "value": 'PRESS'}, {"action": 'TOGGLE'})
    ]
```

## Integración con Extension Platform

ACKit es compatible con el nuevo sistema Extension Platform de Blender 4.0+. Para utilizar esta funcionalidad:

1. Crea un archivo `blender_manifest.toml` en la raíz de tu addon:

```toml
schema_version = "1.0.0"
id = "mi_addon_id"
version = "1.0.0"
name = "Mi Addon"
tagline = "Descripción corta del addon"
maintainer = "Tu Nombre"
type = "add-on"

# Tags para categorización
tags = ["Modeling", "Animation"]

# Versión mínima de Blender compatible
blender_version_min = "4.2.0"

# Licencia
license = [
  "SPDX:GPL-2.0-or-later",
]

# Permisos (opcional)
[permissions]
network = "Razón para acceso a internet"
files = "Razón para acceso a archivos"
```

2. ACKit automáticamente detecta la versión de Blender y ajusta el comportamiento según corresponda:

```python
# En globals.py de ACKit
ADDON_MODULE_SHORT = __main_package__.split('.')[-1] if BLENDER_VERSION >= (4, 2, 0) else __main_package__
```

## Generación Automática de Código

ACKit incluye un sistema para generar código automáticamente:

```python
# En __init__.py
from .ackit import AddonLoader, AutoCode

AddonLoader.init_modules(
    auto_code={
        AutoCode.OPS,    # Genera ops.py con clases helper para operadores
        AutoCode.ICONS,  # Genera icons.py con constantes para iconos
        AutoCode.TYPES   # Genera types.py con tipos personalizados
    }
)
```

### Generación de Operadores (OPS)

Para cada operador definido en tu addon, `AutoCode.OPS` genera una clase helper con métodos `run()` y `run_invoke()`:

```python
# Código generado automáticamente
from ops import MYADDON_OT_My_Operator
MYADDON_OT_My_Operator.run(param1="valor", param2=42)
MYADDON_OT_My_Operator.run_invoke(param1="valor")  # Modo INVOKE_DEFAULT
```

### Generación de Iconos (ICONS)

Genera una clase `Icons` con constantes para todos los iconos en el directorio `lib/icons/`:

```python
from icons import Icons
Icons.CATEGORY.ICON_NAME  # Acceso a un icono específico
```

### Generación de Tipos (TYPES)

Genera una clase `Types` con tipos personalizados definidos en tu addon:

```python
from types import Types
Types.MiGrupoDeProps  # Acceso a un tipo PropertyGroup definido en tu addon
```

## Sistema de Debugging

ACKit incluye algunas herramientas de debugging que pueden ser útiles durante el desarrollo:

```python
from ...ackit.debug import print_debug
from ...ackit.debug.logger import get_logger
from ...ackit.debug.profiler import AddonProfiler

# Impresión de debug (solo en modo desarrollo)
print_debug("Mensaje de debug")

# Uso del logger
logger = get_logger()
logger.info("Información")
logger.warning("Advertencia")
logger.error("Error")

# Perfilado de código
profiler = AddonProfiler()
profiler.start_timer("mi_operacion")
# ... código a medir ...
elapsed = profiler.stop_timer("mi_operacion")
```

El modo de desarrollo se puede detectar usando:

```python
from ...ackit.globals import GLOBALS

is_dev = GLOBALS.check_in_development()
if is_dev:
    print("Estamos en modo desarrollo")
```

## Prácticas Recomendadas

1. **Estructura Modular**: Organiza tu código en módulos siguiendo la estructura del template:
   ```
   mi_addon/
   ├── __init__.py           # Punto de entrada principal
   ├── blender_manifest.toml # Definición para Extension Platform
   ├── ackit/                # Módulo ACKit (submodule)
   └── src/                  # Código fuente del addon
       ├── ops/              # Operadores
       ├── ui/               # Paneles y UI
       ├── props/            # Definiciones de propiedades
       └── utils/            # Utilidades
   ```

2. **Tipado Fuerte**: Utiliza `ACK.PropsWrapped` en lugar de `ACK.Props` para beneficiarte del tipado fuerte y la mejora de autocompletado.

3. **Uso de Decoradores**: Aprovecha los decoradores de polling y flags para simplificar tu código:
   ```python
   @ACK.Flags.OPERATOR.REGISTER_UNDO
   @ACK.Poll.ACTIVE_OBJECT.MESH
   @ACK.Poll.MODE.EDIT
   class MiOperador(ACK.Register.Types.Ops.Action):
       # Implementación...
   ```

4. **Funciones para UI Simple**: Para UI simple, utiliza el enfoque basado en funciones:
   ```python
   @ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Tab")
   def mi_panel(context, layout):
       layout.label(text="Mi Panel")
   ```

5. **Reportes Simplificados**: Utiliza los helpers para reportes:
   ```python
   self.report_info("Operación completada")    # En lugar de self.report({'INFO'}, "...")
   self.report_warning("Advertencia")          # En lugar de self.report({'WARNING'}, "...")
   self.report_error("Error")                  # En lugar de self.report({'ERROR'}, "...")
   ```

6. **Acceso a Globales**: Utiliza `GLOBALS` para acceder a información del addon:
   ```python
   from ...ackit.globals import GLOBALS
   
   addon_path = GLOBALS.ADDON_SOURCE_PATH
   is_dev = GLOBALS.check_in_development()
   ```

7. **Generación Automática**: Aprovecha el sistema de generación automática para operadores, iconos y tipos.

8. **Compatibilidad con Blender 4.x**: Diseña tu addon pensando en compatibilidad con la Extension Platform de Blender 4.x.

9. **Callbacks de Ciclo de Vida**: Utiliza los callbacks de ciclo de vida (`init`, `register`, `late_register`, etc.) para organizar la lógica de inicialización y limpieza.

10. **Uso de Clases vs Funciones**: 
    - Para operaciones complejas, utiliza clases derivadas de `ACK.Register.Types.Ops.*`
    - Para UI simple o operaciones sencillas, utiliza los decoradores de función `ACK.Register.FromFunction.*`