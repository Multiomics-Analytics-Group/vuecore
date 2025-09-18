# vuecore/utils/doc_utils.py
from typing import Type, Dict, Any, get_origin, get_args, Optional, Union
from pydantic import BaseModel, Field
from functools import wraps
import textwrap
import re


def get_all_model_fields(model: Type[BaseModel]) -> Dict[str, Field]:
    """
    Extract all fields from a Pydantic model, including inherited ones.

    Parameters
    ----------
    model : Type[BaseModel]
        The Pydantic model class from which to extract fields.

    Returns
    -------
    Dict[str, Any]
        A dictionary with field names as keys and field information as values.
    """
    fields = {}
    # Iterate through the method resolution order (mro) in reverse to start from the base classes
    for cls in reversed(model.__mro__):
        if issubclass(cls, BaseModel) and hasattr(cls, "model_fields"):
            for field_name, field in cls.model_fields.items():
                fields[field_name] = field
    return fields


def get_type_string(annotation: Any) -> str:
    """
    Helper to get a clean type string from a type annotation.

    Parameters
    ----------
    annotation : Any
        The type annotation to process.

    Returns
    -------
    str
        A simplified string representation of the type.
    """
    origin = get_origin(annotation)

    # Handle annotation with more than one type (e.g., str | bool)
    if origin is None and hasattr(annotation, "__args__"):
        args = get_args(annotation)
        if args:
            arg_strings = [get_type_string(arg) for arg in args]
            # Exclude NoneType from the list if it's an Optional
            if type(None) in args:
                return f"Optional[{' | '.join(s for s in arg_strings if s != 'None')}]"
            return " | ".join(arg_strings)

    # Handle Optional and Union types with single non-None type
    if origin is Union or origin is Optional:
        args = get_args(annotation)
        non_none_arg = next((arg for arg in args if arg is not type(None)), None)
        if non_none_arg:
            return get_type_string(non_none_arg)
        return "Any"
    elif origin is list or annotation is list:
        args = get_args(annotation)
        if not args:
            return "list"
        inner_type = ", ".join(arg.__name__ for arg in args)
        return f"list of {inner_type}"
    elif origin is dict or annotation is dict:
        args = get_args(annotation)
        if not args:
            return "dict"
        key_type_str = get_type_string(args[0])
        value_type_str = get_type_string(args[1])
        return f"Dict[{key_type_str}, {value_type_str}]"

    # Fallback for primitives and other types
    if hasattr(annotation, "__name__"):
        return annotation.__name__

    return str(annotation)


def document_pydant_params(model: Type[BaseModel]):
    """
    Decorator to add Pydantic model parameters to a function's docstrings.

    Parameters
    ----------
    model : Type[BaseModel]
        The Pydantic model class whose fields should be documented.

    Returns
    -------
    function
        A decorator function that modifies the docstring of the target function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        original_doc = wrapper.__doc__ or ""
        lines = original_doc.splitlines()

        # Find the end of the "Parameters" section
        insert_index = -1
        # Find the line that marks the end of the Parameters section
        # or the beginning of a new section like Returns or Raises
        for i, line in enumerate(lines):
            if re.match(r"^\s*(Returns|Raises|Examples|See Also)", line):
                insert_index = i
                break

        # If no other section is found, assume the end of the docstring
        if insert_index == -1:
            insert_index = len(lines)

        # Generate the new, detailed parameter list in NumPydocs style
        fields = get_all_model_fields(model)
        params_doc_lines = []
        for field_name, field in fields.items():
            type_str = get_type_string(field.annotation)
            description = field.description or "No description available."
            default_value = field.get_default(call_default_factory=True)
            default_str = (
                f" (default: ``{default_value}``)"
                if default_value is not None and default_value is not ...
                else ""
            )

            # Format as a single line for the NumPy-style bulleted list
            params_doc_lines.append(
                f"* **{field_name}** ({type_str}) – {description}{default_str}"
            )

            # Indent all lines in the parameter list correctly
            indented_params_lines = textwrap.indent(
                "\n".join(params_doc_lines), prefix="        "
            ).splitlines()

        # Create the kwargs documentation as a list of lines
        new_kwargs_lines = [
            "    **kwargs",
            "         Keyword arguments for plot configuration. These arguments are validated against",
            f"        the ``{model.__name__}`` Pydantic model and the engine specific parameters.\n",
            "        The following parameters are supported:\n",
        ]

        # Add all parameter lines
        new_kwargs_lines.extend(indented_params_lines)

        # Reconstruct the docstring by inserting the new lines
        new_doc_lines = lines[:insert_index] + new_kwargs_lines + lines[insert_index:]
        wrapper.__doc__ = "\n".join(new_doc_lines)
        return wrapper

    return decorator
