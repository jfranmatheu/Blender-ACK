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
  - [Sistema de Propiedades](#sistema-de-propiedades)
    - [Propiedades Básicas](#propiedades-básicas)
    - [Propiedades Avanzadas](#propiedades-avanzadas)
  - [Sistema de Polling](#sistema-de-polling)
  - [Integración con Extension Platform](#integración-con-extension-platform)
  - [Generación Automática de Código](#generación-automática-de-código)
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

    # Método para dibujar en 2D en el viewport
    def draw_2d(self, context):
        blf.size(0, 12)
        blf.position(0, 100, 50, 0)
        blf.color(0, 1, 0, 0, 1)
        blf.draw(0, self.text)
```

Los operadores modales ofrecen una estructura clara con:
- `modal_enter`: Inicialización
- `modal_update`: Manejador de eventos principal
- `modal_exit`: Limpieza al finalizar
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
    
    # Panel con cabecera oculta
    @ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", flags=(ACK.Flags.PANEL.HIDE_HEADER,), order=1)
    def my_panel_no_header(context, layout):
        layout.label(text="Panel sin cabecera")
    
    # Panel cerrado por defecto
    @ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", flags=(ACK.Flags.PANEL.DEFAULT_CLOSED,), order=2)
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

# Combinaciones
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.EDIT              # Solo en modo edición con objetos mesh activos

# Polling personalizado
@ACK.Poll.custom(lambda cls, context: context.scene.render.engine == 'CYCLES')
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

El código generado para operadores permite invocarlos de manera tipada:

```python
# Código generado automáticamente
from ops import MYADDON_OT_My_Operator
MYADDON_OT_My_Operator.run(param1="valor", param2=42)
MYADDON_OT_My_Operator.run_invoke(param1="valor")  # Modo INVOKE_DEFAULT
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