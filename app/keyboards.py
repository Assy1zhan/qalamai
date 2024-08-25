from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

lang = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Русский', callback_data='russian_lang')],
        [InlineKeyboardButton(text='Қазақша', callback_data='kazakh_lang')],
        [InlineKeyboardButton(text='English', callback_data='english_lang')]
    ]
)