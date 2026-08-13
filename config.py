import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8922187032:AAE7HJnG5d8eroxapjhywJWF3eRwnikg7PU")
    ADMIN_CHAT_ID: int = int(os.getenv("ADMIN_CHAT_ID", "8235864550"))
    MINI_APP_URL: str = os.getenv("MINI_APP_URL", "https://amazing-fairy-6d0c51.netlify.app")
    DB_PATH: str = os.getenv("DB_PATH", "bot_database.db")

    # Required channels for verification
    REQUIRED_CHANNELS: list[dict] = [
        {"chat_id": "@Click2Cash_Site", "url": "https://t.me/Click2Cash_Site", "name": "Main Channel"},
        {"chat_id": "@Earning_Money_Lob", "url": "https://t.me/Earning_Money_Lob", "name": "Payment Channel"}
    ]

settings = Settings()
