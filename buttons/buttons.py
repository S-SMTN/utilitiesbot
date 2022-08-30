from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


""" Buttons """

button_help = KeyboardButton('/Help')
button_manage_utilities = KeyboardButton('/Manage_utilities')
button_manage_records = KeyboardButton('/Manage_records')
button_view_records = KeyboardButton('/View_records')

button_main = KeyboardButton('/Main_menu')

button_utility_add = KeyboardButton('/Add_utility')
button_utility_remove = KeyboardButton('/Remove_utility')
button_utility_edit = KeyboardButton('/Edit_utility')

button_record_add = KeyboardButton('/Add_record')
button_record_remove = KeyboardButton('/Remove_record')
button_records_edit = KeyboardButton('/Edit_record')

button_yes = KeyboardButton('Yes')
button_no = KeyboardButton('No')

button_cancel = KeyboardButton('Cancel')

button_year_2020 = KeyboardButton('2020')
button_year_2021 = KeyboardButton('2021')
button_year_2022 = KeyboardButton('2022')
button_year_2023 = KeyboardButton('2023')

button_month_jan = KeyboardButton('Jan')
button_month_feb = KeyboardButton('Feb')
button_month_mar = KeyboardButton('Mar')
button_month_apr = KeyboardButton('Apr')
button_month_may = KeyboardButton('May')
button_month_jun = KeyboardButton('Jun')
button_month_jul = KeyboardButton('Jul')
button_month_aug = KeyboardButton('Aug')
button_month_sep = KeyboardButton('Sep')
button_month_oct = KeyboardButton('Oct')
button_month_nov = KeyboardButton('Nov')
button_month_dec = KeyboardButton('Dec')

button_stop = KeyboardButton('Stop')
button_remove = KeyboardButton('Remove the record')

button_schedule_all = KeyboardButton('Show all')
button_schedule_by_service = KeyboardButton('By servise')
button_schedule_by_date = KeyboardButton('By date')
button_schedule_by_services_and_date = KeyboardButton('By servises and date')
button_schedule_main = KeyboardButton('Main menu')

button_schedule_show = KeyboardButton('Show chart')
button_schedule_back = KeyboardButton('Back')

""" Menues """

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(button_view_records).add(button_manage_records).add(button_manage_utilities).add(button_help)

utility_menu = ReplyKeyboardMarkup(resize_keyboard=True)
utility_menu.row(button_utility_add, button_utility_edit, button_utility_remove).row(button_main)

intomain_menu = ReplyKeyboardMarkup(resize_keyboard=True)
intomain_menu.row(button_main)

yes_no_menu = ReplyKeyboardMarkup(resize_keyboard=True)
yes_no_menu.row(button_yes, button_no)

cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_menu.row(button_cancel)

records_menu = ReplyKeyboardMarkup(resize_keyboard=True)
records_menu.row(button_record_add, button_record_remove).row(button_main)

year_menu = ReplyKeyboardMarkup(resize_keyboard=True)
year_menu.row(button_year_2023, button_year_2022).row(button_year_2021, button_year_2020).row(button_cancel)

monthes_menu = ReplyKeyboardMarkup(resize_keyboard=True)
monthes_menu.row(button_month_jan, button_month_feb, button_month_mar)
monthes_menu.row(button_month_apr, button_month_may, button_month_jun)
monthes_menu.row(button_month_jul, button_month_aug, button_month_sep)
monthes_menu.row(button_month_oct, button_month_nov, button_month_dec).row(button_cancel)

remove_stop_menu = ReplyKeyboardMarkup(resize_keyboard=True)
remove_stop_menu.row(button_remove, button_stop)

schedule_menu = ReplyKeyboardMarkup(resize_keyboard=True)
schedule_menu.row(button_schedule_all, button_schedule_by_service, button_schedule_by_date)
schedule_menu.row(button_schedule_main)

schedule_show = ReplyKeyboardMarkup(resize_keyboard=True)
schedule_show.row(button_schedule_show).row(button_schedule_back)