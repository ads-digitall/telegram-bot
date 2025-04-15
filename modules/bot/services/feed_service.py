from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_database
from core.database.models import Post, Channel
from sqlalchemy.sql.expression import func
import logging

logger = logging.getLogger(__name__)

async def get_random_posts(limit: int = 1):
    """
    Возвращает случайные посты из базы.
    """
    async for session in get_database():
        result = await session.execute(
            select(Post)
            .join(Channel, Post.channel_id == Channel.channel_id)
            .where(Channel.channel_link.isnot(None))
            .order_by(func.random())
            .limit(limit)
        )
        posts = result.scalars().all()
        break
    return posts

async def get_posts_by_interest(interest: str, limit: int = 2):
    """
    Возвращает посты по интересу.
    """
    async for session in get_database():
        result = await session.execute(
            text("""
                SELECT posts.*
                FROM posts
                JOIN channels ON posts.channel_id = channels.channel_id
                WHERE posts.interests ILIKE :interest
                AND channels.channel_link IS NOT NULL
                ORDER BY posts.date DESC
                LIMIT :limit
            """),
            {"interest": f"%{interest}%", "limit": limit}
        )
        posts = result.fetchall()
        break
    return [Post(**dict(p)) for p in posts]

async def generate_user_feed(user_id: int, posts_per_page: int = 10):
    """
    Генерирует ленту 2/1/2/1/... с учётом интересов и случайных постов.
    Если интересов нет — полностью случайная лента.
    """
    try:
        async for session in get_database():
            user_result = await session.execute(
                text("SELECT interests FROM users WHERE user_id = :user_id"),
                {"user_id": user_id}
            )
            user = user_result.fetchone()
            break

        # Если интересов нет — возвращаем случайные посты
        if not user or not user[0]:
            logger.warning(f"❗ У пользователя {user_id} нет интересов. Показываем случайную ленту.")
            return await get_random_posts(limit=posts_per_page)

        interests = user[0]
        feed = []
        interest_index = 0

        while len(feed) < posts_per_page:
            # 2 поста по интересам
            for _ in range(2):
                if interest_index >= len(interests):
                    interest_index = 0
                posts = await get_posts_by_interest(interests[interest_index], limit=1)
                feed.extend(posts)
                interest_index += 1

            # 1 случайный
            feed.extend(await get_random_posts(limit=1))

        return feed[:posts_per_page]

    except Exception as e:
        logger.error(f"Ошибка при формировании ленты пользователя {user_id}: {e}")
        raise
