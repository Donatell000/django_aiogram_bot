from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from aiogram.types import Message

from dialogs.states import DialogSG
from services.api import create_category


async def on_category_input(message: Message, widget, dialog_manager: DialogManager):
    user_id = message.from_user.id
    category_name = message.text.strip()
    if not category_name:
        await message.answer("Название категории не может быть пустым.")
        return

    category = await create_category(user_id, category_name)
    if category:
        dialog_manager.dialog_data["category_id"] = category["id"]
        await message.answer("Категория добавлена!")
        await dialog_manager.switch_to(DialogSG.view_tasks)
    else:
        await message.answer("Ошибка при создании категории. Попробуйте еще раз.")


add_category_window = Window(
    Const("Введите название категории:"),
    MessageInput(on_category_input),
    state=DialogSG.add_category,
)
