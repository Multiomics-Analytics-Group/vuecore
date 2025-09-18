## VueCore Documentation
<!-- https://myst-parser.readthedocs.io/en/latest/faq/index.html
#include-a-file-from-outside-the-docs-folder-like-readme-md -->

```{include} ./sections_readme/home_page.md
:relative-docs: docs
:relative-images:
```

```{toctree} 
:maxdepth: 1
:caption: Overview

sections_readme/about
sections_readme/installation
sections_readme/execution
sections_readme/license
```

```{toctree}
:maxdepth: 1
:caption: API Usage Examples

api_examples/scatter_plot
api_examples/line_plot
api_examples/bar_plot
api_examples/box_violin_plot
api_examples/histogram_plot
```

```{toctree}
:maxdepth: 2
:caption: API Reference
:hidden:

reference/vuecore
```

```{toctree} 
:maxdepth: 1
:caption: Project Support

sections_readme/contributing
sections_readme/credits
sections_readme/contact
sections_readme/changelog
```

```{toctree}
:maxdepth: 1
:caption: Extra Materials
:hidden:

README.md
```
