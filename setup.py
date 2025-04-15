"""
setup.py — конфигурационный скрипт для упаковки и установки проекта «Бот-2».

Этот файл определяет метаданные проекта, зависимости, точки входа для командной строки,
а также включает все пакеты, необходимые для корректной установки и запуска проекта.
"""

from setuptools import setup, find_packages

# Загрузка полного описания из README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Система автоматизации на базе Telegram-бота."

setup(
    name="BotLenta",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Централизованная система управления подписками и репостами в Telegram.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/botlenta",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiogram",
        "telethon",
        "pydantic",
        "sqlalchemy",
        "asyncpg",
        "redis",
        "python-dotenv",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"]
    },
    entry_points={
        "console_scripts": [
            "botlenta=central_core.launcher:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
