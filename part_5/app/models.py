import datetime
from sqlalchemy import String, Integer, DateTime, func, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.backend.db import Base


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
    date: Mapped[datetime.date] = mapped_column(Date)
    created_on: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_on: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_response(self):
        return {
            "id": self.id,
            "exchange_product_id": self.exchange_product_id,
            "exchange_product_name": self.exchange_product_name,
            "oil_id": self.oil_id,
            "delivery_basis_id": self.delivery_basis_id,
            "delivery_basis_name": self.delivery_basis_name,
            "delivery_type_id": self.delivery_type_id,
            "volume": self.volume,
            "total": self.total,
            "count": self.count,
            "date": self.date.strftime('%Y-%m-%d'),
            "created_on": self.created_on.strftime('%Y-%m-%d %H:%M'),
            "updated_on": self.updated_on.strftime('%Y-%m-%d %H:%M'),
        }
