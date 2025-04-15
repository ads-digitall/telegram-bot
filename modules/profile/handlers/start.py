from aiogram import Router, types
from aiogram.filters import CommandStart
from modules.profile.handlers.profile import build_user_profile, update_user_subscriptions
from core.logger import get_logger
from core.database import get_database
from core.database.models import User

router = Router()
logger = get_logger(__name__)

@router.message(CommandStart())
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    async for session in get_database():
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id, username=username, subscribed_channels=[], referrals_count=0)
            session.add(user)
            await session.commit()

    # Обновляем список подписок при каждом старте
    await update_user_subscriptions(user_id, message.bot)

    profile_text, keyboard = await build_user_profile(user_id, username, message.bot)
    await message.answer(profile_text, reply_markup=keyboard, parse_mode="HTML")
