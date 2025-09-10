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


# --- Test for the Decorator ---
def test_decorator_modifies_docstring():
    """Verify the decorator correctly adds model parameters to the docstring."""
    # Define the expected docstring
    expected_docstring = """
    This is the original docstring.

    Parameters
    ----------
    data : dict
        A dictionary of sample data.
    
    **kwargs
        Keyword arguments for plot configuration. These arguments are validated against
        the ``TestModel`` Pydantic model and the engine specific parameters.
        
        The following parameters are supported:
        
        * **param_str** (str) – A string parameter. (default: ``PydanticUndefined``)
        * **param_int** (int) – An integer parameter with a default. (default: ``5``)
        * **param_list** (list of str) – An optional list of strings.
        * **param_dict** (dict) – A generic dictionary parameter. (default: ``{}``)
        * **param_bare_list** (list) – A bare list parameter. (default: ``[]``)
    Returns
    -------
    None
        Does not return anything.
    """
    # Dedent the expected docstring for accurate comparison
    expected_docstring = textwrap.dedent(expected_docstring).strip()

    # Get the decorated function's docstring and dedent it before comparison
    decorated_docstring = textwrap.dedent(dummy_plot_function.__doc__).strip()

    # Assert that the docstrings are a perfect match
    assert decorated_docstring == expected_docstring
