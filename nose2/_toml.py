from __future__ import annotations

import types

TOML_ENABLED: bool = False
toml: types.ModuleType | None = None

try:
    import tomllib as toml

    TOML_ENABLED = True
except ImportError:
    try:
        import tomli as toml

        TOML_ENABLED = True
    except ImportError:
        toml = None
        TOML_ENABLED = False


def load_toml(file: str) -> dict:
    if toml is None:
        raise RuntimeError("toml library not found. Please install 'tomli'.")
    with open(file, "rb") as fp:
        return toml.load(fp)
