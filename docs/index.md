# ACKit - Addon Creator Kit

[![Blender Version](https://img.shields.io/badge/Blender-4.0%2B-orange)](https://www.blender.org/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL%20v3-green)](https://www.gnu.org/licenses/gpl-3.0.html)

**ACKit** (Addon Creator Kit) es un framework moderno y tipado para el desarrollo de addons para Blender. Proporciona una capa de abstracción sobre la API de Blender que facilita la creación de addons robustos, mantenibles y bien estructurados.

## Características Principales

- **API Tipada:** Todas las interfaces están completamente tipadas para proporcionar mejor autocompletado e información en IDEs.
- **Sistema de Registro Automatizado:** Registro y desregistro de clases y funciones sin código boilerplate.
- **Decoradores Potentes:** Decoradores para simplificar tareas comunes como polling, flags y handlers.
- **Propiedades Mejoradas:** Sistema de propiedades con sintaxis fluida y validación.
- **Generación Automática de Código:** Generación automática de helpers y constantes.
- **Compatibilidad con Extension Platform:** Soporte para el nuevo sistema de extensiones de Blender 4.0+.

## Instalación

ACKit está diseñado para ser incluido como un submódulo dentro de tu propio addon:

```bash
# En la raíz de tu addon
git submodule add https://github.com/jfranmatheu/Blender-ACKit.git ackit
```

## Inicio Rápido

```python
from .ackit import ACK, AddonLoader, AutoCode

# Inicialización
AddonLoader.init_modules(
    auto_code={AutoCode.OPS, AutoCode.ICONS, AutoCode.TYPES}
)

def register():
    AddonLoader.register_modules()

def unregister():
    AddonLoader.unregister_modules()
```

## Ejemplos de Uso

### Operador Simple
```python
from ...ackit import ACK

@ACK.Poll.ACTIVE_OBJECT.MESH
class MyOperator(ACK.Register.Types.Ops.Action):
    label = "Mi Operador"
    
    # Propiedades tipadas
    value = ACK.PropsWrapped.Float("Valor").default(0.5).min(0.0).max(1.0)
    
    def action(self, context):
        self.report_info(f"Valor: {self.value}")
```

### Panel UI
```python
from ...ackit import ACK

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="Mi Addon")
def my_panel(context, layout):
    layout.operator('object.my_operator')
```

## Tabla de Contenidos

```{toctree}
:maxdepth: 2
:caption: Guías

guides/quickstart
guides/getting-started
guides/registration
guides/addon-structure
guides/extension-platform
```

```{toctree}
:maxdepth: 2
:caption: Tutoriales

tutorials/basic-operator
tutorials/ui-creation
tutorials/modal-operators
tutorials/properties
tutorials/node-system
```

```{toctree}
:maxdepth: 2
:caption: Referencia API

api/overview
api/ack
api/register
api/properties
api/polling
api/decorators
api/utils
api/debug
```

```{toctree}
:maxdepth: 1
:caption: Recursos Adicionales

reference/ackit-structure
reference/analysis
reference/best-practices
reference/faq
```

## Índices y Tablas

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search` 