from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from aiogram.types import Message

from dialogs.states import DialogSG
from services.api import create_task


async def on_task_input(message: Message, widget, dialog_manager: DialogManager):
    user_id = message.from_user.id
    task_title = message.text
    category_id = dialog_manager.dialog_data.get("category_id")

    if not category_id:
        await message.answer("Ошибка: категория не выбрана.")
        return

    task_data = {
        "user_id": user_id,
        "title": task_title,
        "category_id": category_id
    }

    await create_task(task_data)
    await message.answer("Задача добавлена!")
    await dialog_manager.switch_to(DialogSG.view_tasks)


add_task_window = Window(
    Const("Введите название задачи:"),
    MessageInput(on_task_input),
    state=DialogSG.add_task,
)
