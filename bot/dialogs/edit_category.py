from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from aiogram.types import Message

from dialogs.states import DialogSG
from services.api import edit_category


async def on_category_input(message: Message, widget, dialog_manager: DialogManager):
    telegram_id = message.from_user.id
    new_category_name = message.text
    category_id = dialog_manager.dialog_data.get("category_id")

    await edit_category(category_id, new_category_name, telegram_id)

    await message.answer(f"Категория '{new_category_name}' обновлена!")
    await dialog_manager.switch_to(DialogSG.view_categories)


edit_category_window = Window(
    Const("Введите новое название категории:"),
    MessageInput(on_category_input),
    state=DialogSG.edit_category,
)
