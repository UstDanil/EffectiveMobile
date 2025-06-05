import os
import uuid
import pandas as pd
import aiohttp
import aiofiles
from datetime import datetime

from database import Session, SpimexTradingResult


async def get_content_from_link(href):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(href, allow_redirects=True) as response:
                if response.status != 200:
                    print(f'Не  удалось получить информацию по ссылке {href}')
                    return None
                data = await response.read()
                return data
    except Exception as e:
        print(f"Не удалось получить информацию по ссылке {href}. Ошибка: {str(e)}")
        return None


async def save_content_to_xls(content):
    file_path = f'files/{str(uuid.uuid4())}.xls'
    async with aiofiles.open(file_path, 'wb+') as file:
        await file.write(content)
    return file_path


async def save_data_from_link(href):
    content = await get_content_from_link(href)
    if not content:
        return 0
    xls_path = await save_content_to_xls(content)

    try:
        async with Session() as session:
            counter = 0
            df = pd.read_excel(xls_path)
            date = df['Форма СЭТ-БТ'][2].replace('Дата торгов: ', '')
            metric_ton_rows = df[df.eq("Единица измерения: Метрическая тонна").any(axis=1)].index.tolist()
            if not metric_ton_rows:
                return 0
            row_with_metric_ton = int(metric_ton_rows[0])
            df = df[row_with_metric_ton + 3:]

            total_row = int(df[df.eq("Итого:").any(axis=1)].index.tolist()[0])
            df = df[:total_row - row_with_metric_ton - 3]
            df = df[df['Unnamed: 14'] != '-']
            for index, row in df.iterrows():
                try:
                    exchange_product_id = row['Форма СЭТ-БТ']
                    if len(exchange_product_id) == 11:
                        new_trading_result = SpimexTradingResult(
                            id=str(uuid.uuid4()),
                            exchange_product_id=exchange_product_id,
                            exchange_product_name=row['Unnamed: 2'],
                            oil_id=exchange_product_id[:4],
                            delivery_basis_id=exchange_product_id[4:7],
                            delivery_basis_name=row['Unnamed: 3'],
                            delivery_type_id=exchange_product_id[-1],
                            volume=int(row['Unnamed: 4']),
                            total=int(row['Unnamed: 5']),
                            count=int(row['Unnamed: 14']),
                            date=datetime.strptime(date, '%Y-%m-%d').date(),
                        )
                        session.add(new_trading_result)
                        counter += 1
                except Exception as e:
                    print(e)

            await session.commit()
        print(f"Сохранено {counter} записей из ссылки {href}.")
    except Exception as e:
        print(e)
    finally:
        os.remove(xls_path)
        return counter
