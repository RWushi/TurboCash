from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Config import DB
from Backup import send_and_delete_backups


async def update_left_days():
    async with DB() as conn:
        await conn.execute("""
            UPDATE client
            SET days_left = days_left - 1
            WHERE days_left > 0 AND days_left IS NOT NULL;
        """)


async def everyday_task():
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(update_left_days, 'cron', hour=0, minute=0)
    scheduler.add_job(send_and_delete_backups, 'cron', hour=0, minute=0)
    scheduler.start()
