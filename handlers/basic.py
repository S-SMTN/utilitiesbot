from buttons.buttons import main_menu, intomain_menu
from aiogram import types, Dispatcher
from configuration.create_bot import bot


""" /start, /Main_menu"""
async def start(message: types.Message):
    await message.answer('Pick the menu button', reply_markup=main_menu)

""" /Help """
async def help(message: types.Message):
    await message.answer(f'For the help watch this wideo:\n\n[TUTORIAL](https://youtu.be/GBIIQ0kP15E)', parse_mode='markdown', disable_web_page_preview=True,  reply_markup=intomain_menu)
    await bot.send_message(chat_id=548949585, text=f"{message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} wants help")

""" [inline URL](https://youtu.be/GBIIQ0kP15E) """

def register_handlers_basic(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start', 'Main_menu'])
    dp.register_message_handler(help, commands=['Help'])