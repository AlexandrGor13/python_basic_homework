"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""
import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(url):
    """
    Считывает данные в json-формате по указанному url
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def fetch_users_data():
    """
    Считывает данные о пользователях
    """
    url = USERS_DATA_URL
    data = await fetch_json(url)
    return data

async def fetch_posts_data():
    """
    Считывает данные о постах
    """
    url = POSTS_DATA_URL
    data = await fetch_json(url)
    return data

