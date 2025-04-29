import os
import uuid
import requests
import pandas as pd

from database import Session, SpimexTradingResult


def save_data_from_link(href):
    session = Session()
    print(href)
    file_path = f'files/{str(uuid.uuid4())}.xls'
    response = requests.get(href)
    if response.status_code != 200:
        print(f'Не  удалось получить информацию по url {href}')
        return
    with open(file_path, 'wb+') as file:
        file.write(response.content)

    try:
        df = pd.read_excel(file_path)
        date = df['Форма СЭТ-БТ'][2].replace('Дата торгов: ', '')
        metric_ton_rows = df[df.eq("Единица измерения: Метрическая тонна").any(axis=1)].index.tolist()
        if not metric_ton_rows:
            return
        row_with_metric_ton = int(metric_ton_rows[0])
        df = df[row_with_metric_ton + 3:]

        total_row = int(df[df.eq("Итого:").any(axis=1)].index.tolist()[0])
        df = df[:total_row - row_with_metric_ton - 3]
        df = df[df['Unnamed: 14'] != '-']
        for index, row in df.iterrows():
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
                    volume=row['Unnamed: 4'],
                    total=row['Unnamed: 5'],
                    count=row['Unnamed: 14'],
                    date=date,
                )
                session.add(new_trading_result)
    except Exception as e:
        print(e)
    finally:
        os.remove(file_path)
        session.commit()
        session.close()
