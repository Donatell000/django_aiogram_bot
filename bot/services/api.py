import aiohttp

from config_bot import API_BASE_URL


async def get_tasks(user_id: int, category_id: int = None):
    url = f"{API_BASE_URL}/tasks/?user_id={user_id}"
    if category_id:
        url += f"&category_id={category_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                tasks = await resp.json()
                if isinstance(tasks, list) and all(isinstance(task, dict) for task in tasks):
                    return tasks
                else:
                    raise ValueError("Полученные данные не являются списком словарей")
            except Exception as e:
                print(f"Ошибка при обработке данных: {e}")
                return []


async def create_task(task_data: dict):
    user_id = task_data["user_id"]
    task_title = task_data["title"]
    category_id = task_data["category_id"]

    async with aiohttp.ClientSession() as session:
        payload = {"user_id": user_id, "title": task_title, "category_id": category_id}
        async with session.post(f"{API_BASE_URL}/tasks/", json=payload) as resp:
            content_type = resp.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return await resp.json()
            else:
                html_content = await resp.text()
                raise ValueError(f"Unexpected content type: {content_type}. Response: {html_content}")


async def edit_task(task_id: str, title: str, user_id: int, category_id: int = None):
    async with aiohttp.ClientSession() as session:
        payload = {
            "title": title,
            "user": user_id
        }
        if category_id:
            payload["category_id"] = category_id

        async with session.put(f"{API_BASE_URL}/tasks/{task_id}/", json=payload) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                error_message = await resp.text()
                raise ValueError(f"Failed to update task: {resp.status} - {error_message}")


async def delete_task(task_id: int, user_id: int = None, category_id: int = None):
    async with aiohttp.ClientSession() as session:
        payload = {}
        if user_id:
            payload["user"] = user_id
        if category_id:
            payload["category_id"] = category_id

        async with session.delete(f"{API_BASE_URL}/tasks/{task_id}/", json=payload) as resp:
            if resp.status == 204:
                return True
            else:
                error_message = await resp.text()
                print(f"Error message: {error_message}")
                raise ValueError(f"Failed to delete task: {resp.status} - {error_message}")


async def mark_task_as_done(user_id: int, task_id: str):
    async with aiohttp.ClientSession() as session:
        payload = {"is_done": True, "user_id": user_id}

        try:
            async with session.patch(f"{API_BASE_URL}/tasks/{task_id}/", json=payload) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    error_message = await resp.text()
                    raise ValueError(f"Failed to mark task as done: {resp.status} - {error_message}")
        except Exception as e:
            raise Exception(f"Ошибка при пометке задачи как выполненной: {str(e)}")


async def get_categories(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/categories/?user_id={user_id}") as resp:
            try:
                categories = await resp.json()
                if isinstance(categories, list) and all(isinstance(cat, dict) for cat in categories):
                    return categories
                else:
                    raise ValueError("Полученные данные не являются списком словарей")
            except Exception as e:
                print(f"Ошибка при обработке данных: {e}")
                return []


async def create_category(user_id: int, name: str):
    async with aiohttp.ClientSession() as session:
        payload = {"user_id": user_id, "name": name}
        async with session.post(f"{API_BASE_URL}/categories/", json=payload) as resp:
            content_type = resp.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return await resp.json()
            else:
                html_content = await resp.text()
                raise ValueError(f"Unexpected content type: {content_type}. Response: {html_content}")


async def edit_category(category_id: int, name: str, user_id: int):
    async with aiohttp.ClientSession() as session:
        payload = {
            "name": name,
            "user_id": user_id,

        }

        async with session.put(f"{API_BASE_URL}/categories/{category_id}/", json=payload) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                error_message = await resp.text()
                raise ValueError(f"Failed to update category: {resp.status} - {error_message}")


async def delete_category(category_id: int, user_id: int):
    async with aiohttp.ClientSession() as session:
        payload = {
            "user_id": user_id
        }

        async with session.delete(f"{API_BASE_URL}/categories/{category_id}/", json=payload) as resp:
            if resp.status == 204:
                return True
            else:
                error_message = await resp.text()
                raise ValueError(f"Failed to delete category: {resp.status} - {error_message}")
