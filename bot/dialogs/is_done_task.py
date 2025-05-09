from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo

from dialogs.states import DialogSG
from services.api import mark_task_as_done


async def mark_done_on_enter(dialog_manager: DialogManager, **kwargs):
    task_id = dialog_manager.dialog_data.get("task_id")
    user_id = dialog_manager.event.from_user.id

    if not task_id:
        return {"status_text": "❌ Не удалось определить задачу."}

    try:
        await mark_task_as_done(user_id, task_id)
        return {"status_text": "✅ Задача помечена как выполненная."}
    except Exception as e:
        return {"status_text": f"❌ Ошибка при пометке задачи: {e}"}


is_done_task_window = Window(
    Format("{status_text}"),
    SwitchTo(Const("🔙 Назад"), id="to_view_tasks", state=DialogSG.view_tasks),
    state=DialogSG.is_done_task,
    getter=mark_done_on_enter,
)
