from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.types import CallbackQuery, Message
from config import BOT_TOKEN
from crud_functions import initiate_db, get_all_products


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
initiate_db()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


def calculate_calories(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age + 5


def formulas_info():
    return (
        "Формула Миффлина-Сан Жеора для мужчин: \n"
        "Калории = 10 × вес (кг) + 6.25 × рост (см) - 5 × возраст (лет) + 5\n\n"
        "Формула для женщин: \n"
        "Калории = 10 × вес (кг) + 6.25 × рост (см) - 5 × возраст (лет) - 161"
    )


async def handle_formulas(call: CallbackQuery):
    await call.message.answer(formulas_info())
    await call.answer()


async def handle_calories(call: CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    dp.register_message_handler(set_growth, state=UserState.age)
    dp.register_message_handler(set_weight, state=UserState.growth)
    dp.register_message_handler(send_calories, state=UserState.weight)


async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    result = calculate_calories(data['weight'], data['growth'], data['age'])
    await message.answer(f"Ваша норма калорий: {result:.2f} ккал в день.")
    await state.finish()

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Рассчитать"), KeyboardButton("Информация"))
keyboard.add(KeyboardButton("Купить"))

inline_keyboard = InlineKeyboardMarkup(row_width=1)
inline_keyboard.add(
    InlineKeyboardButton("Рассчитать норму калорий", callback_data="calories"),
    InlineKeyboardButton("Формулы расчёта", callback_data="formulas"),
)

inline_buy_keyboard = InlineKeyboardMarkup(row_width=2)
products = get_all_products()

for product in products:
    product_id, title, description, price, image_path = product
    inline_buy_keyboard.add(
        InlineKeyboardButton(title, callback_data=f"product{product_id}")
    )


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
    products = get_all_products()
    for product in products:
        product_id, title, description, price, image_path = product
        with open(image_path, "rb") as photo:
            await message.answer_photo(
                photo,
                caption=f"Название: {title} | Описание: {description} | Цена: {price}"
            )

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_buy_keyboard)


@dp.callback_query_handler(lambda call: call.data.startswith("product"))
async def send_confirm_message(call: CallbackQuery):
    product_id = int(call.data[7:])

    products = get_all_products()

    product = next((p for p in products if p[0] == product_id), None)

    if product:
        title = product[1]
        await call.message.answer(f"Вы успешно приобрели продукт: {title}!")
    else:
        await call.message.answer("Продукт не найден.")

    await call.answer()


@dp.callback_query_handler(lambda call: call.data == "formulas")
async def get_formulas(call: CallbackQuery):
    await handle_formulas(call)


@dp.callback_query_handler(lambda call: call.data == "calories")
async def set_age(call: CallbackQuery):
    await handle_calories(call)


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
