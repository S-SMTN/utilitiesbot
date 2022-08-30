import sqlite3

class SQLighter:
    def __init__(self):
        self.connection = sqlite3.connect('database\\data.db')
        self.cursor = self.connection.cursor()

    def get_utilities(self, id):
        with self.connection:
            servises = self.cursor.execute("SELECT Services FROM Users WHERE User_ID = (?)", (id,)).fetchall()
            respond = []
            for row in servises:
                servise = ''.join(row)
                respond.append(servise)
            respond = '\n'.join(respond)
            if respond:
                return f'You have registrated these servises:\n\n{respond}'
            else:
                return f"You have not registered servises!"

    def is_service(self, id, service):
        with self.connection:
            matching = self.cursor.execute("SELECT Services FROM Users WHERE User_ID = (?) AND Services = (?)", (id,service)).fetchall()
            if matching: return True
            else: return False

    def is_record(self, id, service, date):
        with self.connection:
            matching = self.cursor.execute("SELECT * FROM Data WHERE User_ID = (?) AND Services = (?) AND Date = (?)", (id,service, date)).fetchall()
            if matching: return matching
            else: return False

    def set_utilities(self, id, service):
        with self.connection:
            if not self.is_service(id, service):
                self.cursor.execute("INSERT INTO Users (User_ID, Services) VALUES(?,?)", (id, service))
                return f"New servise is added successfully."
            else: return f"You have this service already!"

    def del_utilities(self, id, service):
        with self.connection:
            if self.is_service(id, service):
                self.cursor.execute("DELETE FROM Users WHERE User_ID = (?) AND Services = (?)", (id,service))
                self.cursor.execute("DELETE FROM Data WHERE User_ID = (?) AND Services = (?)", (id,service))
                return f"Servise deleted successfully."
            else: return f"You don't have this service!"

    def edit_utilities(self, id, name_old, name_new):
        with self.connection:
            self.cursor.execute("UPDATE Users SET Services = (?) WHERE User_ID = (?) AND Services = (?)", (name_new,id,name_old))
            self.cursor.execute("UPDATE Data SET Services = (?) WHERE User_ID = (?) AND Services = (?)", (name_new,id,name_old))
            return f"Servise edited successfully."

    def add_record(self, id, service, date, number, price, summ):
        with self.connection:
            try:
                self.cursor.execute('INSERT INTO Data (User_id, Services, Date, Number, Price, Summ)  VALUES(?,?,?,?,?,?)', (id, service, date, number, price, summ))
                return f"New record is added successfully."
            except:
                return f"something goes wrong"

    def remove_record(self, id, service, date):
        with self.connection:
            if self.is_record(id, service, date):
                self.cursor.execute('DELETE FROM Data WHERE User_ID = (?) AND Services = (?) AND Date = (?)', (id, service, date))
                return f"Record is deleted successfully."
            else: return f"You don't have this record!"

    def show_all_records(self, id):
        with self.connection:
            executed = self.cursor.execute("SELECT Services, Date, Number, Price, Summ FROM Data WHERE User_ID = (?) ORDER BY Date, Services", (id,)).fetchall()
            respond_text = []
            respond_dict = []
            for row in executed:
                servise_text = f'{row[1]}, {row[0]}, Amount: {row[2]}, Price: {row[3]}, Summ: {row[4]}'
                respond_text.append(servise_text)
                servise_dict = {'Date': row[1], 'Service': row[0], 'Amount': row[2], 'Price': row[3], 'Summ': row[4]}
                respond_dict.append(servise_dict)
            respond_text = '\n'.join(respond_text)
            if respond_text:
                return f'You have these records:\n\n{respond_text}', respond_dict
            else:
                return f"You have no records!", False

    def show_by_name(self, id, name):
        with self.connection:
            executed = self.cursor.execute("SELECT Services, Date, Number, Price, Summ FROM Data WHERE User_ID = (?) AND Services = (?) ORDER BY Date, Services", (id,name)).fetchall()
            respond_text = []
            respond_dict = []
            for row in executed:
                servise_text = f'{row[1]}, {row[0]}, Amount: {row[2]}, Price: {row[3]}, Summ: {row[4]}'
                respond_text.append(servise_text)
                servise_dict = {'Date': row[1], 'Service': row[0], 'Amount': row[2], 'Price': row[3], 'Summ': row[4]}
                respond_dict.append(servise_dict)
            respond_text = '\n'.join(respond_text)
            if respond_text:
                return f'You have these records:\n\n{respond_text}', respond_dict
            else:
                return f"You have no records of {name}!", False

    def show_by_date(self, id, date):
        executed = self.cursor.execute("SELECT Services, Date, Number, Price, Summ FROM Data WHERE User_ID = (?) AND Date = (?) ORDER BY Date, Services", (id,date)).fetchall()
        respond_text = []
        respond_dict = []
        for row in executed:
            servise_text = f'{row[1]}, {row[0]}, Amount: {row[2]}, Price: {row[3]}, Summ: {row[4]}'
            respond_text.append(servise_text)
            servise_dict = {'Date': row[1], 'Service': row[0], 'Amount': row[2], 'Price': row[3], 'Summ': row[4]}
            respond_dict.append(servise_dict)
        respond_text = '\n'.join(respond_text)
        if respond_text:
            return f'You have these records:\n\n{respond_text}', respond_dict
        else:
            return f"You have no records in this date: {date}!", False