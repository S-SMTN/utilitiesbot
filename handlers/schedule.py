from buttons.buttons import schedule_menu, schedule_show, main_menu, cancel_menu, year_menu, monthes_menu
from aiogram import types, Dispatcher
from database.requests import SQLighter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from plots.plots import Plotter
from configuration.create_bot import bot
from aiogram.types import InputFile
import os

""" dict for monthes """

monthes = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


""" connecting to database """

database_records = SQLighter()
plotter = Plotter()


""" /View_records """

class Record_viewer(StatesGroup):
    choice = State()
    show_all = State()
    show_name = State()
    show_name_schedule = State()
    show_year = State()
    show_month = State()
    show_by_date = State()

async def command_view_records(message: types.Message):
    await Record_viewer.choice.set()
    await message.answer(f"What filter to apply?", reply_markup=schedule_menu)

async def view_choise(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['choice'] = message.text
    if data['choice'] == 'Show all':
        respond_text, respond_dict = database_records.show_all_records(message.from_user.id)
        if not respond_dict:
            await message.answer(respond_text, reply_markup=schedule_menu)
            await Record_viewer.choice.set()
        else:
            async with state.proxy() as data:
                data['respond_dict'] = respond_dict
            await Record_viewer.show_all.set()
            await message.answer(respond_text, reply_markup=schedule_show)
    elif data['choice'] == 'By servise':
        servises = database_records.get_utilities(message.from_user.id)
        await Record_viewer.show_name.set()
        await message.answer(f"{servises}\n\nWhat is the name of utility?", reply_markup=cancel_menu)
    elif data['choice'] == 'By date':
        await Record_viewer.show_year.set()
        await message.answer(f"Pick the year", reply_markup=year_menu)
    elif data['choice'] == 'Main menu':
        await state.finish()
        await message.answer('Pick the menu button', reply_markup=main_menu)

async def view_all_schedule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['show'] = message.text
    if data['show'] == 'Show chart':
        file = plotter.make_plot_all(message.from_user.id, data['respond_dict'])
        schedule = InputFile(path_or_bytesio=file)
        await bot.send_photo(message.from_user.id, schedule, f'', reply_markup=schedule_menu)
        os.remove(file)
        await Record_viewer.choice.set()
    elif data['show'] == 'Back':
        await Record_viewer.choice.set()
        await message.answer('Pick the menu button', reply_markup=schedule_menu)
    else:
        await Record_viewer.show_all.set()
        await message.reply(f"You have entered incorrect data!\n\nUse buttons, please.", reply_markup=schedule_show)

async def view_by_name_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['name'] == 'Cancel':
        await Record_viewer.choice.set()
        await message.answer('Pick the menu button', reply_markup=schedule_menu)
    elif database_records.is_service(message.from_user.id, data['name']):
        respond_text, respond_dict = database_records.show_by_name(message.from_user.id, data['name'])
        if not respond_dict:
            await message.answer(respond_text, reply_markup=schedule_menu)
            await Record_viewer.choice.set()
        else:
            async with state.proxy() as data:
                data['respond_dict'] = respond_dict
            await Record_viewer.show_name_schedule.set()
            await message.answer(respond_text, reply_markup=schedule_show)
    else:
        await Record_viewer.show_name.set()
        await message.answer(f"You have entered a non-existent service\n\nWhat is the name of utility?", reply_markup=cancel_menu)

async def view_by_name_schedule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['show'] = message.text
    if data['show'] == 'Show chart':
        file = plotter.make_plot_name(message.from_user.id, data['respond_dict'])
        schedule = InputFile(path_or_bytesio=file)
        await bot.send_photo(message.from_user.id, schedule, f'', reply_markup=schedule_menu)
        os.remove(file)
        await Record_viewer.choice.set()
    elif data['show'] == 'Back':
        await Record_viewer.choice.set()
        await message.answer('Pick the menu button', reply_markup=schedule_menu)
    else:
        await Record_viewer.show_all.set()
        await message.reply(f"You have entered incorrect data!\n\nUse buttons, please.", reply_markup=schedule_show)

async def view_by_date_year(message: types.Message, state: FSMContext):
    years = [2020, 2021, 2022, 2023]
    async with state.proxy() as data:
        try:
            data['year'] = message.text
            if data['year'] == 'Cancel':
                await Record_viewer.choice.set()
                await message.answer(f'Operation is canceled.\n\nPick the menu button', reply_markup=schedule_menu)
            elif int(data['year']) in years:
                await Record_viewer.show_month.set()
                await message.reply(f"Pick the month", reply_markup=monthes_menu)
            else: raise ValueError
        except ValueError:
            await Record_viewer.show_year.set()
            await message.reply(f"You have entered incorrect data!\n\nUse buttons, please.", reply_markup=year_menu)

async def view_by_date_month(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = message.text
    if data['month'] == 'Cancel':
                await Record_viewer.choice.set()
                await message.answer(f'Operation is canceled.\n\nPick the menu button', reply_markup=schedule_menu)
    elif data['month'] in monthes:
        date = f"{data['year']}-{monthes[data['month']]}"
        respond_text, respond_dict = database_records.show_by_date(message.from_user.id, date)
        if not respond_dict:
            await message.answer(respond_text, reply_markup=schedule_menu)
            await Record_viewer.choice.set()
        else:
            async with state.proxy() as data:
                data['respond_dict'] = respond_dict
            await Record_viewer.show_by_date.set()
            await message.answer(respond_text, reply_markup=schedule_show)
    else:
        await Record_viewer.show_month.set()
        await message.reply(f"You have entered incorrect data!\n\nUse buttons, please.", reply_markup=monthes_menu)

async def view_by_date_schedule(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['show'] = message.text
    if data['show'] == 'Show chart':
        file = plotter.make_plot_date(message.from_user.id, data['respond_dict'])
        schedule = InputFile(path_or_bytesio=file)
        await bot.send_photo(message.from_user.id, schedule, f'', reply_markup=schedule_menu)
        os.remove(file)
        await Record_viewer.choice.set()
    elif data['show'] == 'Back':
        await Record_viewer.choice.set()
        await message.answer('Pick the menu button', reply_markup=schedule_menu)
    else:
        await Record_viewer.show_all.set()
        await message.reply(f"You have entered incorrect data!\n\nUse buttons, please.", reply_markup=schedule_show)


""" the registration of message handlers """

def register_handlers_views(dp : Dispatcher):
    dp.register_message_handler(command_view_records, commands=['View_records'], state=None)
    dp.register_message_handler(view_choise, state=Record_viewer.choice)
    dp.register_message_handler(view_all_schedule, state=Record_viewer.show_all)
    dp.register_message_handler(view_by_name_set, state=Record_viewer.show_name)
    dp.register_message_handler(view_by_name_schedule, state=Record_viewer.show_name_schedule)
    dp.register_message_handler(view_by_date_year, state=Record_viewer.show_year)
    dp.register_message_handler(view_by_date_month, state=Record_viewer.show_month)
    dp.register_message_handler(view_by_date_schedule, state=Record_viewer.show_by_date)