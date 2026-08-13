from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.database import db
from utils.membership import check_user_membership
from keyboards.inline import get_mini_app_keyboard
from keyboards.reply import get_verified_reply_keyboard

router = Router()

@router.callback_query(F.data == "check_verification")
async def verify_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    is_member = await check_user_membership(callback.bot, user_id)

    if is_member:
        # Save 24-Hour verification state
        await db.set_verified(user_id)
        await callback.message.delete()
        
        # Bottom reply keyboard
        await callback.message.answer(
            "মোট ফিচার অ্যাক্সেস প্রস্তুত!",
            reply_markup=get_verified_reply_keyboard()
        )
        
        # Final success message with Mini App inline buttons
        await callback.message.answer(
            "✅ অভিনন্দন! ভেরিফিকেশন সফল হয়েছে!\n\n🎉 আপনি এখন বটটি ব্যবহার করার জন্য প্রস্তুত।",
            reply_markup=get_mini_app_keyboard()
        )
    else:
        await callback.answer(
            "❌ আপনি সবকটি চ্যানেলে জয়েন করেননি! সব চ্যানেলে জয়েন করে আবার চেষ্টা করুন।",
            show_alert=True
        )
      
