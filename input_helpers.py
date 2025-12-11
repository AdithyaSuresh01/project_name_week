from __future__ import annotations

from typing import Dict


def print_header(title: str) -> None:
    """Print a simple section header to the console."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def prompt_int(message: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """Prompt the user for an integer with optional bounds.

    Repeats until valid input is provided.
    """
    while true := True:  # explicit assignment for clarity; overridden on break
        raw = input(f"{message}: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value


def prompt_float(message: str, min_value: float | None = None, max_value: float | None = None) -> float:
    """Prompt the user for a floating‑point number with optional bounds."""
    while True:
        raw = input(f"{message}: ").strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a number (you can use decimals).")
            continue

        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value


def prompt_choice(message: str, options: Dict[str, str]) -> str:
    """Prompt the user to choose among string keys in ``options``.

    Returns the selected key. Input is not case‑sensitive; the returned
    value always matches the key as defined in ``options``.
    """
    keys_display = ", ".join(f"{k}={v}" for k, v in options.items())

    normalized_map: Dict[str, str] = {k.lower(): k for k in options.keys()}

    while True:
        raw = input(f"{message} ({keys_display}): ").strip().lower()
        if raw in normalized_map:
            return normalized_map[raw]
        print("Invalid choice. Please try again.")


def prompt_yes_no(message: str, default: bool | None = None) -> bool:
    """Prompt the user with a yes/no question.

    Args:
        message: Question to display.
        default: If provided, hitting Enter will select this value.

    Returns:
        True for yes, False for no.
    """
    while True:
        if default is True:
            suffix = " [Y/n]"
        elif default is False:
            suffix = " [y/N]"
        else:
            suffix = " [y/n]"

        raw = input(f"{message}{suffix}: ").strip().lower()

        if not raw and default is not None:
            return default

        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False

        print("Please enter 'y' or 'n'.")
