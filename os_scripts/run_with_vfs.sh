#!/usr/bin/env bash
# Запуск с параметром VFS (на этапе 2 файл ещё не читается,
# но параметр должен приниматься и выводиться в отладке).
python -m src.main --vfs examples/vfs/minimal.json