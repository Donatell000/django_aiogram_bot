from aiogram.fsm.state import State, StatesGroup


class DialogSG(StatesGroup):
    add_category = State()
    add_task = State()
    delete_category = State()
    delete_task = State()
    edit_category = State()
    edit_task = State()
    is_done_task = State()
    main_menu = State()
    view_all_tasks = State()
    view_categories = State()
    view_tasks = State()
    select_category = State()
    select_task = State()
