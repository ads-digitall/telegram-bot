from core.database import get_database
from core.database.models import User
from core.logger import get_logger

logger = get_logger(__name__)

async def apply_referral(new_user_id: int, referrer_id: int):
    """
    Сохраняет ID реферера и начисляет бонусные показы.
    """
    async for session in get_database():
        # Новый пользователь
        new_user = await session.get(User, new_user_id)
        if not new_user:
            logger.warning(f"❗ Новый пользователь {new_user_id} не найден в БД.")
            return

        # Не перезаписываем, если уже есть реферал
        if new_user.referrer_id:
            logger.info(f"🔁 Пользователь {new_user_id} уже зарегистрирован по рефералке.")
            return

        # Проверка валидности реферала
        referrer = await session.get(User, referrer_id)
        if not referrer or referrer.user_id == new_user_id:
            logger.warning(f"❌ Невалидный реферал ID: {referrer_id}")
            return

        new_user.referrer_id = referrer_id
        referrer.referrals_count += 1
        referrer.referral_bonus_views += 10

        await session.commit()

        logger.info(f"🎉 Реферал: {referrer_id} получил 10 показов за {new_user_id}")
        break


def generate_referral_link(bot_username: str, user_id: int) -> str:
    """
    Генерирует ссылку вида: https://t.me/botname?start=ref_userid
    """
    return f"https://t.me/{bot_username}?start=ref_{user_id}"
