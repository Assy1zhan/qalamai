from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
import openai
import os
from openai import AsyncOpenAI
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import app.keyboards as kb

load_dotenv()
router = Router()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))
user_histories = {}

async def gpt4(dialog):
    response = await client.chat.completions.create(
        messages=dialog,
        model="gpt-4o-mini", 
        max_tokens=1024
    )
    return response

class Generate(StatesGroup):
    text = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id in user_histories:
        del user_histories[user_id]
    
    await message.answer(f'Привет! Я чат-бот компании QalaEduTech.\nДля навигации воспользуйся командой /help', reply_markup=kb.main)
    await state.clear()

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f'Я ИИ бот задачей которого отвечать на вопросы и помогать вам в обучении. Вы можете задать мне свой вопрос, а постараюсь на него ответить. Чем детальнее вы опишите вашу проблему, тем лучше я смогу вам помочь\nС чего начнем?', reply_markup=kb.settings)

@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ваш предыдущий запрос выполняется...')


@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    
    user_id = message.from_user.id
    user_message = message.text
    
    if user_id not in user_histories:
        user_histories[user_id] = []
        
    user_histories[user_id].append({"role": "user", "content": user_message})
    response = await gpt4(user_histories[user_id])

    bot_reply = response.choices[0].message.content
    user_histories[user_id].append({"role": "assistant", "content": bot_reply})
    
    await message.answer(bot_reply)
    await state.clear()