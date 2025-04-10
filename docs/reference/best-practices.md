# Mejores Prácticas para ACKit

Esta guía recopila las mejores prácticas para usar ACKit de manera efectiva en el desarrollo de addons para Blender, basadas en la experiencia de desarrolladores y patrones recomendados.

## Estructura y Organización

### Estructura de Archivos

1. **Sigue la estructura recomendada** para mantener tu código organizado y facilitar la colaboración:
   ```
   mi_addon/
   ├── __init__.py                # Punto de entrada principal
   ├── blender_manifest.toml      # Para Blender 4.0+
   ├── ackit/                     # Submódulo ACKit
   └── src/                       # Código fuente del addon
       ├── ops/                   # Operadores
       ├── ui/                    # Interfaces de usuario
       └── props/                 # Propiedades
   ```

2. **Nombra los archivos con claridad** utilizando nombres descriptivos que indiquen su propósito principal.

3. **Agrupa por funcionalidad** y no por tipo. Por ejemplo, si tienes una herramienta de escultura, coloca todos sus componentes (operadores, UI, propiedades) en una carpeta `sculpting/` en lugar de dispersarlos por tipo.

### Importaciones y Dependencias

1. **Sigue un patrón consistente para las importaciones**:
   ```python
   # Importaciones de Python estándar
   import os
   import math
   
   # Importaciones de Blender
   import bpy
   import bmesh
   
   # Importaciones de ACKit
   from ...ackit import ACK
   from ...ackit.utils import fs
   
   # Importaciones de tu addon
   from ..props.settings import MyAddonSettings
   ```

2. **Minimiza las importaciones circulares** planificando las dependencias entre módulos.

3. **Importa selectivamente** solo lo que necesitas, en lugar de importar módulos completos.

## Registro y Ciclo de Vida

1. **Deja que ACKit maneje el registro** en lugar de implementar manualmente el proceso de registro y desregistro:
   ```python
   from .ackit import AddonLoader, AutoCode
   
   def register():
       AddonLoader.register_modules()
   
   def unregister():
       AddonLoader.unregister_modules()
   ```

2. **Utiliza los callbacks de ciclo de vida** para inicialización y limpieza específica:
   ```python
   from ...ackit import ACK
   
   @ACK.RegDeco.ADDON_INIT
   def initialize_addon():
       # Código de inicialización específico
       setup_custom_resources()
   
   @ACK.RegDeco.ADDON_CLEANUP
   def cleanup_addon():
       # Limpieza al desinstalar
       cleanup_custom_resources()
   ```

3. **Aprovecha la generación automática de código** para reducir el código boilerplate:
   ```python
   AddonLoader.init_modules(
       auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}
   )
   ```

## Clases y Componentes

### Operadores

1. **Usa el tipo de operador adecuado** para cada tarea:
   - `ACK.Register.Types.Ops.Generic`: Para operadores simples.
   - `ACK.Register.Types.Ops.Action`: Para operadores con UI y estructura definida.
   - `ACK.Register.Types.Ops.Modal`: Para operadores interactivos que mantienen estado.

2. **Proporciona feedback claro al usuario** utilizando `self.report()` o los métodos auxiliares de ACKit:
   ```python
   def execute(self, context):
       if success:
           self.report_info("Operación completada con éxito")
       else:
           self.report_error("La operación falló debido a...")
       return ACK.Returns.Operator.FINISHED
   ```

3. **Implementa la cancelación de operaciones** cuando sea posible para permitir al usuario deshacer acciones:
   ```python
   def modal(self, context, event):
       if event.type == 'ESC':
           self.restore_original_state()
           return ACK.Returns.Modal.CANCELLED
   ```

### Interfaces de Usuario

1. **Usa el enfoque basado en funciones** para interfaces simples:
   ```python
   @ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
   def simple_panel(context, layout):
       layout.operator("object.my_operator")
   ```

2. **Usa el enfoque basado en clases** para interfaces complejas:
   ```python
   class ComplexPanel(ACK.Register.Types.UI.Panel):
       # Implementación...
   ```

3. **Organiza la UI por secciones** para una mejor legibilidad:
   ```python
   def draw(self, context):
       layout = self.layout
       
       # Sección de configuración general
       box = layout.box()
       box.label(text="Configuración General")
       # ...
       
       # Sección de operaciones
       box = layout.box()
       box.label(text="Operaciones")
       # ...
   ```

4. **Adapta la UI al contexto** para mostrar solo las opciones relevantes:
   ```python
   def draw(self, context):
       layout = self.layout
       
       if context.object and context.object.type == 'MESH':
           # Opciones específicas para mallas
       elif context.object and context.object.type == 'CURVE':
           # Opciones específicas para curvas
       else:
           layout.label(text="Selecciona un objeto compatible")
   ```

### Propiedades

1. **Usa `ACK.PropsWrapped` para nuevos desarrollos** para aprovechar el tipado fuerte:
   ```python
   # Preferido (con tipado fuerte y API fluida)
   my_prop = ACK.PropsWrapped.Float("Mi Propiedad").default(0.5).min(0).max(1)
   
   # Menos recomendado (sin tipado fuerte)
   my_prop = ACK.Props.Float(name="Mi Propiedad", default=0.5, min=0, max=1)
   ```

2. **Organiza las propiedades en grupos** para mantener el espacio global limpio:
   ```python
   class MyAddonSettings(ACK.Register.Types.Data.PropertyGroup):
       # Propiedades relacionadas agrupadas
   ```

3. **Proporciona límites y valores predeterminados adecuados** para todas las propiedades numéricas.

4. **Usa funciones de actualización** para mantener la coherencia entre propiedades relacionadas:
   ```python
   def update_dimension(self, context):
       # Actualizar propiedades relacionadas
       if self.maintain_aspect_ratio:
           self.height = self.width / self.aspect_ratio
   
   width = ACK.PropsWrapped.Float("Ancho").update(update_dimension)
   ```

## Rendimiento y Optimización

1. **Evita cálculos pesados en bucles de dibujo** como `draw()` o `modal_update()`.

2. **Implementa la actualización condicional** en operadores modales:
   ```python
   def modal_update(self, context, event):
       if event.type == 'MOUSEMOVE':
           # Solo actualizar en eventos de ratón
           self.recalculate_values()
           context.area.tag_redraw()
       return ACK.Returns.Modal.RUNNING_MODAL
   ```

3. **Utiliza el perfilador de ACKit** para identificar cuellos de botella:
   ```python
   from ...ackit.debug import profiler
   
   @profiler.profile
   def potentially_slow_function():
       # Código a perfilar
   ```

4. **Implementa caching para cálculos costosos** que se repiten:
   ```python
   def expensive_calculation(self, obj):
       # Verificar si ya tenemos el resultado en caché
       cache_key = f"{obj.name}_{obj.data.version}"
       if cache_key in self._cache:
           return self._cache[cache_key]
       
       # Realizar el cálculo costoso
       result = perform_expensive_calculation(obj)
       
       # Guardar en caché
       self._cache[cache_key] = result
       return result
   ```

## Depuración

1. **Utiliza el sistema de logging de ACKit** en lugar de `print()`:
   ```python
   from ...ackit.debug import output
   
   # Preferido
   output.log("Procesando objeto", level='INFO')
   
   # Menos recomendado
   print("Procesando objeto")
   ```

2. **Incluye mensajes de depuración condicionales**:
   ```python
   from ...ackit.debug import output
   from ...ackit.globals import GLOBALS
   
   if GLOBALS.DEBUG_MODE:
       output.log(f"Valores de depuración: {detailed_values}")
   ```

3. **Implementa aserciones para detectar errores temprano**:
   ```python
   from ...ackit.debug import assert_utils
   
   assert_utils.assert_true(mesh.polygons, "La malla debe tener al menos un polígono")
   ```

## Compatibilidad

1. **Verifica la versión de Blender** antes de usar características específicas:
   ```python
   from ...ackit.globals import GLOBALS
   
   if GLOBALS.BLENDER_VERSION >= (4, 0, 0):
       # Código específico para Blender 4.0+
   else:
       # Código para versiones anteriores
   ```

2. **Utiliza las abstracciones de ACKit** para manejar diferencias entre versiones:
   ```python
   # ACKit se encarga de las diferencias de API entre versiones
   my_op = ACK.Register.Types.Ops.Generic()
   ```

3. **Solicita permisos explícitos** para funcionalidades sensibles en Blender 4.0+:
   ```python
   from ...ackit.utils.permissions import has_permission, request_permission
   
   if not has_permission('network'):
       if not request_permission('network', "Necesario para descargar recursos"):
           self.report({'ERROR'}, "No se puede continuar sin permisos de red")
           return ACK.Returns.Operator.CANCELLED
   ```

## Código Limpio

1. **Sigue las convenciones de nombre de Blender**:
   - `CamelCase` para clases
   - `lower_case_with_underscores` para funciones y variables
   - `UPPER_CASE` para constantes

2. **Mantén las funciones pequeñas y centradas** en una tarea específica.

3. **Incluye docstrings y comentarios** para explicar el "por qué" más que el "qué":
   ```python
   def calculate_offset(self, vertices):
       """
       Calcula el desplazamiento óptimo para los vértices.
       
       Este algoritmo usa una técnica heurística para encontrar un desplazamiento
       que minimiza la intersección con otros objetos de la escena.
       
       Args:
           vertices: Lista de vértices a desplazar.
           
       Returns:
           Vector con el desplazamiento óptimo.
       """
   ```

4. **Usa tipos de retorno explícitos** para mejorar la claridad:
   ```python
   def get_selected_vertices(self) -> list:
       # Implementación...
   ```

## Prácticas Específicas de ACKit

1. **Aprovecha los decoradores de polling** para definir cuándo están disponibles los operadores y paneles:
   ```python
   @ACK.Poll.ACTIVE_OBJECT.MESH
   @ACK.Poll.MODE.EDIT
   class EditMeshOperator(ACK.Register.Types.Ops.Generic):
       # Operador disponible solo con una malla activa en modo edición
   ```

2. **Usa los valores de retorno de ACKit** en lugar de diccionarios:
   ```python
   # Preferido
   return ACK.Returns.Operator.FINISHED
   
   # Menos recomendado
   return {'FINISHED'}
   ```

3. **Implementa manejadores de eventos con los decoradores de ACKit**:
   ```python
   @ACK.RegDeco.HANDLER.LOAD_POST(persistent=True)
   def on_file_load():
       # Código a ejecutar después de cargar un archivo
   ```

4. **Registra atajos de teclado con los decoradores de ACKit**:
   ```python
   @ACK.RegDeco.KEYMAP('3D View', 'WINDOW', 'W', 'PRESS', ctrl=True, shift=True)
   def register_my_tool_shortcut():
       return "object.my_special_tool"
   ```

## Distribución y Mantenimiento

1. **Incluye archivos README y documentación básica** para explicar el propósito y uso del addon.

2. **Mantén un registro de cambios** (CHANGELOG.md) para ayudar a los usuarios a entender las actualizaciones.

3. **Implementa pruebas básicas** para verificar que las funcionalidades críticas siguen funcionando después de cambios:
   ```python
   from ...ackit.debug import test_utils
   
   def test_basic_functionality():
       result = my_module.process_data(test_data)
       test_utils.assert_equal(result, expected_result)
   ```

4. **Mantén actualizadas las dependencias**:
   - Actualiza ACKit cuando haya nuevas versiones disponibles
   - Especifica versiones mínimas de Blender en `bl_info` o `blender_manifest.toml`

## Consejos para Addons Grandes

1. **Divide tu addon en módulos funcionales** para facilitar el mantenimiento:
   ```
   modules/
   ├── modeling/        # Herramientas de modelado
   ├── texturing/       # Herramientas de texturizado
   ├── animation/       # Herramientas de animación
   └── core/            # Funcionalidad compartida
   ```

2. **Implementa un sistema de configuración centralizado** para mantener la coherencia:
   ```python
   class AddonConfig:
       """Configuración centralizada del addon."""
       # Constantes y opciones globales
   ```

3. **Considera una arquitectura de plugins** para funcionalidades extensibles:
   ```python
   # Sistema para registrar extensiones
   class PluginRegistry:
       _plugins = {}
       
       @classmethod
       def register_plugin(cls, name, plugin_class):
           cls._plugins[name] = plugin_class
   ```

## Resumen

Seguir estas mejores prácticas te ayudará a desarrollar addons más robustos, mantenibles y eficientes con ACKit. Recuerda que estas recomendaciones son guías y no reglas estrictas; adapta tu enfoque según las necesidades específicas de tu proyecto. 