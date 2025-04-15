#!/bin/bash

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости как на ноуте
pip install -r freeze_pc.txt --force-reinstall
