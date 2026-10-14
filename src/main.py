"""Точка входа эмулятора."""
from src.config import parse_args
from src.shell import Shell
from src.vfs import VFS


def main() -> None:
    """Запускает эмулятор."""
    args = parse_args()

    print("Параметры запуска:")
    print(f"  VFS:    {args.vfs}")
    print(f"  Скрипт: {args.script}")

    vfs = VFS()
    shell = Shell(vfs)

    if args.script:
        shell.run_script(args.script)

    shell.repl()


if __name__ == "__main__":
    main()