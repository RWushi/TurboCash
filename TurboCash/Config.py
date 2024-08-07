from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncpg


DATABASE_CONFIGS = {
    'alisher': {
        'host': '',
        'database': '',
        'user': '',
        'password': '',
        'port': '5432'
    },
    'kirill': {
        'host': '',
        'database': '',
        'user': '',
        'password': '',
        'port': '5432'
    }
}


async def create_connection(config_name='alisher'):
    config = DATABASE_CONFIGS[config_name]
    return await asyncpg.connect(**config)


class DB:
    def __init__(self, config_name='alisher'):
        self.config_name = config_name

    async def __aenter__(self):
        self.conn = await create_connection(self.config_name)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


class UserState(StatesGroup):
    full_name = State()
    workplace = State()
    rates = State()
    confirmation = State()
    menu = State()
    black_list = State()
    add_black_list = State()
    delete_black_list = State()
    admin = State()
    add_admin = State()
    delete_admin = State()
    delete_bl_req = State()
    delete_cause_bl_req = State()
    payment_conf = State()


storage = MemoryStorage()
bot = Bot(token='')
dp = Dispatcher(bot, storage=storage)

ADMIN_ID=
