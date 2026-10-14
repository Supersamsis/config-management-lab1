# Эмулятор оболочки ОС (Вариант 12)

Эмулятор командной строки UNIX-подобной ОС с поддержкой
виртуальной файловой системы (VFS). Реализован на Python 3.11
в виде CLI.

## Возможности

- REPL с приглашением, отражающим текущую директорию VFS.
- Раскрытие переменных окружения: `$VAR`, `${VAR}`, `%VAR%`.
- Виртуальная файловая система в памяти, загружаемая из JSON.
- Команды: `ls`, `cd`, `whoami`, `date`, `mkdir`, `vfs-load`,
  `exit`.
- Запуск стартовых скриптов с поддержкой комментариев `#`.
- Обработка ошибок: неизвестные команды, неверные аргументы,
  отсутствующие файлы.

## Установка

Требуется Python 3.8+.

    py -3.11 -m pip install -r requirements.txt

## Запуск

    py -3.11 -m src.main

С параметрами:

    py -3.11 -m src.main --vfs examples/vfs/minimal.json
    py -3.11 -m src.main --script examples/scripts/test_all.sh
    py -3.11 -m src.main --vfs examples/vfs/nested.json \
        --script examples/scripts/test_final.sh

## Команды эмулятора

| Команда          | Описание                              |
|------------------|---------------------------------------|
| `ls [path]`      | Содержимое директории                 |
| `cd [path]`      | Смена текущей директории              |
| `whoami`         | Имя текущего пользователя             |
| `date`           | Текущая дата и время                  |
| `mkdir <path>`   | Создать директорию в VFS              |
| `vfs-load <path>`| Загрузить новую VFS из JSON-файла     |
| `exit`           | Выход из эмулятора                    |

## Параметры командной строки

- `--vfs PATH` — путь к JSON-файлу VFS (если не указан,
  создаётся VFS по умолчанию).
- `--script PATH` — путь к стартовому скрипту с командами.

## Тесты

    py -3.11 -m pytest tests/ -v

## Примеры VFS

- `examples/vfs/minimal.json` — минимальная структура.
- `examples/vfs/nested.json` — вложенные директории.
- `examples/vfs/deep.json` — глубоко вложенная структура.

## Скрипты

- `examples/scripts/test_all.sh` — базовая проверка.
- `examples/scripts/test_commands.sh` — команды этапа 4.
- `examples/scripts/test_final.sh` — все команды, включая
  `mkdir` и `vfs-load`.
- `os_scripts/run_minimal.sh` — запуск без параметров.
- `os_scripts/run_with_script.sh` — запуск со скриптом.
- `os_scripts/run_with_vfs.sh` — запуск с VFS.