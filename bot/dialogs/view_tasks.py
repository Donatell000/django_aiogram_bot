import datetime

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from dialogs.states import DialogSG
from services.api import get_tasks


async def on_back_to_select_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "view"
    manager.dialog_data["current_page"] = 1
    await manager.switch_to(DialogSG.select_category)


async def on_add_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(DialogSG.add_task)


async def on_edit_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "edit"
    await manager.switch_to(DialogSG.select_task)


async def on_delete_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "delete"
    await manager.switch_to(DialogSG.select_task)


async def on_is_done_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "is_done"
    await manager.switch_to(DialogSG.select_task)


def format_datetime(datetime_str):
    dt_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt_obj.strftime("%H:%M %d-%m-%Y")


async def get_tasks_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    category_id = dialog_manager.dialog_data.get("category_id")
    if not category_id:
        return {"tasks_text": "Категория не выбрана."}

    try:
        tasks = await get_tasks(user_id=user_id, category_id=category_id)
        if tasks:
            tasks_text = "\n".join(
                f"{'✅' if task['is_done'] else '❌'} {task['title']} - время создания: {format_datetime(task['created_at'])} "
                f"| {'задача выполнена' if task['is_done'] else 'не выполнена'} "
                + (f"в: {format_datetime(task['due_date'])}" if task["is_done"] and task.get("due_date") else "")
                for task in tasks
            )
        else:
            tasks_text = "Нет задач в этой категории."
    except Exception as e:
        tasks_text = f"Ошибка при получении задач: {str(e)}"

    return {"tasks_text": tasks_text}


view_tasks_window = Window(
    Format("{tasks_text}"),
    Row(
        Button(Const("Добавить"), id="add_task", on_click=on_add_task),
        Button(Const("Изменить"), id="edit_task", on_click=on_edit_task),
        Button(Const("Удалить"), id="delete_task", on_click=on_delete_task),
    ),
    Row(
        Button(Const("Пометить как выполненную"), id="done_task", on_click=on_is_done_task),
    ),
    SwitchTo(Const("Назад"), id="to_select_category", state=DialogSG.select_category, on_click=on_back_to_select_category),
    state=DialogSG.view_tasks,
    getter=get_tasks_data,
)
