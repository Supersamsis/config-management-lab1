"""Точка входа эмулятора."""
from src.shell import Shell
from src.vfs import VFS


def main() -> None:
    """Запускает эмулятор."""
    vfs = VFS()
    shell = Shell(vfs)
    shell.repl()


if __name__ == "__main__":
    main()