from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Меню предметов для изучения')]
    ], 
    resize_keyboard=True,
    input_field_placeholder='Введите ваш запрос или просмотрите меню'
)

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='кнопка', url='https://youtube.com')],
    [InlineKeyboardButton(text='еще кнопка', url='https://youtube.com')]
])