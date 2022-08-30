from aiogram import executor

from configuration.create_bot import dp
from handlers import basic, servises, records, schedule

basic.register_handlers_basic(dp)
servises.register_handlers_servises(dp)
records.register_handlers_records(dp)
schedule.register_handlers_views(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)