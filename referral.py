from aiogram import Router, F
from aiogram.types import Message
from database.database import db
from utils.membership import is_user_verified

router = Router()

@router.message(F.text == "📊 My Profile / Referrals")
async def show_referral_info(message: Message):
    user_id = message.from_user.id
    
    if not await is_user_verified(message.bot, user_id):
        return

    ref_count = await db.get_completed_referral_count(user_id)
    bot_info = await message.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"

    text = (
        f"👤 **আপনার প্রোফাইল & রেফারেল তথ্য**\n\n"
        f"🆔 User ID: `{user_id}`\n"
        f"👥 সফল রেফারেল: **{ref_count}**\n\n"
        f"🔗 আপনার রেফারেল লিংক:\n`{ref_link}`"
    )
    await message.answer(text, parse_mode="Markdown")
  
