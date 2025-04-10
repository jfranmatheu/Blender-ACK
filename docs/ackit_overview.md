# ACKit - Addon Creator Kit

## Visión General

ACKit (Addon Creator Kit) es un framework integral para el desarrollo de addons en Blender, diseñado para simplificar y agilizar el proceso de creación de extensiones para Blender. El módulo proporciona una capa de abstracción sobre la API nativa de Blender (bpy), ofreciendo un conjunto de herramientas y utilidades que facilitan tareas comunes en el desarrollo de addons.

## Propósito

El objetivo principal de ACKit es resolver varios desafíos comunes en el desarrollo de addons para Blender:

1. **Simplificación del registro de clases**: Automatiza el proceso de registro y desregistro de clases de Blender (operadores, paneles, menús, etc.).
2. **Gestión modular**: Facilita la organización del código en módulos que pueden ser cargados y registrados automáticamente.
3. **Tipado fuerte**: Proporciona anotaciones de tipo y wrappers que mejoran la experiencia de desarrollo con Python.
4. **Patrones consistentes**: Establece patrones de diseño y convenciones para mantener una estructura de código coherente.
5. **Generación automática de código**: Incluye herramientas para generar código repetitivo automáticamente.

## Integración con Blender y el Addon

ACKit se integra con Blender y con el resto del addon a través de varios mecanismos:

### 1. Sistema de Registro

El núcleo de ACKit es su sistema de registro, que maneja la inicialización, registro y desregistro de todas las clases y módulos del addon. Este sistema tiene dos implementaciones principales:

- **AddonLoader**: Sistema moderno recomendado para la carga de módulos y registro de clases.
- **AutoLoad**: Sistema legacy para compatibilidad con código anterior.

### 2. API Unificada

La clase principal `ACK` proporciona una API unificada para acceder a todas las funcionalidades del framework, incluyendo:

- Wrappers tipados para clases de Blender (`ACK.Register.Types`)
- Funciones helper para registro de propiedades (`ACK.Register.Property`, `ACK.Register.Properties`)
- Generadores de clases desde funciones (`ACK.Register.FromFunction`)
- Constantes y enumeraciones para operaciones comunes (`ACK.Returns`, `ACK.Props`, `ACK.Flags`)

### 3. Gestión Global

El módulo `globals.py` define variables y constantes globales que son utilizadas a través de todo el addon, facilitando el acceso a información del addon, rutas de archivos y configuraciones.

### 4. Compatibilidad con Extension Platform (Blender 4.x)

ACKit está diseñado para ser compatible con el nuevo sistema de Extension Platform introducido en Blender 4.0, que utiliza archivos `blender_manifest.toml` en lugar del tradicional `bl_info` en `__init__.py`.

## Cómo Utilizar ACKit en un Addon

Para implementar ACKit en un addon para Blender, se siguen estos pasos básicos:

1. **Inicialización en el archivo `__init__.py` principal**:
   ```python
   from ackit.registry import AddonLoader
   
   # En la función principal del módulo
   def register():
       AddonLoader.register_modules()
   
   def unregister():
       AddonLoader.unregister_modules()
   ```

2. **Definición de clases utilizando los wrappers de ACKit**:
   ```python
   from ackit._ack import ACK
   
   class MyOperator(ACK.Register.Types.Ops.Generic):
       bl_idname = "mymod.my_operator"
       bl_label = "Mi Operador"
       
       def execute(self, context):
           # Implementación...
           return ACK.Returns.Operator.FINISHED
   ```

3. **Organización modular del código**:
   El addon se estructura en módulos que son descubiertos y cargados automáticamente por el sistema de AddonLoader.

ACKit proporciona un marco robusto y flexible para el desarrollo de addons de Blender, simplificando tareas complejas y promoviendo buenas prácticas de desarrollo. 