# vuecore/utils/doc_utils.py
import inspect
import re
import textwrap
from functools import wraps
from typing import Any, Optional, Union, get_args, get_origin

from pydantic import BaseModel, Field


def get_all_model_fields(model: type[BaseModel]) -> dict[str, Field]:
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


def _config_parameters(
    model: type[BaseModel], taken_names: set[str]
) -> list[inspect.Parameter]:
    """
    Build one keyword-only parameter for each field of the model.

    Fields named like a parameter the function already has are skipped, so the
    function's own parameters keep their meaning.

    Parameters
    ----------
    model : Type[BaseModel]
        The Pydantic model whose fields become parameters.
    taken_names : set of str
        Names of the parameters the function already has.

    Returns
    -------
    list of inspect.Parameter
        The keyword-only parameters, each with the field's type and default.
    """
    parameters = []
    for field_name, field in get_all_model_fields(model).items():
        if field_name in taken_names:
            continue
        if field.is_required():
            default = inspect.Parameter.empty
        else:
            default = field.get_default(call_default_factory=True)
        parameters.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.KEYWORD_ONLY,
                default=default,
                annotation=field.annotation,
            )
        )
    return parameters


def _parameter_docs(model: type[BaseModel], taken_names: set[str]) -> list[str]:
    """
    Write the numpydoc entries for the model's fields, one per parameter.

    Parameters
    ----------
    model : Type[BaseModel]
        The Pydantic model whose fields are documented.
    taken_names : set of str
        Names of the parameters the function already documents.

    Returns
    -------
    list of str
        The entries, ending with one for the remaining ``**kwargs``.
    """
    entries = []
    for field_name, field in get_all_model_fields(model).items():
        if field_name in taken_names:
            continue
        type_str = get_type_string(field.annotation)
        optional = "" if field.is_required() else ", optional"
        description = field.description or "No description available."
        default_value = field.get_default(call_default_factory=True)
        has_shown_default = not field.is_required() and default_value is not None
        if has_shown_default:
            description = f"{description} Defaults to ``{default_value}``."
        entries.append(f"{field_name} : {type_str}{optional}")
        entries.extend(textwrap.indent(description, "    ").splitlines())
    entries.append("**kwargs")
    entries.append("    Further keyword arguments, passed on to the plotting engine.")
    return entries


def _insert_into_parameters_section(doc_lines: list[str], entries: list[str]):
    """
    Put the entries at the end of the docstring's Parameters section.

    A docstring without a Parameters section gets one, placed before the first
    section that follows the summary (Returns, Raises, Examples, See Also) or at
    the end.

    Parameters
    ----------
    doc_lines : list of str
        The docstring, dedented and split into lines.
    entries : list of str
        The entries to add.

    Returns
    -------
    list of str
        The docstring lines with the entries added.
    """
    section_header = re.compile(r"^[A-Z][A-Za-z ]*$")

    def is_header(index: int) -> bool:
        has_underline = index + 1 < len(doc_lines) and re.fullmatch(
            r"-{3,}", doc_lines[index + 1].strip()
        )
        return bool(has_underline and section_header.match(doc_lines[index]))

    parameters_start = next(
        (
            i
            for i in range(len(doc_lines))
            if doc_lines[i] == "Parameters" and is_header(i)
        ),
        None,
    )
    if parameters_start is None:
        end = next((i for i in range(len(doc_lines)) if is_header(i)), len(doc_lines))
        while end > 0 and not doc_lines[end - 1].strip():
            end -= 1
        new_section = ["", "Parameters", "----------", *entries]
        return doc_lines[:end] + new_section + [""] + doc_lines[end:]

    end = next(
        (i for i in range(parameters_start + 2, len(doc_lines)) if is_header(i)),
        len(doc_lines),
    )
    while end > 0 and not doc_lines[end - 1].strip():
        end -= 1
    return doc_lines[:end] + entries + doc_lines[end:]


def document_pydant_params(model: type[BaseModel]):
    """
    Decorator that exposes a Pydantic model's fields as the function's parameters.

    The function keeps accepting ``**kwargs``, which the plotting code validates
    against the model. The decorator makes that visible to tools that read
    the function instead of running it: ``inspect.signature`` and
    ``typing.get_type_hints`` list every model field as a keyword-only
    parameter with its type and default, and the docstring documents each field
    in its Parameters section.

    Parameters
    ----------
    model : Type[BaseModel]
        The Pydantic model class whose fields should be exposed.

    Returns
    -------
    function
        A decorator function that modifies the signature and docstring of the
        target function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        signature = inspect.signature(func)
        taken_names = set(signature.parameters)
        config_parameters = _config_parameters(model, taken_names)

        # The extra keyword arguments the model allows stay at the end.
        own_parameters = [
            parameter
            for parameter in signature.parameters.values()
            if parameter.kind != inspect.Parameter.VAR_KEYWORD
        ]
        var_keyword = [
            parameter
            for parameter in signature.parameters.values()
            if parameter.kind == inspect.Parameter.VAR_KEYWORD
        ]
        wrapper.__signature__ = signature.replace(
            parameters=own_parameters + config_parameters + var_keyword
        )

        # A copy, so the undecorated function's annotations stay as they are.
        annotations = dict(getattr(func, "__annotations__", {}))
        for parameter in config_parameters:
            annotations[parameter.name] = parameter.annotation
        wrapper.__annotations__ = annotations

        doc_lines = inspect.cleandoc(func.__doc__ or "").splitlines()
        entries = _parameter_docs(model, taken_names)
        wrapper.__doc__ = "\n".join(_insert_into_parameters_section(doc_lines, entries))
        return wrapper

    return decorator
