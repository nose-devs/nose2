TOML_ENABLED: bool = False

try:
    import tomllib as toml

    TOML_ENABLED = True
except ImportError:
    try:
        import tomli as toml

        TOML_ENABLED = False
    except ImportError:
        toml = None
        TOML_ENABLED = False


def load_toml(file: str) -> dict:
    if not TOML_ENABLED:
        raise RuntimeError("toml library not found. Please install 'tomli'.")
    with open(file, "rb") as fp:
        return toml.load(fp)
