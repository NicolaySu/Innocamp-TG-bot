from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from buttons import *
from config import rt
from neuro import neuroset
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from func import *


# Состояния
class states(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()


class quests(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()


# Команда /start
@rt.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f'''Здравствуйте, {message.from_user.full_name}!\n
Вы решили пройти отборочный этап на обучение в МТС.\n
Пожалуйста, пришлите мне свое резюме в следующем формате:\n 
Наличие высшего образования, желание работать в МТС
''')
    await state.set_state(states.S1)
    await set_param("id", message.from_user.id)


# Обработка резюме
@rt.message(states.S1)
async def resume(message: Message, state: FSMContext):
    await upd_param("resum", "id", message.text, message.from_user.id)
    text = f'''Ты должен проанализировать это резюме и оценить, соответствует ли оно следующим параметрам:
    У абитуриента есть высшее образование, абитуриент намерен работать в МТС.
    Ответь только одним словом: True - если соответствует или False - если не соответствует. Сходство может быть не абсолютным.
    Резюме: {message.text}'''

    if await neuroset(text) == "True\n":
        await message.answer("Вы прошли на следующий этап! Теперь вам нужно ответить на несколько вопросов.")
        quests_text = await neuroset(
            "Сгенерируй 3 вопроса для собеседования на обучение в МТС в следующем формате: Вопрос1 | Вопрос2 | Вопрос3. Примечание: в ответе должны быть только вопросы через разделитель, без примечаний.")
        quests_mass = quests_text.split(" | ")

        await state.update_data(quests_mass=quests_mass, otvets=[])
        await message.answer(quests_mass[0])
        await state.set_state(quests.q1)
    else:
        await message.answer("Вы не прошли.")
        await upd_param("state", "id", 0, message.from_user.id)


# Вопрос 1
@rt.message(quests.q1)
async def que1(message: Message, state: FSMContext):
    data = await state.get_data()
    otvets = data.get("otvets", [])
    otvets.append(message.text)
    await state.update_data(otvets=otvets)
    await message.answer(data["quests_mass"][1])
    await state.set_state(quests.q2)


# Вопрос 2
@rt.message(quests.q2)
async def que2(message: Message, state: FSMContext):
    data = await state.get_data()
    otvets = data.get("otvets", [])
    otvets.append(message.text)
    await state.update_data(otvets=otvets)
    await message.answer(data["quests_mass"][2])
    await state.set_state(quests.q3)


# Вопрос 3
@rt.message(quests.q3)
async def que3(message: Message, state: FSMContext):
    data = await state.get_data()
    otvets = data.get("otvets", [])
    otvets.append(message.text)
    await state.update_data(otvets=otvets)

    # Проверка правильности
    vopros_otvet = ""
    for q, a in zip(data["quests_mass"], otvets):
        vopros_otvet += f"{q} | {a} | "

    text1 = f'Я пришлю тебе строку, где через разделитель будут вопросы и ответы в формате: Вопрос | Ответ | Вопрос | Ответ | Вопрос | Ответ. Ты должен определить, на все ли вопросы дан правильный ответ, и если да, то написать слово True, если нет - False. Примечание: в ответе должно быть только одно слово.\n{vopros_otvet.strip()}'

    if await neuroset(text1) == "True\n":
        await message.answer("Вы прошли на следующий этап! Теперь вам нужно решить задачу.")
        await state.set_state(states.S3)
        task = await neuroset("Сгенерируй задачу для собеседования поступающих на обучение в МТС абитуриетнов")
        await state.update_data(task=task)
        await message.answer(task)
    else:
        await message.answer("Вы не прошли.")
        await upd_param("state", "id", 0, message.from_user.id)
        await state.clear()


# Задание
@rt.message(states.S3)
async def zadacha(message: Message, state: FSMContext):
    data = await state.get_data()
    task = data.get("task", "")
    otwet = message.text

    check = await neuroset(
        f'Я отправлю тебе задачу и ответ на нее. Ответь True если ответ дан правильно или False если ответ неверен. Примечание: в твоем ответе должно быть только одно слово. Задача: {task} Ответ: {otwet}'
    )

    if check == "True\n":
        await message.answer("Поздравляю! Вы прошли отборочный этап. В скором времени с вами свяжется специалист.",
                             reply_markup=menu.as_markup())
        await upd_param("state", "id", 1, message.from_user.id)
    else:
        await message.answer("Вы не прошли.")
        await upd_param("state", "id", 0, message.from_user.id)
        await state.clear()


@rt.message(Command('AI'))
async def ai(message: Message):
    await message.answer('Задайте вопрос ИИ')

    @rt.message()
    async def ai2(message: Message):
        await message.answer(await neuroset(message.text))
