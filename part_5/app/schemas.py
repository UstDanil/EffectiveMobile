import datetime
from pydantic import BaseModel, field_validator, ConfigDict


class SpimexTradingResultResponse(BaseModel):
    id: str
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: str
    created_on: str
    updated_on: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator('created_on', 'updated_on', mode='before')
    def convert_datetimes(cls, value) -> str:
        if isinstance(value, datetime.datetime):
            value = value.strftime('%Y-%m-%d %H:%M')
        return value

    @field_validator('date', mode='before')
    def convert_date(cls, value) -> str:
        if isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        return value


class DynamicsFilter(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None
    start_date: str | None = None
    end_date: str | None = None

    @field_validator('start_date', 'end_date', mode='after')
    def convert_dates(cls, value: str) -> datetime.date:
        try:
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
            return value
        except:
            raise ValueError('Invalid date value. Correct format "yyyy-mm-dd".')
