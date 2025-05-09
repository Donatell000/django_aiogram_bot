from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from dialogs.states import DialogSG
from services.api import delete_category, get_categories


async def get_category_to_delete(dialog_manager: DialogManager, **kwargs):
    category_to_delete = dialog_manager.dialog_data.get("category_to_delete")
    return {"category_to_delete": category_to_delete}


async def on_delete_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    category_id = manager.dialog_data.get("category_id")
    category_to_delete = manager.dialog_data.get("category_to_delete")
    user_id = callback.from_user.id

    if category_id:
        try:
            await delete_category(category_id, user_id)
            await manager.event.answer(f"Категория '{category_to_delete}' удалена!")
            categories = await get_categories(user_id)
            manager.dialog_data["categories"] = categories
            await manager.switch_to(DialogSG.view_categories)
        except Exception as e:
            await callback.message.answer(f"Ошибка при удалении категории: {e}")
            await manager.switch_to(DialogSG.view_categories)
    else:
        await callback.message.answer("Не указана категория для удаления.")
        await manager.switch_to(DialogSG.view_categories)


async def on_cancel_delete(c, b, manager: DialogManager):
    await manager.switch_to(DialogSG.view_categories)


delete_category_window = Window(
    Format("Удалить категорию: {category_to_delete}?"),
    Row(
        Button(Const("✅ Да"), id="yes", on_click=on_delete_category),
        Button(Const("❌ Нет"), id="no", on_click=on_cancel_delete),
    ),
    state=DialogSG.delete_category,
    getter=get_category_to_delete,
)
