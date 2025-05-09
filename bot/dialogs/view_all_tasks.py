from datetime import datetime

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo

from dialogs.states import DialogSG
from services.api import get_tasks, get_categories


def format_datetime(datetime_str):
    dt_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt_obj.strftime("%Y-%m-%d %H:%M")


async def get_all_tasks_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id

    try:
        categories = await get_categories(user_id)
        all_text_parts = []

        for category in categories:
            category_id = category["id"]
            category_name = category["name"]
            tasks = await get_tasks(user_id=user_id, category_id=category_id)
            if tasks:
                tasks_lines = []
                for task in tasks:
                    created_at = format_datetime(task["created_at"])

                    if task["is_done"]:
                        status_symbol = "✅"
                        task_line = f"{status_symbol} {task['title']} — время создания: {created_at} | задача выполнена в: {format_datetime(task['due_date'])}"
                    else:
                        status_symbol = "❌"
                        task_line = f"{status_symbol} {task['title']} — время создания: {created_at} | задача не выполнена"

                    tasks_lines.append(task_line)

                category_text = f"📂 {category_name}\n" + "\n".join(tasks_lines)
                all_text_parts.append(category_text)

        tasks_text = "\n\n".join(all_text_parts) if all_text_parts else "У вас нет задач."
    except Exception as e:
        tasks_text = f"Ошибка при получении задач: {str(e)}"

    return {"tasks_text": tasks_text}


view_all_tasks_window = Window(
    Format("{tasks_text}"),
    SwitchTo(Const("Назад"), id="back_to_main_menu", state=DialogSG.main_menu),
    state=DialogSG.view_all_tasks,
    getter=get_all_tasks_data,
)
