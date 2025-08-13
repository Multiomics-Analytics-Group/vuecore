<!-- https://myst-parser.readthedocs.io/en/latest/faq/index.html
#include-a-file-from-outside-the-docs-folder-like-readme-md -->

```{include} ../README.md
:start-line: 0
:relative-docs: docs
:relative-images:
```

```{toctree}
:maxdepth: 1
:caption: API Usage Examples

api_examples/scatter_plot
api_examples/line_plot
```

```{toctree}
:maxdepth: 2
:caption: API Reference
:hidden:

reference/vuecore
```

```{toctree}
:maxdepth: 1
:caption: Extra Materials
:hidden:

README.md
```
