import datetime
from sqlalchemy import create_engine, String, Integer, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class SpimexTradingResult(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[str] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String(20))
    exchange_product_name: Mapped[str] = mapped_column(String(200))
    oil_id: Mapped[str] = mapped_column(String(4))
    delivery_basis_id: Mapped[str] = mapped_column(String(3))
    delivery_basis_name: Mapped[str] = mapped_column(String(50))
    delivery_type_id: Mapped[str] = mapped_column(String(1))
    volume: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    date: Mapped[str] = mapped_column(String(10))
    created_on: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_on: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


Base.metadata.create_all(bind=engine)

print("Таблица создана")
