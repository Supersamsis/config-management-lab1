"""Реализация команд эмулятора."""
import os
from datetime import datetime
from typing import List

from src.vfs import VFS


class CommandError(Exception):
    """Ошибка выполнения команды."""


def cmd_ls(vfs: VFS, args: List[str]) -> str:
    """Выводит содержимое директории.

    Args:
        vfs: виртуальная файловая система.
        args: аргументы команды.

    Returns:
        Строка с содержимым.
    """
    path = args[0] if args else "."
    node = vfs.get_node(path)
    if node is None:
        raise CommandError(
            f"ls: {path}: No such file or directory"
        )
    if not node.is_dir:
        return node.name
    return "  ".join(sorted(node.children.keys()))


def cmd_cd(vfs: VFS, args: List[str]) -> str:
    """Меняет текущую директорию.

    Args:
        vfs: виртуальная файловая система.
        args: аргументы команды.

    Returns:
        Пустая строка.
    """
    if not args:
        vfs.cwd = vfs.root
        return ""
    path = args[0]
    node = vfs.get_node(path)
    if node is None or not node.is_dir:
        raise CommandError(f"cd: {path}: Not a directory")
    vfs.cwd = node
    return ""


def cmd_whoami(_: VFS, __: List[str]) -> str:
    """Возвращает имя текущего пользователя."""
    return os.getenv("USER", os.getenv("USERNAME", "user"))


def cmd_date(_: VFS, __: List[str]) -> str:
    """Возвращает текущую дату и время."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "whoami": cmd_whoami,
    "date": cmd_date,
}