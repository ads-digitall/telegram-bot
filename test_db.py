import asyncio
from core.database import get_database
from core.database.crud import get_all_users

async def test_connection():
    # Получаем сессию из базы данных
    async for db in get_database():
        # Выполняем запрос для получения всех пользователей (может вернуть пустой список)
        users = await get_all_users(db)
        print("Пользователи в базе:", users)
        break  # Используем первую полученную сессию и выходим

if __name__ == "__main__":
    asyncio.run(test_connection())
