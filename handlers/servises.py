from buttons.buttons import utility_menu, yes_no_menu, cancel_menu
from aiogram import types, Dispatcher
from database.requests import SQLighter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

database = SQLighter()

""" /My_utilities """
async def command_my_utilities(message: types.Message):
    servises = database.get_utilities(message.from_user.id)
    await message.answer(servises, reply_markup=utility_menu)


""" /Add_utility """
class Utility_adder(StatesGroup):
    name = State()
    confirmation = State()

async def command_add_utility(message: types.Message):
    await Utility_adder.name.set()
    await message.reply('What is the name of utility?', reply_markup=cancel_menu)

async def utility_add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['name'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
    else:
        await Utility_adder.next()
        await message.reply(f"Do you really want to add \"{data['name']}\"?", reply_markup=yes_no_menu)

async def utility_add_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm'] = message.text
    if data['confirm'] == 'Yes':
        reply = database.set_utilities(message.from_user.id, data['name'])
        await message.answer(reply)
        await command_my_utilities(message)
        await state.finish()
    elif data['confirm'] == 'No':
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
        await state.finish()
    else:
        await Utility_adder.confirmation.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=yes_no_menu)


""" /Remove_utility """

class Utility_remover(StatesGroup):
    name = State()
    confirmation = State()

async def command_remove_utility(message: types.Message):
    await Utility_remover.name.set()
    await message.reply('What is the name of utility?', reply_markup=cancel_menu)

async def utility_remove_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    if data['name'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
    else:
        await Utility_remover.next()
        await message.reply(f"Do you really want to remove {data['name']}?", reply_markup=yes_no_menu)

async def utility_remove_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm'] = message.text
    if data['confirm'] == 'Yes':
        reply = database.del_utilities(message.from_user.id, data['name'])
        await message.answer(reply)
        await command_my_utilities(message)
        await state.finish()
    elif data['confirm'] == 'No':
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
        await state.finish()
    else:
        await Utility_remover.confirmation.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=yes_no_menu)


""" /Edit_utility """

class Utility_editer(StatesGroup):
    name_old = State()
    name_new = State()
    confirmation = State()

async def command_edit_utility(message: types.Message):
    await Utility_editer.name_old.set()
    await message.reply('What is the name of utility You want to edit?', reply_markup=cancel_menu)

async def utility_edit_name_old(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_old'] = message.text
    if data['name_old'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
    elif not database.is_service(message.from_user.id, data['name_old']):
        await state.finish()
        await message.answer(f"You don't have this service!\n\nThe operation is cancelled.")
        await command_my_utilities(message)
    else:
        await Utility_editer.next()
        await message.reply('What is the new name of utility?', reply_markup=cancel_menu)

async def utility_edit_name_new(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_new'] = message.text
    if data['name_new'] == 'Cancel':
        await state.finish()
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
    elif database.is_service(message.from_user.id, data['name_new']):
        await state.finish()
        await message.answer(f"You have this service already!\n\nThe operation is cancelled.")
        await command_my_utilities(message)
    else:
        await Utility_editer.next()
        await message.reply(f"Do you really want to change tne name of {data['name_old']} to {data['name_new']}?", reply_markup=yes_no_menu)

async def utility_edit_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm'] = message.text
    if data['confirm'] == 'Yes':
        reply = database.edit_utilities(message.from_user.id, data['name_old'], data['name_new'])
        await message.answer(reply)
        await state.finish()
        await command_my_utilities(message)
    elif data['confirm'] == 'No':
        await message.answer('The operation is cancelled.')
        await command_my_utilities(message)
        await state.finish()
    else:
        await Utility_editer.confirmation.set()
        await message.reply(f"You have entered incorrect data!\nUse buttons, please.", reply_markup=yes_no_menu)


""" the registration of message handlers """

def register_handlers_servises(dp : Dispatcher):
    dp.register_message_handler(command_my_utilities, commands=['Manage_utilities'], state=None)
    dp.register_message_handler(command_add_utility, commands=['Add_utility'], state=None)
    dp.register_message_handler(utility_add_name, state=Utility_adder.name)
    dp.register_message_handler(utility_add_confirm, state=Utility_adder.confirmation)
    dp.register_message_handler(command_remove_utility, commands=['Remove_utility'], state=None)
    dp.register_message_handler(utility_remove_name, state=Utility_remover.name)
    dp.register_message_handler(utility_remove_confirm, state=Utility_remover.confirmation)
    dp.register_message_handler(command_edit_utility, commands=['Edit_utility'], state=None)
    dp.register_message_handler(utility_edit_name_old, state=Utility_editer.name_old)
    dp.register_message_handler(utility_edit_name_new, state=Utility_editer.name_new)
    dp.register_message_handler(utility_edit_confirm, state=Utility_editer.confirmation)