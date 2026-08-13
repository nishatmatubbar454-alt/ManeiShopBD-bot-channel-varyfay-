import aiosqlite
from datetime import datetime, timedelta, timezone
from config import settings

class Database:
    def __init__(self, db_path: str = settings.DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        """Creates table schema persistently in SQLite."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    created_at TIMESTAMP,
                    last_activity TIMESTAMP,
                    verification_status INTEGER DEFAULT 0,
                    verification_time TIMESTAMP,
                    verification_expiry TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER,
                    referred_user_id INTEGER UNIQUE,
                    created_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    status TEXT,
                    FOREIGN KEY(referrer_id) REFERENCES users(user_id),
                    FOREIGN KEY(referred_user_id) REFERENCES users(user_id)
                )
            """)
            await db.commit()

    async def register_or_update_user(self, user_id: int, first_name: str, username: str):
        now = datetime.now(timezone.utc)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, first_name, username, created_at, last_activity)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    first_name = excluded.first_name,
                    username = excluded.username,
                    last_activity = excluded.last_activity
            """, (user_id, first_name, username, now, now))
            await db.commit()

    async def process_referral_on_start(self, referrer_id: int, new_user_id: int) -> bool:
        """Processes and instantly completes referral condition upon /start with start parameter."""
        if referrer_id == new_user_id:
            return False  # Prevent self-referral

        now = datetime.now(timezone.utc)
        async with aiosqlite.connect(self.db_path) as db:
            # Confirm referrer exists in user table
            async with db.execute("SELECT user_id FROM users WHERE user_id = ?", (referrer_id,)) as cursor:
                if not await cursor.fetchone():
                    return False

            # Create & Complete Referral Record
            try:
                await db.execute("""
                    INSERT INTO referrals (referrer_id, referred_user_id, created_at, completed_at, status)
                    VALUES (?, ?, ?, ?, 'COMPLETED')
                """, (referrer_id, new_user_id, now, now))
                await db.commit()
                return True
            except aiosqlite.IntegrityError:
                return False  # Already referred once

    async def get_user(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def set_verified(self, user_id: int):
        now = datetime.now(timezone.utc)
        expiry = now + timedelta(hours=24)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users
                SET verification_status = 1, verification_time = ?, verification_expiry = ?
                WHERE user_id = ?
            """, (now, expiry, user_id))
            await db.commit()

    async def set_unverified(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users
                SET verification_status = 0, verification_time = NULL, verification_expiry = NULL
                WHERE user_id = ?
            """, (user_id,))
            await db.commit()

    async def get_all_user_ids(self) -> list[int]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT user_id FROM users") as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    async def get_completed_referral_count(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND status = 'COMPLETED'", 
                (user_id,)
            ) as cursor:
                res = await cursor.fetchone()
                return res[0] if res else 0

db = Database()

