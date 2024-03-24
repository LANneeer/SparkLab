from bot.infrastructure.handlers.menu import dp
from bot.infrastructure.handlers.help import router as help_router


# dp.include_router()
dp.include_router(help_router)
