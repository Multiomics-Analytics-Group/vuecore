# DataFrame

Each specific analysis plot is based on a type from acore `acore.types`. Use the pandera
schema to validate the input DataFrame.

- use the pandas API whenever you can

## Format

Use black to format the src folder

```bash
black src
```

## Ruff checks

```
ruff check src --fix
```

## Staging

Ask me if I want to stage the files and provide the command to do so.

## Docstrings

Use the default format for type annotated functions is numpy style.

https://numpydoc.readthedocs.io/en/latest/format.html#parameters

## Module functions

`static.py` import the matplotlib related functions and `interactive.py` import the
plotly related functions. The main module `vuecore.py` imports all functions from the two
submodules and provides a unified interface for the user.
