project = 'WDFAP'
copyright = '2024, Ismael Mousa'
author = 'Ismael Mousa'
release = '1.1.0'

extensions = ['myst_parser',
              'sphinx.ext.githubpages']

myst_enable_extensions = ["deflist"]

source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

html_theme = 'piccolo_theme'
html_static_path = ['_static']
