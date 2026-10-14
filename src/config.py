"""Парсинг аргументов командной строки."""
import argparse


def parse_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки.

    Returns:
        argparse.Namespace: объект с полями vfs и script.
    """
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС (Вариант 12)"
    )
    parser.add_argument(
        "--vfs",
        type=str,
        default=None,
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Путь к стартовому скрипту",
    )
    return parser.parse_args()