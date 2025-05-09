from aiogram_dialog import Dialog

from .add_category import add_category_window
from .add_task import add_task_window
from .delete_category import delete_category_window
from .delete_task import delete_task_window
from .edit_category import edit_category_window
from .edit_task import edit_task_window
from .is_done_task import is_done_task_window
from .main_menu import main_menu_window
from .select_category import select_category_window
from .select_task import select_task_window
from .view_all_tasks import view_all_tasks_window
from .view_categories import view_categories_window
from .view_tasks import view_tasks_window


dialog = Dialog(add_category_window,
                add_task_window,
                delete_category_window,
                delete_task_window,
                edit_category_window,
                edit_task_window,
                is_done_task_window,
                main_menu_window,
                view_all_tasks_window,
                view_categories_window,
                view_tasks_window,
                select_category_window,
                select_task_window,
                )
