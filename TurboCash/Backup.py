import os
import asyncio
from datetime import datetime
from Config import DATABASE_CONFIGS, bot, ADMIN_ID

BACKUP_DIR = "Backups"


async def backup_database(config_name, config):
    formatted_date = datetime.now().strftime('%d.%m.%Y')
    if config_name == 'alisher':
        backup_name = f"Подписки {formatted_date}.sql"
    elif config_name == 'kirill':
        backup_name = f"Пользователи {formatted_date}.sql"

    backup_path = os.path.join(BACKUP_DIR, backup_name)
    command = f"pg_dump -U {config['user']} -h {config['host']} -p {config['port']} {config['database']}"

    process = await asyncio.create_subprocess_shell(
        command,
        env={"PGPASSWORD": config['password'], **os.environ},
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(stdout.decode('utf-8'))
    return backup_path


async def send_and_delete_backups():
    for name, config in DATABASE_CONFIGS.items():
        backup_path = await backup_database(name, config)
        await bot.send_document(ADMIN_ID, open(backup_path, 'rb'))
        os.remove(backup_path)
