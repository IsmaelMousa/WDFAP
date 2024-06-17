import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = 'WDFAP'
copyright = '2024, Ismael Mousa'
author = 'Ismael Mousa'
release = '1.1.0'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'press'
html_static_path = ['_static']
