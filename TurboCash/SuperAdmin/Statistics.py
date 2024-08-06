import pandas as pd
from Config import DB
from io import BytesIO


async def get_data():
    async with DB() as conn:
        data = await conn.fetch('SELECT * FROM client')
    return data


async def records_to_dataframe(records):
    columns = records[0].keys()
    rows = [list(record.values()) for record in records]
    return pd.DataFrame(rows, columns=columns)


async def get_file():
    query = await get_data()
    df = await records_to_dataframe(query)
    df.rename(columns={
        'id': 'ID',
        'full_name': 'ФИО',
        'contact': 'Контакт',
        'workplace': 'Кол-во ПК',
        'term': 'Срок',
        'payment': 'Оплата',
        'order_number': 'Кол-во заказов',
        'keys': 'Ключи активации',#после этого идет версия тк
        'machine_guid': 'Машин-гайд адреса',
        'start_date': 'Дата начала лицензии UTC',
        'end_date': 'Дата окончания лицензии UTC',
        'days_left': 'Остаток дней'
    }, inplace=True)

    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output
