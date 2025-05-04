# 1. Ознакомиться с документацией по mkdir
man mkdir

# 2. Создать структуру директорий рекурсивно
mkdir -p /tmp/.tasks/bash/one/

# 3. Перейти в /tmp/ и вывести список содержимого с размерами в удобном формате
cd /tmp/
ls -lh

# 4. Переместить ".tasks/bash/one" в ".tasks/one" и удалить ".tasks/bash"
mv /tmp/.tasks/bash/one /tmp/.tasks/one
rmdir /tmp/.tasks/bash
