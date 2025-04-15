@echo off
REM Переход в папку проекта
cd /d D:\Телеграм\Бот\бот

REM Добавить все файлы
git add .

REM Коммит с текущей датой и временем
for /f %%i in ('wmic os get localdatetime ^| find "."') do set datetime=%%i
set datetime=%datetime:~0,8%-%datetime:~8,6%
git commit -m "Авто-коммит %datetime%"

REM Отправить изменения на GitHub
git push origin main

pause
