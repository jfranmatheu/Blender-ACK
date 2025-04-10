# Sistema de Depuración en ACKit

ACKit proporciona un sistema de depuración completo para ayudar en el desarrollo y solución de problemas de addons. Esta guía cubre las herramientas de depuración disponibles y cómo usarlas eficazmente.

## Módulo debug

El módulo `debug` de ACKit contiene varias herramientas para depuración, logging y perfilado:

```
ackit/debug/
├── __init__.py           # Exporta las funciones principales
├── output.py             # Funciones para salida de depuración en consola
├── logger.py             # Sistema de logging con niveles y formateo
└── profiler.py           # Herramientas de perfilado de rendimiento
```

## Salida de Depuración Básica

El módulo `output` proporciona funciones simples para mostrar información de depuración:

```python
from ...ackit.debug import output

# Mensaje básico
output.log("Procesando objeto")

# Niveles de log
output.log("Operación completada con éxito", level='INFO')
output.log("Advertencia: valor fuera de rango", level='WARNING')
output.log("Error crítico en el proceso", level='ERROR')

# Mensajes condicionales (solo se muestran en modo debug)
output.debug("Valores internos: x={0}, y={1}", 10, 20)

# Imprimir variables
my_var = {"key": "value", "number": 42}
output.print_var(my_var, "my_var")  # Imprime con formato y tipo
```

## Sistema de Logging Avanzado

El módulo `logger` proporciona un sistema de logging más avanzado con niveles, formatos y destinos configurables:

```python
from ...ackit.debug import logger

# Crear un logger para un módulo específico
my_logger = logger.get_logger("mi_addon.module")

# Diferentes niveles de logging
my_logger.debug("Información detallada (solo visible en modo debug)")
my_logger.info("Información general")
my_logger.warning("Advertencia")
my_logger.error("Error")
my_logger.critical("Error crítico")

# Logging con formato
my_logger.info("Procesando %d objetos", 5)
my_logger.error("Error en el objeto: %s", obj.name)

# Logging con excepciones
try:
    # Código que puede fallar
    result = 10 / 0
except Exception as e:
    my_logger.exception("Ocurrió un error: %s", str(e))
    # Esto incluirá automáticamente el stack trace
```

### Configuración del Logger

Puedes configurar el comportamiento del sistema de logging:

```python
from ...ackit.debug import logger

# Configurar nivel de log global
logger.set_level('DEBUG')  # Muestra todos los mensajes
logger.set_level('INFO')   # Solo muestra INFO, WARNING, ERROR, CRITICAL
logger.set_level('WARNING')  # Solo muestra WARNING, ERROR, CRITICAL

# Configurar logger específico
my_logger = logger.get_logger("mi_addon.ui")
my_logger.setLevel('DEBUG')

# Añadir manejador de archivo (guarda logs en un archivo)
logger.add_file_handler("mi_addon_log.txt")

# Formato personalizado
logger.set_format("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
```

## Perfilado de Rendimiento

El módulo `profiler` proporciona herramientas para medir y analizar el rendimiento del código:

```python
from ...ackit.debug import profiler

# Perfilar una función
@profiler.profile
def function_to_profile():
    # Código a perfilar
    for i in range(1000):
        _ = i * i

# Perfilar un bloque de código
with profiler.profiled_section("Cálculo complejo"):
    # Código a perfilar
    result = compute_complex_result()

# Cronometrar operaciones
timer = profiler.Timer()
timer.start()
# Operación a medir
heavy_operation()
elapsed = timer.stop()
print(f"La operación tomó {elapsed:.4f} segundos")

# Múltiples puntos de tiempo
timer = profiler.Timer()
timer.mark("inicio")
step1()
timer.mark("paso1")
step2()
timer.mark("paso2")
timer.print_intervals()  # Muestra el tiempo entre marcas
```

### Perfilado Detallado

Para un perfilado más detallado, puedes usar el decorador `profile_detailed`:

```python
from ...ackit.debug import profiler

@profiler.profile_detailed
def complex_algorithm(data):
    # Implementación
    pass

# Esto generará un informe detallado de las llamadas a funciones
# internas, tiempo acumulado, etc.
```

## Depuración Visual

ACKit también proporciona herramientas para depuración visual en el viewport de Blender:

```python
from ...ackit.debug import visual

# Dibujar puntos
visual.draw_point((0, 0, 0), color=(1, 0, 0, 1), size=5)

# Dibujar líneas
visual.draw_line((0, 0, 0), (1, 1, 1), color=(0, 1, 0, 1), width=2)

# Dibujar texto en el viewport
visual.draw_text("Depuración", position=(100, 100), 
                 color=(1, 1, 0, 1), size=12)

# Dibujar caja 3D
visual.draw_box(center=(0, 0, 0), dimensions=(1, 1, 1), 
                color=(0, 0, 1, 0.5))
```

## Inspección de Tipos y Objetos

Para inspeccionar tipos y objetos en tiempo de ejecución:

```python
from ...ackit.debug import inspect

# Inspeccionar un objeto
obj = context.active_object
inspect.print_attributes(obj)

# Información detallada de una propiedad
inspect.print_property_info(obj, "location")

# Inspeccionar una clase
inspect.print_class_hierarchy(bpy.types.Operator)

# Encontrar todos los operadores registrados con un patrón
ops = inspect.find_operators("object.*")
for op in ops:
    print(f"{op.bl_idname}: {op.bl_label}")
```

## Acceso a Datos Internos de Blender

Para acceder a estructuras de datos internas de Blender para depuración:

```python
from ...ackit.debug import blender_data

# Listar todos los addons cargados
addons = blender_data.get_loaded_addons()
for addon in addons:
    print(f"{addon['name']} - Habilitado: {addon['enabled']}")

# Revisar handlers registrados
handlers = blender_data.get_registered_handlers()
print(f"Load post handlers: {len(handlers['load_post'])}")

# Inspeccionar el contexto actual
context_dict = blender_data.inspect_context(context)
print(f"Área activa: {context_dict['area_type']}")
```

## Depuración Condicional

ACKit proporciona mecanismos para depuración condicional:

```python
from ...ackit.debug import output, logger
from ...ackit.globals import GLOBALS

# Habilitar modo debug global
GLOBALS.DEBUG_MODE = True

# Código que solo se ejecuta en modo debug
if GLOBALS.DEBUG_MODE:
    output.log("Información detallada para depuración")
    # Operaciones adicionales de depuración...

# Logging condicional
logger.debug_if(GLOBALS.DEBUG_MODE, "Mensajes detallados: %s", data)
```

## Aserción y Validación

Para validación en tiempo de desarrollo:

```python
from ...ackit.debug import assert_utils

# Aserciones básicas
assert_utils.assert_true(condition, "Mensaje si falla")
assert_utils.assert_equal(a, b, "a y b deben ser iguales")
assert_utils.assert_in_range(value, min_val, max_val, "valor fuera de rango")

# Validaciones más complejas
assert_utils.validate_object(obj, "No se encontró objeto válido")
assert_utils.validate_mesh(mesh, "Se requiere una malla válida")
```

## Herramientas de Desarrollo

Algunas herramientas útiles para el desarrollo:

```python
from ...ackit.debug import dev_tools

# Información detallada del entorno
dev_tools.print_environment_info()

# Detección de fugas de memoria
dev_tools.memory_usage_before = dev_tools.get_memory_usage()
# ... código a probar ...
dev_tools.check_memory_leak()

# Comprobación de errores comunes en addons
issues = dev_tools.check_addon_issues()
for issue in issues:
    print(f"Problema: {issue['description']}")
```

## Integración con el Panel de Depuración

ACKit incluye un panel de depuración integrado que puedes activar:

```python
from ...ackit.debug import ui

# Activar el panel de depuración
ui.register_debug_panel()

# El panel estará disponible en View3D > Sidebar > ACKit Debug
```

Este panel proporciona:
- Visualización de estado global
- Opciones de logging
- Información de rendimiento
- Herramientas de inspección

## Buenas Prácticas

1. **Usa niveles de log adecuados**:
   - `DEBUG`: Información detallada, útil para depuración
   - `INFO`: Mensajes informativos sobre el flujo normal
   - `WARNING`: Indicación de que algo inesperado ocurrió, pero se puede continuar
   - `ERROR`: Error que impidió que alguna funcionalidad operara correctamente
   - `CRITICAL`: Error grave que impide la operación del addon

2. **Limpia el código de producción**:
   - Considera usar `output.debug()` en lugar de `print()` para mensajes de depuración
   - Usa el modo de depuración condicional para código solo de desarrollo

3. **Perfilado estratégico**:
   - Perfila secciones específicas que sospechas causan problemas de rendimiento
   - Compara diferentes implementaciones con Timer

4. **Información contextual**:
   - Incluye información contextual útil en mensajes de depuración
   - Usa la funcionalidad de formateo para incluir valores relevantes

## Recursos Adicionales

- [Guía de Debugging en Blender](https://docs.blender.org/api/current/info_tips_and_tricks.html#debugging)
- [Buenas Prácticas de Logging](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) 