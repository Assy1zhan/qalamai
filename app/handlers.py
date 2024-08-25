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
    
    user_histories[user_id] = [{"role": "system", "content": "You are a teacher. Your user is a student. Your name is QalamAI and you can speak russian, kazakh and english. Define the subjects and topics student wants to study. Define skill level of the student in the subject. Adapt to individual student needs, such as offering additional resources or adjusting the difficulty level based on the user’s progress. If he needs to write something or solve something, don't do the work for him, but help him do it himself, through leading questions or the Socratic method of teaching. Support dialogues that promote understanding, using techniques like Socratic questioning. Periodically quiz student to assess their knowledge, and provide feedback. Recognize the emotional state of student, and respond accordingly (e.g., offering encouragement, motivation, or breaks). If a student asks a question in particular math topic, make sure he possesses the basic knowledge needed to solve his problem. "}]
    user_histories[user_id].append({"role": "system", "content": "when you are trying to use inline expressions, it doesn't work. Do not use them"})
    user_histories[user_id].append({"role": "system", "content": "When a user asks a question like 'what is...' don't give him an answer right away. First ask him questions to understand his level of knowledge. And then, using the Socratic method of teaching, gradually explain the topic to him."})
    user_histories[user_id].append({"role": "system", "content": "When you and a student are working on a piece of writing and you see that something in their writing could be improved, such as replacing some words with synonyms or changing the wording to sound better, help them. But don't write for them or tell them directly what to add or change, but guide them so that they can figure out how to improve their writing themselves."})
    
    await message.answer(f'Выберите язык\nТілді таңдаңыз\nSelect a language\n\nРусский /ru \nҚазақша /kz\nEnglish /en')
    await state.clear()

@router.message(Command('kz'))
async def kaz_lang(message: Message):
    user_id = message.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your student is willing to talk in kazakh"})
    user_histories[user_id].append({"role": "assistant", "content": "Сәлем! Менің атым QalamAI. Мен бот-мұғаліммін. Егер сізде кез келген нәрсе туралы сұрақтарыңыз болса, маған қоя аласыз, ал мен сізге көмектесуге тырысамын. Ботты қайта іске қосу үшін осында басыңыз -> /start. Сізге қалай көмектесе аламын?"})
    
    await message.answer(f'Сәлем! Менің атым QalamAI. Мен бот-мұғаліммін. \n\nЕгер сізде кез келген нәрсе туралы сұрақтарыңыз болса, маған қоя аласыз, ал мен сізге көмектесуге тырысамын. \nБотты қайта іске қосу үшін осында басыңыз -> /start.\n\nСізге қалай көмектесе аламын?')

@router.message(Command('ru'))
async def rus_lang(message: Message):
    user_id = message.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your student is willing to talk in russian"})
    user_histories[user_id].append({"role": "assistant", "content": "Привет! Меня зовут QalamAI. Я бот-учитель. Ты можешь задавать мне вопросы по темам которые тебе интересны, а я тебе помогу! Чтобы перезапустить бота нажми сюда -> /start. Как я могу тебе помочь?"})
    
    await message.answer(f'Привет! Меня зовут QalamAI. Я бот-учитель.\n\nТы можешь задавать мне вопросы по темам которые тебе интересны, а я тебе помогу!\nЧтобы перезапустить бота нажми сюда -> /start\n\nКак я могу тебе помочь?')

@router.message(Command('en'))
async def eng_lang(message: Message):
    user_id = message.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your student is willing to talk in english"})
    user_histories[user_id].append({"role": "assistant", "content": "Hi there! My name is QalamAI and I'm a bot teacher. If you have any questions about anything, please don't hesitate to ask me. I'd be happy to help! To restart the bot, click here -> /start. How can I assist you today?"})
    
    await message.answer(f"Hi there! My name is QalamAI and I'm a bot teacher. \n\nIf you have any questions about anything, please don't hesitate to ask me. I'd be happy to help! \nTo restart the bot, click here -> /start. \n\nHow can I assist you today?")

@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer('Подождите, ваш предыдущий запрос выполняется...')


@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)
    
    user_id = message.from_user.id
    user_message = message.text
        
    user_histories[user_id].append({"role": "user", "content": user_message})
    response = await gpt4(user_histories[user_id])

    bot_reply = response.choices[0].message.content
    user_histories[user_id].append({"role": "assistant", "content": bot_reply})
    
    await message.answer(bot_reply)
    await state.clear()