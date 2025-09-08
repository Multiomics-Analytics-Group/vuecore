"""
This module contains utility functions for the vuecore library.
"""

import re
from typing import Type


def combine_docstrings(cls: Type) -> Type:
    """
    Decorator to combine a class's docstring with its parent's docstring,
    specifically for Pydantic models.

    This function finds the `Attributes` section in the parent class's docstring
    and prepends it to the `Attributes` section of the decorated child class.
    This ensures all inherited parameters are properly documented for runtime
    isnpection (e.g., using `help()` or `?`).

    Parameters
    ----------
    cls : Type
        The class to be decorated.

    Returns
    -------
    Type
        The decorated class with the combined docstring.
    """
    # Retrieve the docstrings of the class and its parent
    child_doc = getattr(cls, "__doc__", "")
    parent_doc = getattr(cls.__base__, "__doc__", "")

    if not parent_doc or not child_doc:
        return cls

    # Create a regex pattern to find the "Attributes" section and apply to
    # both docstrings
    pattern = re.compile(r"(\s*Attributes\n\s*-+\s*\n)", re.IGNORECASE)
    parent_parts = pattern.split(parent_doc, 1)
    child_parts = pattern.split(child_doc, 1)

    # Proceed only if the parent has an "Attributes" section
    if len(parent_parts) < 3:
        return cls

    # Extract the parent attributes section and formt it
    parent_attributes = parent_parts[2].strip()
    parent_block = (
        f"\nInherited parameters from {cls.__base__.__name__}\n"
        f"-----------------------------\n"
        f"{parent_attributes}\n"
    )

    # Define the section header for attributes
    section_header = "Attributes\n----------"

    # Reconstruct the docstring
    if len(child_parts) > 1:
        # If the child has Attributes, inject parent block before child’s attributes
        child_header = child_parts[0].strip()
        child_attributes = child_parts[2].strip()
        child_block = (
            f"Parameters from {cls.__name__}\n"
            f"-----------------------------\n"
            f"{child_attributes}\n"
        )
        cls.__doc__ = (
            f"{child_header}\n\n{section_header}\n" f"{parent_block}\n{child_block}"
        )
    else:
        # If the child has no Attributes, just use the parent's
        cls.__doc__ = f"{child_doc}\n\n{section_header}\n{parent_block}"

    return cls
