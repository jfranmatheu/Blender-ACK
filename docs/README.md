# Documentación de ACKit

Este directorio contiene la documentación oficial de ACKit generada con Sphinx y ReadTheDocs.

## Estructura

La documentación está organizada en las siguientes secciones:

- **Guías**: Documentos conceptuales y guías generales para entender y usar ACKit.
- **Tutoriales**: Ejemplos prácticos paso a paso para aprender a usar ACKit.
- **API**: Documentación detallada de las clases, funciones y módulos de ACKit.
- **Referencia**: Documentos técnicos, análisis y mejores prácticas.
  - **Mejores Prácticas**: Guía completa sobre patrones y prácticas recomendadas para el desarrollo de addons con ACKit. Incluye consejos sobre estructura del proyecto, patrones de importación, gestión del ciclo de vida, tipos de operadores, diseño de interfaces, gestión de propiedades, optimización de rendimiento y técnicas de depuración.

## Compilar la Documentación

Para compilar localmente la documentación:

1. Instala los requisitos:
   ```
   pip install -r docs/requirements.txt
   ```

2. Genera la documentación HTML:
   ```
   cd docs
   make html
   ```

3. Los archivos generados estarán en el directorio `_build/html`.

## Convenciones de Documentación

- Utiliza encabezados de nivel 1 (`#`) solo para el título principal del documento.
- Utiliza encabezados de nivel 2 (`##`) para las secciones principales.
- Incluye ejemplos de código con bloques de código delimitados por triple backtick.
- Sigue el formato de docstrings de Google para la documentación de API.

## Contribuir a la Documentación

1. Clona el repositorio.
2. Crea una rama para tus cambios.
3. Realiza tus modificaciones siguiendo las convenciones de estilo.
4. Envía un pull request con tus cambios.

## Licencia

La documentación está bajo la misma licencia que ACKit (GPL v3). 