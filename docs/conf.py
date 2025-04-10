import os
import sys
import datetime

# Project information
project = 'ACKit - Addon Creator Kit'
copyright = f'{datetime.datetime.now().year}, JFranMatheu'
author = 'JFranMatheu'
version = '0.1.0'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['css/custom.css']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'style_nav_header_background': '#343131',
    'navigation_depth': 4,
}

# Internationalization
language = 'es'

# Extension configuration
todo_include_todos = True
autosectionlabel_prefix_document = True
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'
add_module_names = False

# Intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'blender': ('https://docs.blender.org/api/current/', None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False 