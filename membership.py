from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from config import settings
from database.database import db
from datetime import datetime, timezone

async def check_user_membership(bot: Bot, user_id: int) -> bool:
    """Uses getChatMember API to verify channel membership."""
    for channel in settings.REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel["chat_id"], user_id=user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                return False
        except Exception:
            return False
    return True

async def is_user_verified(bot: Bot, user_id: int) -> bool:
    """Enforces 24-hour expiration window and immediate live membership check."""
    user = await db.get_user(user_id)
    if not user or not user["verification_status"]:
        return False

    # Check 24-hour expiration rule
    expiry_val = user["verification_expiry"]
    if expiry_val:
        expiry = datetime.fromisoformat(expiry_val) if isinstance(expiry_val, str) else expiry_val
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
            
        if datetime.now(timezone.utc) > expiry:
            await db.set_unverified(user_id)
            return False

    # Recheck active channel status
    is_member = await check_user_membership(bot, user_id)
    if not is_member:
        await db.set_unverified(user_id)
        return False

    return True
  
