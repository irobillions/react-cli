import re
from typing import Literal

GeneratorKind = Literal[
    "component",
    "service",
    "hook",
    "redux",
    "context",
]


def to_pascal_case(name: str) -> str:
    """Convert a name to PascalCase without removing digits."""
    normalized_name = re.sub(r"[-_\s]+", " ", name.strip())
    separated_name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", normalized_name)
    return "".join(word.capitalize() for word in separated_name.split())


def to_camel_case(name: str) -> str:
    """Convert a name to camelCase."""
    pascal_name = to_pascal_case(name)
    if not pascal_name:
        return ""
    return pascal_name[0].lower() + pascal_name[1:]


def remove_suffix_case_insensitive(value: str, suffix: str) -> str:
    """Remove a suffix without considering letter case."""
    if value.lower().endswith(suffix.lower()):
        return value[: -len(suffix)]
    return value


def format_name(name: str, kind: GeneratorKind) -> tuple[str, str, str]:
    """Return the (formatted, PascalCase, camelCase) names for a schematic."""
    base_name = name.strip()

    if kind == "hook":
        # Strip "use" only when it is a real hook prefix: useCounter -> Counter,
        # but user -> user (next char is lowercase, so it's not a prefix).
        if (
            len(base_name) > 3
            and base_name[:3].lower() == "use"
            and base_name[3].isupper()
        ):
            base_name = base_name[3:]
    elif kind == "service":
        base_name = remove_suffix_case_insensitive(base_name, "service")
    elif kind == "redux":
        base_name = remove_suffix_case_insensitive(base_name, "slice")
    elif kind == "context":
        base_name = remove_suffix_case_insensitive(base_name, "context")
    elif kind != "component":
        raise ValueError(f"Unsupported generator kind: {kind}")

    if not base_name:
        raise ValueError("The name cannot be empty after normalization.")

    pascal_name = to_pascal_case(base_name)
    # camel derives directly from pascal no need to recompute to_pascal_case.
    camel_name = pascal_name[0].lower() + pascal_name[1:] if pascal_name else ""

    if kind == "hook":
        formatted_name = "use" + pascal_name
    elif kind == "service":
        formatted_name = pascal_name + "Service"
    elif kind == "redux":
        formatted_name = camel_name + "Slice"
    elif kind == "context":
        formatted_name = pascal_name + "Context"
    else:
        formatted_name = pascal_name

    return formatted_name, pascal_name, camel_name