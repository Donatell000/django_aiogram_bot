from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery

from .states import DialogSG


async def on_view_all_tasks(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(DialogSG.view_all_tasks)


async def on_view_tasks(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(DialogSG.view_tasks)


async def on_view_categories(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(DialogSG.view_categories)


main_menu_window = Window(
    Const("Выберите действие:"),
    Row(
        Button(Const("Все задачи"), id="view_all_tasks", on_click=on_view_all_tasks),
        Button(Const("Категории"), id="view_categories", on_click=on_view_categories),
    ),
    state=DialogSG.main_menu,
)
