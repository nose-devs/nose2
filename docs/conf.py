import os
import sys

import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath(".."))
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "nose2.sphinxext",
]
source_suffix = ".rst"
master_doc = "index"
project = "nose2"
copyright = "2010, Jason Pellerin"
version = "0.6"
release = "0.6.0"
exclude_patterns = ["_build"]
templates_path = ["_templates"]
pygments_style = "sphinx"
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
man_pages = [("index", "nose2", "nose2 Documentation", ["Jason Pellerin"], 1)]
intersphinx_mapping = {"python": ("http://docs.python.org/", None)}
