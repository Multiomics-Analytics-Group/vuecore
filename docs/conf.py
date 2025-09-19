# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import nltk

# Make sure stopwords are available for autodoc
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
from importlib import metadata
from pathlib import Path

# -- Project information -----------------------------------------------------

project = "vuecore"
copyright = "2024, Multiomics-Analytics-Group"
author = (
    "Multiomics-Analytics-Group, Sebastián Ayala Ruano, Henry Webel, Alberto Santos"
)
PACKAGE_VERSION = metadata.version("vuecore")
version = PACKAGE_VERSION
release = PACKAGE_VERSION


# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_new_tab_link",
    "myst_nb",
    "sphinx_copybutton",
    "sphinxcontrib.autodoc_pydantic",
]

#  https://myst-nb.readthedocs.io/en/latest/computation/execute.html
nb_execution_mode = "auto"

myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence"]

# Plolty support through require javascript library
# https://myst-nb.readthedocs.io/en/latest/render/interactive.html#plotly
# html_js_files = [
# ]
# Set the Plotly renderer to notebook for ReadTheDocs (visualize plotly figures
# in the documentation) - needed for plotly6
# Plotly normally decides itself fine which renderer to use, so keep it to Sphinx
# see https://plotly.com/python/renderers/#setting-the-default-renderer
os.environ["PLOTLY_RENDERER"] = "notebook"

# https://myst-nb.readthedocs.io/en/latest/configuration.html
# Execution
nb_execution_raise_on_error = True
# Rendering
nb_merge_streams = True
# maximum execution time per cell in seconds
nb_execution_timeout = 120

# https://myst-nb.readthedocs.io/en/latest/authoring/custom-formats.html#write-custom-formats
# ! if you use it, then you cannot directly execute the notebook in the browser in colab
# (the file needs to be fetched from the repository)
# just keep both syncing it using papermill
# nb_custom_formats = {".py": ["jupytext.reads", {"fmt": "py:percent"}]}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "jupyter_execute",
    "conf.py",
]

# Intersphinx options
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "pyvis": ("https://pyvis.readthedocs.io/en/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    # "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# Options for the autodoc_pydantic extension
autodoc_pydantic_field_show_default = True
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_model_signature_prefix = "class"
autodoc_pydantic_field_signature_prefix = "attribute"
autodoc_pydantic_field_show_required = True
autodoc_pydantic_field_show_optional = True
autodoc_pydantic_field_show_default = True
autodoc_pydantic_field_doc_policy = "description"
autodoc_pydantic_model_member_order = "bysource"
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_summary = False
autodoc_pydantic_model_hide_paramlist = False
autodoc_pydantic_field_list_validators = False

# Options for the autodoc extension
autodoc_default_options = {
    "inherited-members": "BaseModel",
    "show-inheritance": True,
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# See:
# https://github.com/executablebooks/MyST-NB/blob/master/docs/conf.py
# html_title = ""
html_theme = "sphinx_book_theme"
html_logo = "images/logo/vuecore_logo.svg"
html_favicon = "images/logo/vuecore_logo_small.svg"
html_theme_options = {
    "github_url": "https://github.com/Multiomics-Analytics-Group/vuecore",
    "repository_url": "https://github.com/Multiomics-Analytics-Group/vuecore",
    "repository_branch": "main",
    "home_page_in_toc": True,
    "path_to_docs": "docs",
    "show_navbar_depth": 1,
    "use_edit_page_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    "launch_buttons": {
        "colab_url": "https://colab.research.google.com"
        #     "binderhub_url": "https://mybinder.org",
        #     "notebook_interface": "jupyterlab",
    },
    "navigation_with_keys": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


# -- Setup for sphinx-apidoc -------------------------------------------------

# Read the Docs doesn't support running arbitrary commands like tox.
# sphinx-apidoc needs to be called manually if Sphinx is running there.
# https://github.com/readthedocs/readthedocs.org/issues/1139

if os.environ.get("READTHEDOCS") == "True":

    PROJECT_ROOT = Path(__file__).parent.parent
    PACKAGE_ROOT = PROJECT_ROOT / "src" / "vuecore"

    def run_split_readme(_):
        print("[conf.py] Splitting README.md into sections...")
        from split_readme import process_readme

        readme_path = PROJECT_ROOT / "README.md"
        output_dir = PROJECT_ROOT / "docs" / "sections_readme"
        process_readme(readme_path, output_dir)

    def run_apidoc(_):
        from sphinx.ext import apidoc

        apidoc.main(
            [
                "--force",
                "--implicit-namespaces",
                "--module-first",
                "--separate",
                "-o",
                str(PROJECT_ROOT / "docs" / "reference"),
                str(PACKAGE_ROOT),
                str(PACKAGE_ROOT / "*.c"),
                str(PACKAGE_ROOT / "*.so"),
            ]
        )

    def setup(app):
        app.connect("builder-inited", run_split_readme)
        app.connect("builder-inited", run_apidoc)
