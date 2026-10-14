"""Основной цикл REPL."""
import os
import re
from typing import List

from src.commands import COMMANDS, CommandError
from src.vfs import VFS


class Shell:
    """Эмулятор оболочки."""

    def __init__(self, vfs: VFS = None):
        self.vfs = vfs or VFS()
        self.running = True

    def _expand_vars(self, text: str) -> str:
        """Раскрывает переменные окружения в строке.

        Поддерживает два синтаксиса:
        - $VAR или ${VAR} (UNIX-подобный);
        - %VAR% (Windows).
        Если переменная не найдена, подставляется пустая строка.
        """
        def replace_var(match: "re.Match") -> str:
            name = match.group(1)
            value = os.environ.get(name)
            if value is None and name == "HOME":
                value = os.environ.get("USERPROFILE")
            return value or ""
        text = re.sub(
            r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}",
            replace_var,
            text,
        )
        text = re.sub(
            r"\$([A-Za-z_][A-Za-z0-9_]*)",
            replace_var,
            text,
        )
        text = re.sub(
            r"%([A-Za-z_][A-Za-z0-9_]*)%",
            replace_var,
            text,
        )
        return text

    def _parse(self, line: str) -> List[str]:
        """Разбирает строку на команду и аргументы."""
        return self._expand_vars(line).split()

    def execute(self, line: str) -> str:
        """Выполняет одну команду."""
        tokens = self._parse(line)
        if not tokens:
            return ""
        cmd_name, args = tokens[0], tokens[1:]

        if cmd_name == "exit":
            self.running = False
            return "Выход."

        if cmd_name not in COMMANDS:
            raise CommandError(f"Команда не найдена: {cmd_name}")

        return COMMANDS[cmd_name](self.vfs, args)

    def repl(self) -> None:
        """Запускает интерактивный режим."""
        print("Добро пожаловать в эмулятор оболочки!")
        while self.running:
            try:
                prompt = f"{self.vfs.name}$ "
                print(prompt, end="", flush=True)
                line = input()
                output = self.execute(line)
                if output:
                    print(output)
            except CommandError as e:
                print(f"Ошибка: {e}")
            except (EOFError, KeyboardInterrupt):
                print("\nВыход.")
                break
    def run_script(self, path: str) -> None:
        """Выполняет стартовый скрипт.

        Поддерживает комментарии, начинающиеся с '#'.
        Показывает ввод и вывод, имитируя диалог с пользователем.

        Args:
            path: путь к файлу скрипта.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                for raw_line in f:
                    stripped = raw_line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    print(f"$ {stripped}")
                    try:
                        output = self.execute(stripped)
                        if output:
                            print(output)
                    except CommandError as e:
                        print(f"Ошибка: {e}")
        except FileNotFoundError:
            print(f"Ошибка: скрипт не найден: {path}")