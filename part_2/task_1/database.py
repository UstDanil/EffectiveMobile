import uuid
import datetime
from sqlalchemy import create_engine, String, Integer, Numeric, ForeignKey, Date, types, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = "genre"

    genre_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    name_genre: Mapped[str] = mapped_column(String(70))


class Author(Base):
    __tablename__ = "author"

    author_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    name_author: Mapped[str] = mapped_column(String(200))


class City(Base):
    __tablename__ = "city"

    city_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    name_city: Mapped[str] = mapped_column(String(200))
    days_delivery: Mapped[int] = mapped_column(Integer())


class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("author.author_id"))
    genre_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("genre.genre_id"))
    price: Mapped[float] = mapped_column(Numeric())
    amount: Mapped[int] = mapped_column(Integer())


class Client(Base):
    __tablename__ = "client"

    client_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    name_client: Mapped[str] = mapped_column(String(200))
    city_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("city.city_id"))
    email: Mapped[str] = mapped_column(String(50))


class Buy(Base):
    __tablename__ = "buy"

    buy_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    buy_description: Mapped[str] = mapped_column(String(300))
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("client.client_id"))


class BuyBook(Base):
    __tablename__ = "buy_book"

    buy_book_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    buy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("buy.buy_id"))
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("book.book_id"))
    amount: Mapped[int] = mapped_column(Integer())


class Step(Base):
    __tablename__ = "step"

    step_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    name_step: Mapped[str] = mapped_column(String(100))


class BuyStep(Base):
    __tablename__ = "buy_step"

    buy_step_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    buy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("buy.buy_id"))
    step_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("step.step_id"))
    date_step_beg: Mapped[datetime.date] = mapped_column(Date)
    date_step_end: Mapped[datetime.date] = mapped_column(Date)


Base.metadata.create_all(bind=engine)
