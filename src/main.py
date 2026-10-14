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

    vfs = _load_vfs(args.vfs)
    shell = Shell(vfs)

    if args.script:
        shell.run_script(args.script)

    shell.repl()


def _load_vfs(path: str) -> VFS:
    """Загружает VFS из файла или создаёт по умолчанию.

    Args:
        path: путь к JSON-файлу или None.

    Returns:
        VFS: загруженная или созданная по умолчанию.
    """
    if not path:
        print("Создана VFS по умолчанию.")
        return VFS()
    try:
        vfs = VFS.from_json(path)
        print(f"VFS загружена из {path}")
        return vfs
    except FileNotFoundError:
        print(f"Ошибка: файл VFS не найден: {path}")
        return VFS()
    except ValueError as error:
        print(f"Ошибка загрузки VFS: {error}")
        return VFS()


if __name__ == "__main__":
    main()
