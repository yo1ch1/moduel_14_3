from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton('Формулы расчета калорий', callback_data='formulas')
kb2 = InlineKeyboardMarkup()
button6 = InlineKeyboardButton('Product1', callback_data='product_buying')
button7 = InlineKeyboardButton('Product2', callback_data='product_buying')
button8 = InlineKeyboardButton('Product3', callback_data='product_buying')
button9 = InlineKeyboardButton('Product4', callback_data='product_buying')

kb1.add(button3, button4, button6, button7, button8, button9)
kb2.add(button6, button7, button8, button9)

kb = ReplyKeyboardMarkup()
button1 = KeyboardButton('Расcчитать', resize_keyboard=True)
button2 = KeyboardButton('Информация', resize_keyboard=True)
button5 = KeyboardButton('Купить', resize_keyboard=True)
kb.add(button1, button2, button5)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(text='Привет, выбери одну из предложных кнопок!', reply_markup=kb)

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я первый тренировочный бот. Я могу рассчитать количество калорий, которое нужно потреблять в день.')

@dp.message_handler(text='Расcчитать')
async def main_menu(message):
    await message.answer('Выберите опцию.', reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'{i}.jpg', 'rb') as img:
            await message.answer_photo(img,
                        caption=f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





