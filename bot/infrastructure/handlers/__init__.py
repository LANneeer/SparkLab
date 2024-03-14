from bot.infrastructure.handlers.main import dp
from bot.infrastructure.handlers.menu import router as menu_router
from bot.infrastructure.handlers.help import router as help_router


dp.include_router(menu_router)
dp.include_router(help_router)
