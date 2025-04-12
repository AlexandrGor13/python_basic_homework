from app.db import async_session
from app.models import User, Post

async def fill_users_data(data: list[dict]):
    async with async_session() as session:
        for user_data in data:
            user_data_dict = {}
            user_data.pop("id")
            address = user_data.pop("address")
            user_data.pop("company")
            geo = address.pop("geo")
            user_data_dict.update(user_data | address | geo)
            user = User(**user_data_dict)
            session.add(user)
        await session.commit()


async def fill_posts_data(data: list[dict]):
    async with async_session() as session:
        for post_data in data:
            post_data_dict = {}
            post_data.pop("id")
            post_data_dict["user_id"] = post_data.pop("userId")
            post_data_dict.update(post_data)
            post = Post(**post_data_dict)
            session.add(post)
        await session.commit()