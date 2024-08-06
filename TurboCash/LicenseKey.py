import random
import string
from Config import DB


async def check_key(key):
    async with DB() as conn:
        result = await conn.fetchval('SELECT 1 FROM client WHERE $1 = ANY(keys)', key)
    return result is not None


async def generate_key():
    characters = string.ascii_letters + string.digits
    groups = [''.join(random.choices(characters, k=6)) for _ in range(6)]
    key = '-'.join(groups)
    return key


async def generate_unique_key():
    while True:
        key = await generate_key()
        if not await check_key(key):
            return key


async def workplaces_keys(workplace):
    keys = []
    for _ in range(workplace):
        key = await generate_unique_key()
        keys.append(key)
    return keys
