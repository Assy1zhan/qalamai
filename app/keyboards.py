from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Кнопка 1')],
        [KeyboardButton(text='Кнопка 2'), KeyboardButton(text='Еще кнопка')]
    ], 
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='кнопка', url='https://youtube.com')],
    [InlineKeyboardButton(text='еще кнопка', url='https://youtube.com')]
])