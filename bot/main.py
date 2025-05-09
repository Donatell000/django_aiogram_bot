import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogManager, setup_dialogs, StartMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from dialogs import dialog
from dialogs.states import DialogSG
from config_bot import BOT_TOKEN


logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(dialog)
    setup_dialogs(dp)

    @dp.message(Command("start"))
    async def start(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(state=DialogSG.main_menu, mode=StartMode.RESET_STACK)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
