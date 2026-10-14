# Этап 5: тестирование всех команд, включая mkdir и vfs-load.

# --- Базовые команды ---
whoami
date

# --- Работа с VFS ---
ls /
cd /home
ls

# --- Создание директорий ---
mkdir /home/testdir
ls /home
mkdir /home/testdir/sub
cd /home/testdir
ls
cd /

# --- Ошибки mkdir ---
mkdir
mkdir /home/testdir

# --- Перезагрузка VFS ---
vfs-load examples/vfs/minimal.json
ls /
cd /etc
ls

# --- Ошибки vfs-load ---
vfs-load
vfs-load examples/vfs/nofile.json

# --- Выход ---
exit