"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""
import dataclasses

from sqlalchemy import MetaData, String, DECIMAL, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite, relationship

from app.config import SQLA_NAMING_CONVENTION


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=SQLA_NAMING_CONVENTION,
    )
    id: Mapped[int] = mapped_column(primary_key=True)


@dataclasses.dataclass
class Geo:
    lat: DECIMAL
    lng: DECIMAL


@dataclasses.dataclass
class Address:
    street: str
    suite: str
    city: str
    zipcode: str


class User(Base):
    __tablename__ = "users"

    name = mapped_column(String)
    username = mapped_column(String, unique=True)
    email = mapped_column(String, unique=True)
    street = mapped_column(String, default="")
    suite = mapped_column(String, default="")
    city = mapped_column(String, default="")
    zipcode = mapped_column(String, default="")
    lat = mapped_column(DECIMAL, default=0)
    lng = mapped_column(DECIMAL, default=0)
    phone = mapped_column(String, default="")
    website = mapped_column(String, default="")

    address = composite(Address, street, suite, city, zipcode)
    geo = composite(Geo, lat, lng)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
    )


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[String] = mapped_column(String)
    body: Mapped[String] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )

    author: Mapped["User"] = relationship(
        back_populates="posts",
    )
