import asqlite

async def init_db():
    async with asqlite.connect("ticket_system.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS ticket_settings (
                guild_id INTEGER PRIMARY KEY,
                admin_role_id INTEGER NOT NULL,
                opened_tickets_category_id INTEGER NOT NULL,
                closed_tickets_category_id INTEGER NOT NULL,
                log_channel_id INTEGER NOT NULL
            )
        ''')
        await db.commit()
