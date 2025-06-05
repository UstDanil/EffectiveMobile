import datetime
import json
from typing import Annotated, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, BackgroundTasks

from app.backend.db_depends import get_db
from app.backend.redis_client import redis_client
from app.schemas import SpimexTradingResultResponse, DynamicsFilter
from app.models import SpimexTradingResult


spimex_result_router = APIRouter(prefix='', tags=['spimex_result'])


def save_redis_data(redis_key: str, value: List[SpimexTradingResultResponse]):
    redis_client.set(redis_key, json.dumps([v.model_dump() for v in value]))
    expired_date = datetime.datetime.now()
    if expired_date.hour > 14 or (expired_date.hour == 14 and expired_date.minute > 11):
        expired_date += datetime.timedelta(days=1)
    expired_date_14_11 = expired_date.replace(hour=14, minute=11)
    redis_client.pexpireat(redis_key, expired_date_14_11)


@spimex_result_router.get('/get_last_trading_dates')
async def get_last_trading_dates(db: Annotated[AsyncSession, Depends(get_db)],
                                 last_trading_days_count: int = 7) -> List[str]:
    current_date = datetime.datetime.now()
    start_day = (current_date - datetime.timedelta(days=last_trading_days_count)).date()
    redis_key = f'last_trading_dates__{start_day.strftime("%Y-%m-%d")}'
    value = redis_client.get(redis_key)
    if value:
        return json.loads(value)

    trading_dates = await db.scalars(select(SpimexTradingResult.date).
                                     where(SpimexTradingResult.date >= start_day).distinct())
    result = [date.strftime('%Y-%m-%d') for date in trading_dates.all()]
    redis_client.set(redis_key, json.dumps(result))
    return result


@spimex_result_router.get('/get_dynamics')
async def get_dynamics(db: Annotated[AsyncSession, Depends(get_db)],
                       background_tasks: BackgroundTasks,
                       dynamics_filter: Annotated[DynamicsFilter, Query()]) -> List[SpimexTradingResultResponse]:
    filter_values_list = [str(value) for value in dynamics_filter.model_dump().values()]
    filters_str = '__'.join(filter_values_list)
    redis_key = f'get_dynamics__{filters_str}'
    value = redis_client.get(redis_key)
    if value:
        return json.loads(value)

    query = select(SpimexTradingResult)
    if dynamics_filter.start_date:
        query = query.where(SpimexTradingResult.date >= dynamics_filter.start_date)
    if dynamics_filter.end_date:
        query = query.where(SpimexTradingResult.date <= dynamics_filter.end_date)
    if dynamics_filter.oil_id:
        query = query.where(SpimexTradingResult.oil_id == dynamics_filter.oil_id)
    if dynamics_filter.delivery_type_id:
        query = query.where(SpimexTradingResult.delivery_type_id == dynamics_filter.delivery_type_id)
    if dynamics_filter.delivery_basis_id:
        query = query.where(SpimexTradingResult.delivery_basis_id == dynamics_filter.delivery_basis_id)

    filter_result = await db.scalars(query)
    result = [SpimexTradingResultResponse.model_validate(r) for r in filter_result.all()]
    background_tasks.add_task(save_redis_data, redis_key, result)
    return result


@spimex_result_router.get('/get_trading_results')
async def get_trading_results(db: Annotated[AsyncSession, Depends(get_db)],
                              background_tasks: BackgroundTasks,
                              oil_id: str = None, delivery_type_id: str = None,
                              delivery_basis_id: str = None) -> List[SpimexTradingResultResponse]:
    redis_key = f'trading_results__{oil_id}__{delivery_type_id}__{delivery_basis_id}'
    value = redis_client.get(redis_key)
    if value:
        return json.loads(value)

    date_query = select(func.max(SpimexTradingResult.date))
    result = await db.execute(date_query)
    last_date = result.scalar()
    query = select(SpimexTradingResult).where(SpimexTradingResult.date == last_date)
    if oil_id:
        query = query.where(SpimexTradingResult.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(SpimexTradingResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(SpimexTradingResult.delivery_basis_id == delivery_basis_id)
    trading_results = await db.scalars(query)
    result = [SpimexTradingResultResponse.model_validate(r) for r in trading_results.all()]
    background_tasks.add_task(save_redis_data, redis_key, result)
    return result
