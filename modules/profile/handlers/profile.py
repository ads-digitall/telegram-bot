import logging
import html
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold

from core.database.models import User
from modules.bot.services.channel_service import get_user_channels
from modules.bot.services.subscription_service import update_user_subscriptions
from core.database.database import get_async_session
from aiogram import Router
from error_handler import handle_error
from modules.bot.services.subscription_service import is_user_premium

logger = logging.getLogger(__name__)
router = Router()

async def build_user_profile(user_id: int, username: str, bot):
    async with get_async_session() as session:
        # Обновляем данные о подписках пользователя
        await update_user_subscriptions(user_id, bot)

        # Загружаем пользователя и связанные каналы
        user = await session.get(User, user_id)
        if not user:
            return "❌ Пользователь не найден.", None

        # Проверка на премиум
        is_premium = await is_user_premium(user_id, bot)

        # Получаем каналы пользователя
        subscribed_channels, managed_channels = await get_user_channels(user_id, bot)

        # Заголовок профиля
        text = (
            f"<b>👤 Профиль пользователя</b>\n"
            f"{hbold('🆔 ID')}: <code>{user.user_id}</code>\n"
            f"{hbold('🔻 Username')}: @{username}\n"
            f"🐭 Подписано каналов: {len(subscribed_channels)}\n"
            f"💎 Премиум: {'✅ Да' if is_premium else '❌ Нет'}\n"
            f"💠 Премиум-показов: {user.premium_views}\n"
            f"🎯 Реферальных показов: {user.referral_bonus_views}\n\n"
        )

        text += "<b>🐭 Подписки:</b>\n"
        if subscribed_channels:
            for ch in subscribed_channels:
                name = html.escape(ch.channel_name or "Без названия")
                link = f"{ch.channel_link}" if ch.channel_link else "-"
                text += f"• {name} ({link})\n"
        else:
            text += "• Нет подписок\n"

        text += "\n<b>👑 Управление:</b>\n"
        if managed_channels:
            for ch in managed_channels:
                name = html.escape(ch.channel_name or "Без названия")
                link = f"{ch.channel_link}" if ch.channel_link else "-"
                text += f"• {name} ({link})\n"
        else:
            text += "• Нет каналов под управлением\n"

        # Реферальная программа
        text += (
            "\n<b>👥 Реферальная программа</b>\n"
            "Приглашено: 0\n"
            f"Ссылка: https://t.me/lenta_feed_bot?start=ref_{user.user_id}\n"
        )

        # Финальный блок с пояснением
        text += (
            "\n🎯 Используйте ссылку, чтобы получить +10 показов за каждого приглашённого.\n"
            "📢 Чтобы ваш канал появился в ленте, добавьте в него двух ботов:\n"
            "@Lenta_food_bot и @lenta_profile_bot\n"
        )

        # Кнопки
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить каналы", callback_data="refresh_profile")],
            [InlineKeyboardButton(text="💎 Plus-подписка", url="https://t.me/tribute/app?startapp=ssC9")],
            [InlineKeyboardButton(text="📣 Разместить пост в каналах", callback_data="promote_channel")],
        ])

        return text, keyboard


@router.callback_query(lambda c: c.data == "refresh_profile")
async def handle_refresh_profile(callback: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "🔄 Обновить каналы"
    """
    user_id = callback.from_user.id
    username = callback.from_user.username
    bot = callback.bot

    try:
        text, keyboard = await build_user_profile(user_id, username, bot)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        handle_error(e, "ProfileHandler", f"Ошибка при обновлении профиля пользователя {user_id}")
        await callback.answer("Произошла ошибка при обновлении профиля.", show_alert=True)
