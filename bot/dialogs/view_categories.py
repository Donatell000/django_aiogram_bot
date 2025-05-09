from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, SwitchTo
from aiogram_dialog.widgets.text import Const

from dialogs.states import DialogSG
from services.api import get_categories


async def on_add_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(DialogSG.add_category)


async def on_edit_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "edit"
    await manager.switch_to(DialogSG.select_category)


async def on_delete_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "delete"
    await manager.switch_to(DialogSG.select_category)


async def on_view_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["mode"] = "view"
    await manager.switch_to(DialogSG.select_category)


async def get_categories_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    categories = await get_categories(user_id)
    return {"categories": categories}


view_categories_window = Window(
    Const("Управление категориями:"),
    Column( #был Row
        Button(Const("Просмотр"), id="go_select_category", on_click=on_view_category),
        Button(Const("Добавить"), id="add_category", on_click=on_add_category),
        Button(Const("Изменить"), id="edit_category", on_click=on_edit_category),
        Button(Const("Удалить"), id="delete_category", on_click=on_delete_category),
    ),
    SwitchTo(Const("Назад"), id="to_main_menu", state=DialogSG.main_menu),
    state=DialogSG.view_categories,
    getter=get_categories_data,
)
