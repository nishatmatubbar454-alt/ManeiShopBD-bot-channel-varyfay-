from aiogram import Router
from aiogram.types import Message
from utils.membership import is_user_verified
from keyboards.inline import get_verification_keyboard

router = Router()

@router.message()
async def global_message_gate(message: Message):
    """Global verification gate that catches any attempt to bypass channel verification."""
    user_id = message.from_user.id
    verified = await is_user_verified(message.bot, user_id)

    if not verified:
        await message.answer(
            "🔒 এই বটটি ব্যবহার করতে আপনার ভেরিফিকেশন সক্রিয় থাকা আবশ্যক।\n\n"
            "নিচের চ্যানেলগুলোতে জয়েন হয়ে Verify এ চাপুন:",
            reply_markup=get_verification_keyboard()
        )
      
