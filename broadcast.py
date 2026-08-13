import asyncio
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from config import settings
from database.database import db

router = Router()

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, command: CommandObject):
    # Admin verification
    if message.from_user.id != settings.ADMIN_CHAT_ID:
        return

    if not command.args:
        await message.answer("⚠️ Broadcast বার্তা প্রদান করুন।\n\nউদাহরণ: `/broadcast Hello Users!`", parse_mode="Markdown")
        return

    text_to_send = command.args
    users = await db.get_all_user_ids()
    
    success, failed = 0, 0
    status_msg = await message.answer(f"⏳ ব্রডকাস্ট শুরু হয়েছে... মোট ইউজার: {len(users)}")

    for uid in users:
        try:
            await message.bot.send_message(chat_id=uid, text=text_to_send)
            success += 1
            await asyncio.sleep(0.05)  # Rate limit protection
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ **ব্রডকাস্ট সম্পন্ন হয়েছে!**\n\n"
        f"🎯 সফল: {success}\n"
        f"❌ ব্যর্থ/ব্লকড: {failed}"
  )
  
