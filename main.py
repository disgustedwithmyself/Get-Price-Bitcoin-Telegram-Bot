# Фреймворк для работы с апишкой тг (aiogram)
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Сам парсер крипты
import crypto_stocks

# В классе Bot указываем parse_mode и задаём ему значение HTML, что бы была возможно красиво оформлять сообщения с помощью HTML тегов
bot = Bot(token="", parse_mode="HTML")
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):

    # Клавиатура
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        # Кнопка
        KeyboardButton(
            f"? Узнать курс доллара"
        )
    )

    # Сообщение с текстом и клавиатурой
    await message.answer(
        f"Привет, {message.from_user.first_name}! Напиши команду /Price или нажми на кнопку ниже Чтобы получить Стоимость биткоина к доллару на данный момент",
        reply_markup=markup
    )

# Обработчик текста с кнопки
@dp.message_handler(text="? Узнать курс доллара")
async def text_price(message: types.Message):

    # Клавитаруа под сообщением
    markup = InlineKeyboardMarkup(inline_keyboard=False)

    # Добавляем кнопки в неё
    markup.add(
        InlineKeyboardButton(
            "BINANCE", callback_data="currency:binance"
        ),
        InlineKeyboardButton(
            "COINBASE", callback_data="currency:coinbase"
        ),
        InlineKeyboardButton(
            "FTX", callback_data="currency:ftx"
        ),
        InlineKeyboardButton(
            "Kraken", callback_data="currency:kraken"
        ),
    )

    # Редактируем сообщение и кидаем новую клавиатуру
    await message.answer(
        f"На какой бирже будем смотреть курс? ?", reply_markup=markup
    )

# Обработчик команды /price
@dp.message_handler(commands=['price'])
async def cmd_price(message: types.Message):

    # Тут всё тоже самое что и в обработчике текста

    markup = InlineKeyboardMarkup(inline_keyboard=False)

    markup.add(
        InlineKeyboardButton(
            "BINANCE", callback_data="currency:binance"
        ),
        InlineKeyboardButton(
            "COINBASE", callback_data="currency:coinbase"
        ),
        InlineKeyboardButton(
            "FTX", callback_data="currency:ftx"
        ),
        InlineKeyboardButton(
            "Kraken", callback_data="currency:kraken"
        ),
    )

    await message.answer(
        f"На какой бирже будем смотреть курс? ?", reply_markup=markup
    )

# Не много Python 3.10
# В ином случае заменяем на всем любимою конструкцию if elif else
def get_price(stock="binance"):

    # Создаём переменную в которую запишем цену битка к вечно зелёным бумажкам
    price = 0
    
    # Тут начинаем наш switch-case
    match stock:
        # Если мы передали значение binance (по дефолту установлено)
        case "binance":
            # Берём цену с бинанса.
            # Ниже и так понятно
            price = crypto_stocks.Binance('btc', 'usd')
        case "coinbase":
            price = crypto_stocks.Coinbase('btc', 'usd')
        case "ftx":
            price = crypto_stocks.FTX('btc', 'usd')
        case "kraken":
            price = crypto_stocks.Kraken('btc', 'usd')

    # Возвращаем значение
    return price

# Наш обработчик инлайн кнопок
@dp.callback_query_handler(text_startswith="currency:")
async def callback_currency(call: types.CallbackQuery):

    # Получаем выбранную биржу
    stock = call.data.split(":")[1]
    # Обращаемся к нашей функции и передаём выбранную биржу
    price = get_price(stock=stock)

    # Создадим кнопку обновления курса и выбору другой биржи
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("? Обновить курс", callback_data=f"currency:{stock}"),
        InlineKeyboardButton("⬅️ Выбрать другую биржу", callback_data=f"back")
    )

    # Редактируем сообщение и кидаем новую клавиатуру
    await call.message.edit_text(
        f"? Курс битка на <b>{stock}</b>:\n<b>1 BTC = ${price}</b>", reply_markup=markup
    )
    
@dp.callback_query_handler(text="back")
async def callback_back(call: types.CallbackQuery):

    markup = InlineKeyboardMarkup(inline_keyboard=False)

    markup.add(
        InlineKeyboardButton(
            "BINANCE", callback_data="currency:binance"
        ),
        InlineKeyboardButton(
            "COINBASE", callback_data="currency:coinbase"
        ),
        InlineKeyboardButton(
            "FTX", callback_data="currency:ftx"
        ),
        InlineKeyboardButton(
            "Kraken", callback_data="currency:kraken"
        ),
    )

    await call.message.edit_text(
        f"На какой бирже будем смотреть курс? ?", reply_markup=markup
    )

# RUN
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
