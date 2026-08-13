from aiogram import Router, CommandObject
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.database import db
from keyboards.inline import get_verification_keyboard, get_mini_app_keyboard
from utils.membership import is_user_verified

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "User"
    username = message.from_user.username or ""

    # Register/Update user session
    await db.register_or_update_user(user_id, first_name, username)

    # Process Referral System logic before verification
    args = command.args
    if args and args.isdigit():
        referrer_id = int(args)
        await db.process_referral_on_start(referrer_id, user_id)

    # If user is already verified within 24 hours
    if await is_user_verified(message.bot, user_id):
        await message.answer(
            "✅ আপনি ইতিমধ্যে ভেরিফাইড আছেন!\n\nনিচের বাটনে ক্লিক করে Mini App খুলুন:",
            reply_markup=get_mini_app_keyboard()
        )
        return

    # Trigger channel verification flow
    await message.answer(
        "👋 স্বাগতম!\n\nবটটি ব্যবহার করতে আমাদের চ্যানেলগুলোতে জয়েন করে **Verify** বাটনে ক্লিক করুন:",
        reply_markup=get_verification_keyboard()
    )
  
