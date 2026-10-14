# Этап 4: тестирование основных команд эмулятора.

# --- Базовые команды ---
whoami
date

# --- ls в разных режимах ---
ls
ls /
ls /etc
ls /home

# --- cd в разных режимах ---
cd /
cd /etc
ls
cd ..
ls
cd /home/user/docs
ls

# --- Проверка ошибок ---
ls /nonexistent
cd /nope
cd /etc/hostname
unknown_command

# --- Выход ---
exit