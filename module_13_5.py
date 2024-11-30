from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот, который поможет рассчитать вашу норму калорий. Выберите действие:",
        reply_markup=keyboard,
    )


@dp.message_handler(Text(equals="Рассчитать", ignore_case=True))
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']

    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")
    await state.finish()


@dp.message_handler(Text(equals="Информация", ignore_case=True))
async def info(message: types.Message):
    await message.answer(
        "Я бот, который рассчитывает вашу норму калорий по формуле Миффлина-Сан Жеора. "
        "Нажмите 'Рассчитать', чтобы начать, или введите /start для возврата в главное меню."
    )


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer(
        "Я не понимаю это сообщение. Пожалуйста, выберите действие на клавиатуре или введите /start."
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
