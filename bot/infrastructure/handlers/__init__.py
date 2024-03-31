from bot.apps import BotConfig
from bot.infrastructure.handlers.help import router as help_router
from bot.infrastructure.handlers.manager import router as manager_router
from bot.infrastructure.handlers.menu import router as menu_router
from bot.infrastructure.handlers.payment import router as payment_router
from bot.infrastructure.handlers.registration import router as registration_router
from bot.infrastructure.handlers.ride import router as ride_router
from bot.infrastructure.handlers.error import router as error_router

dp = BotConfig.dp

dp.include_router(registration_router)
dp.include_router(menu_router)
dp.include_router(help_router)
dp.include_router(manager_router)
dp.include_router(payment_router)
dp.include_router(ride_router)
dp.include_router(error_router)
