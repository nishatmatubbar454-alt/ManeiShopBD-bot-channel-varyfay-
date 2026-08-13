from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from config import settings

def get_verification_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for ch in settings.REQUIRED_CHANNELS:
        buttons.append([InlineKeyboardButton(text=f"🔗 {ch['name']}", url=ch['url'])])
    
    buttons.append([InlineKeyboardButton(text="✅ Verify", callback_data="check_verification")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_mini_app_keyboard() -> InlineKeyboardMarkup:
    web_app = WebAppInfo(url=settings.MINI_APP_URL)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 বট ব্যবহার শুরু করুন", web_app=web_app)],
            [InlineKeyboardButton(text="🌐 Mini App খুলুন", web_app=web_app)]
        ]
    )
  
