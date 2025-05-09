from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from aiogram.types import Message

from dialogs.states import DialogSG
from services.api import edit_task


async def on_task_input(message: Message, widget, dialog_manager: DialogManager):
    telegram_id = message.from_user.id
    new_task_title = message.text
    task_id = dialog_manager.dialog_data.get("task_id")
    category_id = dialog_manager.dialog_data.get("category_id")
    await edit_task(task_id, new_task_title, telegram_id, category_id)
    await message.answer("Задача обновлена!")
    await dialog_manager.switch_to(DialogSG.view_tasks)


edit_task_window = Window(
    Const("Введите новое название задачи:"),
    MessageInput(on_task_input),
    state=DialogSG.edit_task,
)
