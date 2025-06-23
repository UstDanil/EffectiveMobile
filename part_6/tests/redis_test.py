from app.router import save_redis_data
from app.backend.redis_client import redis_client
from app.schemas import SpimexTradingResultResponse


def test_save_redis_data():
    trading_result = SpimexTradingResultResponse(
        id="7bc2a5d0-b36f-4b18-87d8-8225de20b1f5",
        exchange_product_id="DST5BYY001O",
        exchange_product_name="ДТ ЕВРО, летнее, сорта C, эк. класса К5 марки ДТ-Л-К5 по ГОСТ 32511-2013, "
                              "НП Брянск (франко-резервуар ОТП Транснефть)",
        oil_id="DST5",
        delivery_basis_id="BYY",
        delivery_basis_name="НП Брянск",
        delivery_type_id="0",
        volume=20,
        total=45686,
        count=55,
        date="2025-06-19",
        created_on="2025-06-19 17:58",
        updated_on="2025-06-19 17:58"
    )
    save_redis_data("test_redis_key", [trading_result])
    value = redis_client.get("test_redis_key")
    assert value is not None

# def save_redis_data(redis_key: str, value: List[SpimexTradingResultResponse]):
#     redis_client.set(redis_key, json.dumps([v.model_dump() for v in value]))
#     expired_date = datetime.datetime.now()
#     if expired_date.hour > 14 or (expired_date.hour == 14 and expired_date.minute > 11):
#         expired_date += datetime.timedelta(days=1)
#     expired_date_14_11 = expired_date.replace(hour=14, minute=11)
#     redis_client.pexpireat(redis_key, expired_date_14_11)
