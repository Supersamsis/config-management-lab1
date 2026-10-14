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


def cmd_mkdir(vfs: VFS, args: List[str]) -> str:
    """Создаёт директорию в VFS.

    Args:
        vfs: виртуальная файловая система.
        args: список путей для создания.

    Returns:
        Пустая строка.

    Raises:
        CommandError: если путь не указан или создать не удалось.
    """
    if not args:
        raise CommandError("mkdir: missing operand")
    for path in args:
        if not vfs.create_dir(path):
            raise CommandError(
                f"mkdir: cannot create directory '{path}'"
            )
    return ""


def cmd_vfs_load(vfs: VFS, args: List[str]) -> str:
    """Загружает новую VFS из файла.

    Args:
        vfs: текущая VFS (будет заменена).
        args: путь к JSON-файлу.

    Returns:
        Сообщение об успешной загрузке.

    Raises:
        CommandError: если путь не указан или файл недоступен.
    """
    if not args:
        raise CommandError("vfs-load: missing file path")
    path = args[0]
    try:
        new_vfs = VFS.from_json(path)
    except FileNotFoundError:
        raise CommandError(f"vfs-load: file not found: {path}")
    except ValueError as error:
        raise CommandError(f"vfs-load: invalid file: {error}")
    vfs.root = new_vfs.root
    vfs.cwd = new_vfs.cwd
    return f"VFS loaded from {path}"


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "whoami": cmd_whoami,
    "date": cmd_date,
    "mkdir": cmd_mkdir,
    "vfs-load": cmd_vfs_load,
}