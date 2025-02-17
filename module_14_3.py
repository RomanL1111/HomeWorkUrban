from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils import executor
from aiogram.types import CallbackQuery
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
keyboard.add(KeyboardButton("Купить"))

inline_keyboard = InlineKeyboardMarkup(row_width=1)
inline_keyboard.add(
    InlineKeyboardButton("Рассчитать норму калорий", callback_data="calories"),
    InlineKeyboardButton("Формулы расчёта", callback_data="formulas"),
)


inline_buy_keyboard = InlineKeyboardMarkup(row_width=2)
inline_buy_keyboard.add(
    InlineKeyboardButton("Product1", callback_data="product1"),
    InlineKeyboardButton("Product2", callback_data="product2"),
    InlineKeyboardButton("Product3", callback_data="product3"),
    InlineKeyboardButton("Product4", callback_data="product4"),
)


products = [
    {"name": "Product1", "description": "описание 1", "price": 100, "image": "image1.jpg"},
    {"name": "Product2", "description": "описание 2", "price": 200, "image": "image2.jpg"},
    {"name": "Product3", "description": "описание 3", "price": 300, "image": "image3.jpg"},
    {"name": "Product4", "description": "описание 4", "price": 400, "image": "image4.jpg"},
]


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот, который поможет рассчитать вашу норму калорий. Выберите действие:",
        reply_markup=keyboard,
    )


@dp.message_handler(Text(equals="Рассчитать", ignore_case=True))
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)


@dp.message_handler(Text(equals="Купить", ignore_case=True))
async def get_buying_list(message: types.Message):
    for product in products:
        with open(product["image"], "rb") as photo:
            await message.answer_photo(
                photo,
                caption=(
                    f"Название: {product['name']} | "
                    f"Описание: {product['description']} | "
                    f"Цена: {product['price']}"
                ),
            )
    await message.answer("Выберите продукт для покупки:", reply_markup=inline_buy_keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith("product"))
async def send_confirm_message(call: CallbackQuery):
    product_number = call.data[-1]
    await call.message.answer(f"Вы успешно приобрели продукт {product_number}!")
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "formulas")
async def get_formulas(call: CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора для мужчин: \n"
        "Калории = 10 × вес (кг) + 6.25 × рост (см) - 5 × возраст (лет) + 5\n\n"
        "Формула для женщин: \n"
        "Калории = 10 × вес (кг) + 6.25 × рост (см) - 5 × возраст (лет) - 161"
    )
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "calories")
async def set_age(call: CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


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

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

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