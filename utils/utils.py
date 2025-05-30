import re

# Windows reserved filenames (case-insensitive)
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

def sanitize_filename(name: str, replace_spaces: bool = True) -> str:
    """
    Sanitize a string to be safely used as a filename across platforms.
    
    Args:
        name (str): Input string (e.g. model name).
        replace_spaces (bool): Whether to replace spaces with underscores.

    Returns:
        str: A safe filename string.
    """
    # Replace slashes with underscores
    name = name.replace("/", "_").replace("\\", "_")
    
    # Optionally replace spaces
    if replace_spaces:
        name = name.replace(" ", "_")

    # Remove invalid characters
    name = re.sub(r'[<>:"|?*]', '', name)

    # Strip leading/trailing dots and whitespace
    name = name.strip().strip(".")

    # Avoid Windows reserved names
    if name.upper() in WINDOWS_RESERVED_NAMES:
        name = f"_{name}"

    # If still empty or only unsafe, return fallback
    return name or "unnamed"
