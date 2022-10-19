import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()


    def init_main(self):
        """
        Функция инициализации класса
        :return: открытие главного окна
        """
        toolbar = tk.Frame(bg='#b3b2aa', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='book_plus.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#b3b2aa', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#b3b2aa', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#b3b2aa', bd=0, image=self.delete_img,
                                    compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#b3b2aa', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#b3b2aa', bd=0, image=self.refresh_img,
                               compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.balance_img = tk.PhotoImage(file='balance.png')
        btn_balance = tk.Button(toolbar, text='Баланс', bg='#b3b2aa', bd=0, image=self.balance_img,
                               compound=tk.TOP, command=self.open_balance_dialog)
        btn_balance.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода\расхода')
        self.tree.heading('total', text='Сумма')
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview())
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, description: str, costs, total: float):
        """
        Функция добавления данных из базы данных в таблицу Treeview
        :param description: наименование дохода/расхода
        :param costs: выбор из вариантов доход/расход
        :param total: сумма дохода/расхода
        :return: добавление параметров таблицу
        """
        self.db.insert_data(description, costs, total)
        self.view_records()

    def update_record(self, description: str, costs, total: float):
        """
        Функция обновления данных в таблице базы данных
        :param description: наименование дохода/расхода
        :param costs: выбор из вариантов доход/расход
        :param total: сумма дохода/расхода
        :return: изменение данных позиции
        """
        self.db.c.execute('''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
                          (description, costs, total, self.tree.set(self.tree.selection()[0], '#1'),))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        """
        Функция извлечения данных из базы данных и их отображение в TreeView
        :return: отображение данных в таблице TreeView
        """
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        """
        Функция удаления записей с базы данных
        :return: удаление позиций
        """
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM finance WHERE ID=?''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description: str):
        """
        Функция поиска данных по названию в базе данных
        :param description: наименование поиска
        :return: поиск позиций
        """
        description = ('%' + description + '%')
        self.db.c.execute('''SELECT * FROM finance WHERE description LIKE ?''', (description.lower(),))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def open_balance_dialog(self):
        Balance()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        """
        Функция инициализации класса
        :return: открытие окна добавление дохода/расхода
        """
        self.title('Добавить доходы\расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья дохода\расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=lambda: self.destroy())
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_money.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db


    def init_edit(self):
        """
        Функция инициализации класса
        :return: открытие окна редактирования
        """
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_money.get()))
        self.btn_ok.destroy()

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        """
        Функция инициализации класса
        :return: отображение окна поиска
        """
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class Balance(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_balance()
        self.db = db
        self.view = app

    def init_balance(self):
        """
        Функция инициализации класса
        :return: отображение окна баланса
        """
        self.title('Расчет баланса')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        self.btn_sum_income = tk.Button(self, bg='#5ed173', height=3, width=30, text='Сумма дохода', command=self.sum_income)
        self.btn_sum_income.place(x=80, y=25)

        self.btn_sum_expense = tk.Button(self, bg='#5ed173', height=3, width=30, text='Сумма расхода', command=self.sum_expense)
        self.btn_sum_expense.place(x=80, y=80)

        self.btn_sum_total = tk.Button(self, bg='#5ed173', height=3, width=30, text='Баланс', command=self.money)
        self.btn_sum_total.place(x=80, y=135)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=320, y=180)

    def sum_income(self):
        """
        Функция расчета суммы дохода
        :return: сумма дохода
        """
        self.summ = 0
        for row in self.db.c.execute('''SELECT * FROM finance WHERE costs == "Доход";''', ):
            self.summ += row[3]
        self.btn_sum_income['text'] = f'Сумма дохода составляет {self.summ}'

    def sum_expense(self):
        """
        Функция расчета суммы расхода
        :return: сумма расхода
        """
        self.summ = 0
        for row in self.db.c.execute('''SELECT * FROM finance WHERE costs == "Расход";''', ):
            self.summ += row[3]
        self.btn_sum_expense['text'] = f'Сумма расхода составляет {self.summ}'

    def money(self):
        """
        Функция расчета остатка денежных средств
        :return: текущий баланс
        """
        self.income = 0
        self.expense = 0
        for row in self.db.c.execute('''SELECT * FROM finance WHERE costs == "Доход";''', ):
            self.income += row[3]
        for row in self.db.c.execute('''SELECT * FROM finance WHERE costs == "Расход";''', ):
            self.expense += row[3]
        self.btn_sum_total['text'] = f'Ваш баланс составляет {self.income - self.expense}'

        self.grab_set()
        self.focus_set()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(('finance.db'))
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS finance (
            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            description VARCHAR(200),
            costs VARCHAR(200),
            total REAL          
        ); ''')
        self.conn.commit()

    def insert_data(self, description, costs, total):
        """
        Функция выполнения Sql запроса в базу данных и добавления данных в нее по вводимым значениям
        :param description: наименование дохода/расхода
        :param costs: выбор из вариантов доход/расход
        :param total: сумма дохода/расхода
        :return: добавление данных в базу данных
        """
        self.c.execute('''INSERT INTO finance (description, costs, total) 
        VALUES (?, ?, ?);''', (description, costs, total))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(bg='#b3b2aa')
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Personal wallet')
    root.geometry('665x450+300+200')
    root.resizable(False, False)
    root.mainloop()

