from Config import bot, DB
from datetime import datetime, timezone
import calendar


async def add_new_user(user_id, contact):
    async with DB() as conn:
        async with conn.transaction():
            await conn.execute('''
                INSERT INTO user_settings (ID, role) VALUES ($1, 'client') 
                ON CONFLICT (ID) DO NOTHING
            ''', user_id)
            await conn.execute('''
                INSERT INTO client (ID, contact) VALUES ($1, $2) 
                ON CONFLICT (ID) DO UPDATE
                SET contact = $2
            ''', user_id, contact)


async def get_role(user_id):
    async with DB() as conn:
        role = await conn.fetchval('SELECT role FROM user_settings WHERE ID = $1', user_id)
    return role


async def get_contact(user_id):
    user = await bot.get_chat(user_id)
    username = user.username
    if username:
        contact = f"https://t.me/{username}"
    else:
        contact = "-"
    return contact


async def exists_check(user_id):
    async with DB() as conn:
        result = await conn.fetchval('''SELECT EXISTS 
                                        (SELECT 1 FROM client
                                        WHERE ID = $1 AND full_name IS NOT NULL )''', user_id)
    return result


async def purchase_check(user_id):
    async with DB() as conn:
        result = await conn.fetchval('''SELECT EXISTS 
                                        (SELECT 1 FROM client
                                        WHERE ID = $1 AND
                                        order_number <> 0)''', user_id)
    return result


async def add_fullname(user_id, full_name):
    async with DB() as conn:
        await conn.execute('''UPDATE client SET full_name = $2
                              WHERE ID = $1''', user_id, full_name)


async def get_workplace_word(workplace):
    if workplace % 10 == 1 and workplace % 100 != 11:
        workplace_word = "рабочее место"
    elif 2 <= workplace % 10 <= 4 and (workplace % 100 < 10 or workplace % 100 >= 20):
        workplace_word = "рабочих места"
    else:
        workplace_word = "рабочих мест"
    return workplace_word


async def calculate_date(term, start_date=None):
    if not start_date:
        start_date = datetime.now(timezone.utc).date()

    month = start_date.month + term
    year = start_date.year
    if month > 12:
        month -= 12
        year += 1

    day = min(start_date.day, calendar.monthrange(year, month)[1])
    end_date = datetime(year, month, day).date()

    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())
    days_in_term = (end_datetime - start_datetime).days

    return start_date, end_date, days_in_term


async def save_order(user_id, term, workplace, price, keys):
    async with DB() as conn:
        result = await conn.fetchval('SELECT days_left FROM client WHERE ID = $1', user_id)
        current_days_left = result if result is not None else 0

        if current_days_left > 0:
            start_date = await conn.fetchval('SELECT end_date FROM client WHERE ID = $1', user_id)
            end_date, days_in_term = (await calculate_date(term, start_date))[1:3]
        else:
            start_date, end_date, days_in_term = await calculate_date(term)
            await conn.execute('UPDATE client SET start_date = $2 WHERE ID = $1', user_id, start_date)

        new_days_left = current_days_left + days_in_term

        await conn.execute('''
            UPDATE client 
            SET 
                end_date = $2,
                term = $3,
                workplace = $4,
                payment = $5,
                keys = $6,
                days_left = $7,
                order_number = order_number + 1
            WHERE ID = $1
        ''', user_id, end_date, term, workplace, price, keys, new_days_left)
