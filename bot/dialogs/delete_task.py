from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, Back
from aiogram_dialog.widgets.text import Format, Const

from dialogs.states import DialogSG
from services.api import delete_task


async def get_task_to_delete(dialog_manager: DialogManager, **kwargs):
    task_to_delete = dialog_manager.dialog_data.get("task_to_delete")
    return {"task_to_delete": task_to_delete}


async def on_delete_task(c, b, manager: DialogManager):
    task_id = manager.dialog_data.get("task_id")
    task_to_delete = manager.dialog_data.get("task_to_delete")
    if task_id:
        try:
            await delete_task(task_id)
            await manager.event.answer(f"Задача '{task_to_delete}' удалена!")
        except Exception as e:
            await manager.event.answer(f"Ошибка при удалении задачи: {e}")
    else:
        await manager.event.answer("Не указана задача для удаления.")

    await manager.switch_to(DialogSG.view_tasks)


async def on_cancel_delete(c, b, manager: DialogManager):
    await manager.switch_to(DialogSG.view_tasks)


delete_task_window = Window(
    Format("Удалить задачу: {task_to_delete}?"),
    Row(
        Button(Const("✅ Да"), id="yes", on_click=on_delete_task),
        Button(Const("❌ Нет"), id="no", on_click=on_cancel_delete),
    ),
    state=DialogSG.delete_task,
    getter=get_task_to_delete,
)
