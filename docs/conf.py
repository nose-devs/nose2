import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import nose2  # noqa:E402

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx_issues",
    "nose2.sphinxext",
]

source_suffix = ".rst"
master_doc = "index"
project = "nose2"
copyright = "2010-2022, Jason Pellerin, Stephen Rosen"
version = release = nose2.__version__
exclude_patterns = ["_build"]
templates_path = ["_templates"]

# theme
html_theme = "sphinx_rtd_theme"

# sphinx-issues
github_user = "nose-devs"
github_repo = "nose2"
issues_github_path = f"{github_user}/{github_repo}"
# intersphinx
intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
}
