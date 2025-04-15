from aiogram import Router
from modules.profile.handlers import start, profile, redirect_lenta

router = Router(name="profile")
router.include_router(start.router)
router.include_router(profile.router)
router.include_router(redirect_lenta.router)
