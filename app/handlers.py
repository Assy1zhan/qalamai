from aiogram.types import Message, CallbackQuery
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
user_lang = {}

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
    
    user_histories[user_id] = [{"role": "system", "content": "You are a teacher. You are an excellent teacher with extensive teaching experience and the skills of a competent professional. Your name is QalamAI and you can speak russian, kazakh and english."}]
    user_lang[user_id] = 0
    
    await message.answer(f'Выберите язык\nТілді таңдаңыз\nSelect a language', reply_markup=kb.lang)
    await state.clear()

@router.callback_query(F.data == 'russian_lang')
async def rus_lang(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your user is willing to talk in russian"})
    user_histories[user_id].append({"role": "assistant", "content": "Приветствую! Меня зовут QalamAI. Я бот-учитель. Вы можете задавать мне вопросы по темам которые вам интересны, а я помогу! Чтобы перезапустить бота нажмите сюда -> /start. Вы ученик или учитель?"})
    user_lang[user_id] = 1
    
    await callback.message.answer(f'Приветствую! Меня зовут QalamAI. Я бот-учитель.\n\nВы можете задавать мне вопросы по темам которые вам интересны, а я помогу!\nЧтобы перезапустить бота нажмите сюда -> /start\n\nВы ученик или учитель?', reply_markup=kb.roles_rus)

@router.callback_query(F.data == 'kazakh_lang')
async def kaz_lang(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your user is willing to talk in kazakh"})
    user_histories[user_id].append({"role": "assistant", "content": "Сәлеметсіз бе! Менің атым QalamAI. Мен бот-мұғаліммін. Егер сізде кез келген нәрсе туралы сұрақтарыңыз болса, маған қоя аласыз, ал мен сізге көмектесуге тырысамын. Ботты қайта іске қосу үшін осында басыңыз -> /start. Сіз оқушысыз ба, әлде мұғалімсіз бе?"})
    user_lang[user_id] = 2
    
    await callback.message.answer(f'Сәлеметсіз бе! Менің атым QalamAI. Мен бот-мұғаліммін. \n\nЕгер сізде кез келген нәрсе туралы сұрақтарыңыз болса, маған қоя аласыз, ал мен сізге көмектесуге тырысамын. \nБотты қайта іске қосу үшін осында басыңыз -> /start.\n\nСіз оқушысыз ба, әлде мұғалімсіз бе?', reply_markup=kb.roles_kaz)

@router.callback_query(F.data == 'english_lang')
async def eng_lang(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your user is willing to talk in english"})
    user_histories[user_id].append({"role": "assistant", "content": "Hi there! My name is QalamAI and I'm a bot teacher. If you have any questions about anything, please don't hesitate to ask me. I'd be happy to help! To restart the bot, click here -> /start. Are you a student or a teacher?"})
    user_lang[user_id] = 3
    
    await callback.message.answer(f"Hi there! My name is QalamAI and I'm a bot teacher. \n\nIf you have any questions about anything, please don't hesitate to ask me. I'd be happy to help! \nTo restart the bot, click here -> /start. \n\nAre you a student or a teacher?", reply_markup=kb.roles_eng)

@router.callback_query(F.data == 'role_student')
async def student(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your user is a pupil. Consider the grade level your student is currently in and the subjects they want to study in order to adapt to their individual needs. This could include offering additional resources or adjusting the difficulty level of the material based on their progress. If he/she needs to write something or solve something, don't do the work for them, but help them do it themselves, through leading questions or the Socratic method of teaching. Support dialogues that promote understanding, using techniques like Socratic questioning. Periodically quiz student to assess their knowledge, and provide feedback. Recognize the emotional state of student, and respond accordingly (e.g., offering encouragement, motivation, or breaks). If a student asks a question in particular math topic, make sure he/she possesses the basic knowledge needed to solve their problem. "})
    user_histories[user_id].append({"role": "system", "content": "when you are trying to use inline expressions, it doesn't work. Do not use them"})
    user_histories[user_id].append({"role": "system", "content": "When student asks a question like 'what is...' don't give the answer right away. First ask them questions to understand his/her level of knowledge. And then, using the Socratic method of teaching, gradually explain the topic to them."})
    user_histories[user_id].append({"role": "system", "content": "When you and a student are working on a piece of writing and you see that something in their writing could be improved, such as replacing some words with synonyms or changing the wording to sound better, help them. But don't write for them or tell them directly what to add or change, but guide them so that they can figure out how to improve their writing themselves by asking questions like 'what do you think can be improve in this sentence', or 'try to paraphrase this sentence to make it sound more formal', etc."})
    
    bot_rep
    
    if user_lang[user_id] == 1:
        bot_rep = 'Напиши пожалуйста в каком ты классе и какой предмет/тему ты хочешь обсудить.'
    elif user_lang[user_id] == 2:
        bot_rep = 'Қай сыныпта екеніңді және қандай пәнді/тақырыпты талқылағың келетінін жаз.'
    else:
        bot_rep = 'Please write down which class you are in and what subject/topic you want to discuss.'
    
    user_histories[user_id].append({"role": "assistant", "content": bot_rep})
    await callback.message.answer(bot_rep)

@router.callback_query(F.data == 'role_teacher')
async def teacher(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    user_histories[user_id].append({"role": "system", "content": "Your user is a teacher. As a professional teacher help them by giving valuable advices and suggestions on their problems."})
    user_histories[user_id].append({"role": "system", "content": "when you are trying to use inline expressions, it doesn't work. Do not use them"})
    
    bot_rep
    
    if user_lang[user_id] == 1:
        bot_rep = 'Опишите максимально детально вашу проблему/ситуацию/вопрос, чтобы я мог дать вам наиболее точный ответ.'
    elif user_lang[user_id] == 2:
        bot_rep = 'Мәселеңізді, жағдайыңызды немесе сұрағыңызды мүмкіндігінше толықтай сипаттаңыз, сонда мен сізге ең нақты жауап бере аламын.'
    else:
        bot_rep = 'Describe your problem/situation/question in as much detail as possible so that I can give you the most accurate answer.'
    
    user_histories[user_id].append({"role": "assistant", "content": bot_rep})
    await callback.message.answer(bot_rep)
    

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