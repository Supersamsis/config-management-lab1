"""Реализация команд эмулятора."""
from typing import List

from src.vfs import VFS


class CommandError(Exception):
    """Ошибка выполнения команды."""


def cmd_ls(vfs: VFS, args: List[str]) -> str:
    """Заглушка ls: выводит имя команды и аргументы."""
    return f"ls: {args}"


def cmd_cd(vfs: VFS, args: List[str]) -> str:
    """Заглушка cd: выводит имя команды и аргументы."""
    return f"cd: {args}"


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
}