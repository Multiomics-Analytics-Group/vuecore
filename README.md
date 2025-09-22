## ![VueCore Logo](https://raw.githubusercontent.com/Multiomics-Analytics-Group/vuecore/HEAD/docs/images/logo/vuecore_logo.svg)

<p align="center">
   VueCore is a Python package for creating interactive and static visualizations of multi-omics data
</p>

| Information           | Links                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Package**           | [![PyPI Latest Release](https://img.shields.io/pypi/v/vuecore.svg)][vuecore-pypi] [![Supported versions](https://img.shields.io/pypi/pyversions/vuecore.svg)][vuecore-pypi] [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)][gpl-license] |
| **Documentation**     | [![View - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=flat)][vuecore-docs] [![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/) ![Docs](https://readthedocs.org/projects/vuecore/badge/?style=flat) [![CC BY 4.0][cc-by-shield]][vuecore-license]|
| **Build**             | [![CI](https://github.com/Multiomics-Analytics-Group/vuecore/actions/workflows/cdci.yml/badge.svg)][ci-gh-action]|                                                                                     
| **Discuss on GitHub** | [![GitHub issues](https://img.shields.io/github/issues/Multiomics-Analytics-Group/vuecore)][issues] [![GitHub pull requests](https://img.shields.io/github/issues-pr/Multiomics-Analytics-Group/vuecore)][pulls]|

## Table of contents:

- [About the project](#about-the-project)
- [Installation](#installation)
- [Documentation](#documentation)
- [License](#license)
- [Contributing](#contributing)
- [Credits and acknowledgements](#credits-and-acknowledgements)
- [Contact and feedback](#contact-and-feedback)

## About the project

VueCore is part of a broader ecosystem of tools for multi-omics analysis, working in conjunction with [ACore][acore] and [VueGen][vuegen] to enable end-to-end data processing, visualization, and reporting.

## Installation

> [!TIP]
> It is recommended to install VueCore inside a virtual environment to manage depenendencies and avoid conflicts with existing packages. You can use the virtual environment manager of your choice, such as `poetry`, `conda`, or `pipenv`.

### Pip

VueCore is available on [PyPI][vuecore-pypi] and can be installed using pip:

```bash
pip install vuecore
```

You can also install the package for development by cloning this repository and running the following command:

> [!WARNING]
> We assume you are in the root directory of the cloned repository when running this command. Otherwise, you need to specify the path to the `vuecore` directory.

```bash
pip install -e .
```

## Documentation

VueCore's documentation is hosted on [Read the Docs][vuecore-docs]. It includes detailed examples for every plot type, configuration options, and the API reference. It is designed to help you with creating visualizations for your multi-omics data.

## License

The code in this repository is licensed under the **MIT License**, allowing you to use, modify, and distribute it freely as long as you include the original copyright and license notice.

The documentation and other creative content are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0) License**, meaning you are free to share and adapt it with proper attribution.

Full details for both licenses can be found in the [LICENSE][vuecore-license] file.

## Contributing

VueCore is an open-source project, and we welcome contributions of all kinds via GitHub issues and pull requests. You can report bugs, suggest improvements, propose new features, or implement changes. 

We follow the [Conventional Commits][conventional-commits] specification for commit messages and use the [changelog-from-release][changelog-from-release-repo] tool to automatically generate the [CHANGELOG](CHANGELOG.md).

Please follow the guidelines in the [CONTRIBUTING](CONTRIBUTING.md) file to ensure that your contribution is easily integrated into the project.

## Credits and acknowledgements

- VueCore was developed by the [Multiomics Network Analytics Group (MoNA)][Mona] at the [Novo Nordisk Foundation Center for Biosustainability (DTU Biosustain)][Biosustain].

## Contact and feedback

We appreciate your feedback! If you have any comments, suggestions, or run into issues while using VueCore, feel free to [open an issue][new-issue] in this repository. Your input helps us make VueCore better for everyone.


[vuecore-pypi]: https://pypi.org/project/vuecore/
[vuecore-license]: https://github.com/Multiomics-Analytics-Group/vuecore/blob/main/LICENSE.md
[vuecore-docs]: https://vuecore.readthedocs.io/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
[gpl-license]: https://www.gnu.org/licenses/gpl-3.0
[ci-gh-action]: https://github.com/Multiomics-Analytics-Group/vuecore/actions/workflows/cdci.yml
[issues]: https://github.com/Multiomics-Analytics-Group/vuecore/issues
[pulls]: https://github.com/Multiomics-Analytics-Group/vuecore/pulls
[vuegen]: https://github.com/Multiomics-Analytics-Group/vuegen
[acore]: https://github.com/Multiomics-Analytics-Group/acore
[conventional-commits]: https://www.conventionalcommits.org/
[changelog-from-release-repo]: https://github.com/rhysd/changelog-from-release
[Mona]: https://multiomics-analytics-group.github.io/
[Biosustain]: https://www.biosustain.dtu.dk/
[new-issue]:https://github.com/Multiomics-Analytics-Group/vuecore/issues/new