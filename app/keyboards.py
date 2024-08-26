from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

lang = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Русский', callback_data='russian_lang')],
        [InlineKeyboardButton(text='Қазақша', callback_data='kazakh_lang')],
        [InlineKeyboardButton(text='English', callback_data='english_lang')]
    ]
)

roles_rus = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ученик', callback_data='role_student')],
        [InlineKeyboardButton(text='Учитель', callback_data='role_teacher')]
    ]
)

roles_kaz = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Оқушы', callback_data='role_student')],
        [InlineKeyboardButton(text='Мұғалім', callback_data='role_teacher')]
    ]
)

roles_eng = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Student', callback_data='role_student')],
        [InlineKeyboardButton(text='Teacher', callback_data='role_teacher')]
    ]
)