from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from dialogs.states import DialogSG
from services.api import get_tasks


async def on_task_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["task_id"] = item_id

    user_id = dialog_manager.event.from_user.id
    category_id = dialog_manager.dialog_data.get("category_id")
    tasks = await get_tasks(user_id, category_id)
    task = next((t for t in tasks if str(t["id"]) == item_id), None)

    dialog_manager.dialog_data["task_to_delete"] = task["title"] if task else "Неизвестная задача"

    mode = dialog_manager.dialog_data.get("mode")
    if mode == "is_done":
        await dialog_manager.switch_to(DialogSG.is_done_task)
    elif mode == "delete":
        await dialog_manager.switch_to(DialogSG.delete_task)
    elif mode == "edit":
        await dialog_manager.switch_to(DialogSG.edit_task)


async def on_next_page(callback: CallbackQuery, button: Button, manager: DialogManager):
    current_page = manager.dialog_data.get("current_page", 1)
    tasks = await get_tasks(manager.event.from_user.id, manager.dialog_data.get("category_id"))

    if current_page * 4 < len(tasks):
        manager.dialog_data["current_page"] = current_page + 1
        await manager.switch_to(DialogSG.select_task)


async def on_previous_page(callback: CallbackQuery, button: Button, manager: DialogManager):
    current_page = manager.dialog_data.get("current_page", 1)
    if current_page > 1:
        manager.dialog_data["current_page"] = current_page - 1
        await manager.switch_to(DialogSG.select_task)


async def get_task_choices(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    category_id = dialog_manager.dialog_data.get("category_id")
    mode = dialog_manager.dialog_data.get("mode")
    current_page = dialog_manager.dialog_data.get("current_page", 1)
    per_page = 4

    try:
        tasks = await get_tasks(user_id, category_id)

        if mode == "is_done":
            tasks = [t for t in tasks if not t.get("is_done")]

        paginated = tasks[(current_page - 1) * per_page: current_page * per_page]
        choices = [{"id": str(t["id"]), "title": t["title"]} for t in paginated]

        mode_text = {
            "delete": "Выберите задачу для удаления:",
            "edit": "Выберите задачу для редактирования:",
            "is_done": "Выберите задачу для изменения статуса выполнения:"
        }.get(mode, "Выберите задачу:")

        return {
            "tasks": choices,
            "mode_text": "У вас нет активных задач." if not choices else mode_text,
            "has_next_page": len(tasks) > current_page * per_page,
            "has_previous_page": current_page > 1,
        }
    except Exception:
        return {
            "tasks": [],
            "mode_text": "Ошибка загрузки задач",
            "has_next_page": False,
            "has_previous_page": False,
        }


select_task_window = Window(
    Format("{mode_text}"),
    Select(
        Format("{item[title]}"),
        id="task_select",
        item_id_getter=lambda item: item["id"],
        items="tasks",
        on_click=on_task_selected,
    ),
    Row(
        Button(Const("Предыдущая страница"), id="prev_page", on_click=on_previous_page, when="has_previous_page"),
        Button(Const("Следующая страница"), id="next_page", on_click=on_next_page, when="has_next_page"),
    ),
    SwitchTo(Const("Назад"), id="to_view_tasks", state=DialogSG.view_tasks),
    state=DialogSG.select_task,
    getter=get_task_choices,
)
