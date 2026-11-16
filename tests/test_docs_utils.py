import inspect
import typing

import pytest
import textwrap
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Import the decorator and helper functions from your module
from vuecore.utils.docs_utils import (
    document_pydant_params,
    get_type_string,
    get_all_model_fields,
)


# --- Test Model and Function ---
# Pydantic model with different field types for validation
class TestModel(BaseModel):
    """A test model for decorator documentation."""

    param_str: str = Field(..., description="A string parameter.")
    param_int: int = Field(5, description="An integer parameter with a default.")
    param_list: Optional[List[str]] = Field(
        None, description="An optional list of strings."
    )
    param_dict: Dict = Field({}, description="A generic dictionary parameter.")
    param_bare_list: list = Field([], description="A bare list parameter.")


# Function to apply the decorator to and check its docstring
@document_pydant_params(TestModel)
def dummy_plot_function(data: dict):
    """
    This is the original docstring.

    Parameters
    ----------
    data : dict
        A dictionary of sample data.

    Returns
    -------
    None
        Does not return anything.
    """
    pass


# --- Tests for Helper Functions ---
def test_get_all_model_fields():
    """Verify that all fields, including inherited ones, are correctly extracted."""
    fields = get_all_model_fields(TestModel)
    assert "param_str" in fields
    assert "param_int" in fields
    assert "param_list" in fields
    assert "param_dict" in fields
    assert "param_bare_list" in fields
    assert len(fields) == 5


@pytest.mark.parametrize(
    "annotation, expected_string",
    [
        (str, "str"),
        (int, "int"),
        (Optional[str], "str"),
        (List[str], "list of str"),
        (Dict, "dict"),
        (list, "list"),
        (Dict[str, int], "Dict[str, int]"),
    ],
)
def test_get_type_string(annotation, expected_string):
    """Test that the type string is correctly formatted for various types."""
    assert get_type_string(annotation) == expected_string


# --- Tests for the Decorator ---
def test_decorator_keeps_the_original_docstring_sections():
    """The summary, the function's own parameters and Returns are kept."""
    docstring = dummy_plot_function.__doc__

    assert "This is the original docstring." in docstring
    assert "data : dict" in docstring
    assert "A dictionary of sample data." in docstring
    assert "Returns" in docstring
    assert "Does not return anything." in docstring


def test_decorator_documents_each_field_as_a_parameter_entry():
    """Each field is a numpydoc entry in the Parameters section, before Returns."""
    docstring = dummy_plot_function.__doc__

    assert "param_str : str\n    A string parameter." in docstring
    assert (
        "param_int : int, optional\n"
        "    An integer parameter with a default. Defaults to ``5``." in docstring
    )
    assert (
        "param_list : list of str, optional\n    An optional list of strings."
        in docstring
    )
    assert (
        "param_dict : dict, optional\n"
        "    A generic dictionary parameter. Defaults to ``{}``." in docstring
    )
    assert docstring.index("param_bare_list : list") < docstring.index("Returns")
    assert "**kwargs\n    Further keyword arguments" in docstring


def test_decorator_adds_a_parameters_section_when_there_is_none():
    """A docstring without a Parameters section gets one."""

    @document_pydant_params(TestModel)
    def plot_without_parameters_section():
        """Summary line."""

    docstring = plot_without_parameters_section.__doc__

    assert docstring.startswith("Summary line.\n\nParameters\n----------\n")
    assert "param_int : int, optional" in docstring


def test_decorator_lists_the_fields_as_keyword_only_signature_parameters():
    """The signature shows every field, with its default, before **kwargs."""
    signature = inspect.signature(dummy_plot_function)
    parameters = signature.parameters

    assert list(parameters) == [
        "data",
        "param_str",
        "param_int",
        "param_list",
        "param_dict",
        "param_bare_list",
    ]
    assert parameters["param_str"].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters["param_str"].default is inspect.Parameter.empty
    assert parameters["param_int"].default == 5
    assert parameters["param_list"].default is None


def test_decorator_keeps_var_keyword_last_when_the_function_has_one():
    """A function taking **kwargs still accepts the model's extra arguments."""

    @document_pydant_params(TestModel)
    def plot_with_kwargs(data: dict, **kwargs):
        """Summary line."""

    parameters = list(inspect.signature(plot_with_kwargs).parameters.values())

    assert parameters[-1].name == "kwargs"
    assert parameters[-1].kind is inspect.Parameter.VAR_KEYWORD
    assert parameters[1].name == "param_str"


def test_decorator_exposes_the_field_types_to_get_type_hints():
    """Tools that read type hints see the fields' real types."""

    hints = typing.get_type_hints(dummy_plot_function)

    assert hints["param_int"] is int
    assert hints["param_list"] == Optional[List[str]]


def test_decorator_leaves_the_undecorated_function_alone():
    """The wrapped function keeps its own annotations and still runs."""

    def undecorated(data: dict, **kwargs):
        """Summary line."""
        return kwargs

    decorated = document_pydant_params(TestModel)(undecorated)

    assert "param_int" not in undecorated.__annotations__
    assert decorated({}, param_int=3) == {"param_int": 3}


def test_decorator_skips_a_field_the_function_already_has():
    """A field named like an existing parameter does not replace it."""

    @document_pydant_params(TestModel)
    def plot_with_same_name(data: dict, param_int: str = "own", **kwargs):
        """Summary line."""

    parameter = inspect.signature(plot_with_same_name).parameters["param_int"]

    assert parameter.default == "own"
    assert parameter.annotation is str
