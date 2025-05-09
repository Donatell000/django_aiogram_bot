from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import CallbackQuery

from dialogs.states import DialogSG
from services.api import get_categories


async def on_category_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, category_id: str):
    dialog_manager.dialog_data["category_id"] = category_id
    user_id = dialog_manager.event.from_user.id

    categories = await get_categories(user_id=user_id)
    category = next((c for c in categories if str(c["id"]) == category_id), None)

    if category:
        category_to_delete = category["name"]
    else:
        category_to_delete = "Неизвестная категория"

    dialog_manager.dialog_data["category_to_delete"] = category_to_delete

    mode = dialog_manager.dialog_data.get("mode")

    if mode == "delete":
        await dialog_manager.switch_to(DialogSG.delete_category)
    elif mode == "edit":
        await dialog_manager.switch_to(DialogSG.edit_category)
    elif mode == "view":
        await dialog_manager.switch_to(DialogSG.view_tasks)


async def get_category_choices(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    mode = dialog_manager.dialog_data.get("mode", "view")
    current_page = dialog_manager.dialog_data.get("current_page", 1)
    categories_per_page = 4

    try:
        categories = await get_categories(user_id=user_id)
        start_index = (current_page - 1) * categories_per_page
        end_index = start_index + categories_per_page
        categories_page = categories[start_index:end_index]
        choices = [(str(category["id"]), category["name"]) for category in categories_page]

        if mode == "delete":
            mode_text = "Выберите категорию для удаления:"
        elif mode == "edit":
            mode_text = "Выберите категорию для редактирования:"
        elif mode == "view":
            mode_text = "Выберите категорию для просмотра:"
        else:
            mode_text = "Выберите категорию:"

        if not choices:
            return {
                "categories": [],
                "mode_text": "У вас нет активных категорий.",
                "has_next_page": False,
                "has_previous_page": current_page > 1
            }

        has_next_page = len(categories) > end_index
        has_previous_page = current_page > 1

        return {
            "categories": choices,
            "mode_text": mode_text,
            "has_next_page": has_next_page,
            "has_previous_page": has_previous_page,
        }
    except Exception:
        return {
            "categories": [],
            "mode_text": "Ошибка загрузки категорий",
            "has_next_page": False,
            "has_previous_page": False
        }


async def on_next_page(callback: CallbackQuery, button: Button, manager: DialogManager):
    current_page = manager.dialog_data.get("current_page", 1)
    categories_per_page = 4
    categories = await get_categories(user_id=manager.event.from_user.id)
    start_index = current_page * categories_per_page
    if start_index < len(categories):
        manager.dialog_data["current_page"] = current_page + 1
        await manager.switch_to(DialogSG.select_category)


async def on_previous_page(callback: CallbackQuery, button: Button, manager: DialogManager):
    current_page = manager.dialog_data.get("current_page", 1)
    if current_page > 1:
        manager.dialog_data["current_page"] = current_page - 1
        await manager.switch_to(DialogSG.select_category)


select_category_window = Window(
    Format("{mode_text}"),
    Select(
        Format("{item[1]}"),
        id="category_select_for_action",
        item_id_getter=lambda item: item[0],
        items="categories",
        on_click=on_category_selected,
    ),
    Row(
        Button(Const("Предыдущая страница"), id="previous_page", on_click=on_previous_page, when="has_previous_page"),
        Button(Const("Следующая страница"), id="next_page", on_click=on_next_page, when="has_next_page"),
    ),
    SwitchTo(Const("Назад"), id="to_view_categories", state=DialogSG.view_categories),
    state=DialogSG.select_category,
    getter=get_category_choices,
)
