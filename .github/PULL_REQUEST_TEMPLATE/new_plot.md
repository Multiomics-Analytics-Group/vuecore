<!--
Please complete the following sections when you submit your pull request. Note that text within html comment tags will not be rendered.
-->
### Description

Add the [PlotName] plot to VueCore.

### Tasks Checklist

- [ ] Create **Pydantic schema** in the `vuecore/schemas` folder. It should be aligned with the [plotly API](https://plotly.com/python-api-reference/index.html)
- [ ]  Create a script with a **build function** in the `vuecore/engines/plotly` folder
- [ ] Update `theming.py` script in the `vuecore/engines/plotly` folder
- [ ] Add the new plot in the **PlotType StrEnum** of the `vuecore/constants.py` script, and register the new **builder** in the `__init__.py` script of the `vuecore/engines/plotly` folder
- [ ] Create a script with the **user-facing function** in the `vuecore/plots` folder. It gathers the Pydantic schema, builder function, and saves the plot
- [ ] Create an **api example jupyter notebook** in the `docs/api_examples folder`
- [ ] Use **jupytext** to sync the Jupyter notebook with a Python script
- [ ] Update `index.md` file in the `docs` folder with the new example
- [ ] Create **test script** in the `/test` folder with the code from the example
