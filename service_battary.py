import tkinter as tk
from tkinter import messagebox as mb
from tkinter import PhotoImage, ttk
import sqlite3


batterybrend = ("6СТ-60",
                "6СТ-62",
                "6СТ-66",
                "6СТ-75",
                "6СТ-90",
                "6СТ-100",
                "6СТ-110",
                "6СТ-132",
                "6СТ-140",
                "6СТ-180",
                "6СТ-190",
                "6СТ-192",
                "6СТ-225")


density_do = ("ВОДА",
              "1,22 г/см3",
              "1,23 г/см3",
              "1,24 г/см3",
              "1,25 г/см3",
              "1,26 г/см3",
              "1,27 г/см3",
              "1,28 г/см3",
              "1,29 г/см3")

density_after = ("1,27 г/см3",
                 "1,28 г/см3",
                 "1,29 г/см3",
                 "1,30 г/см3",
                 "1,31 г/см3")


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
        self.add_img = self.add_img
        self.update_img = self.update_img
        self.delete_img = self.delete_img
        self.search_img = self.search_img
        self.refresh_img = self.refresh_img
        self.backupdb_img = self.backupdb_img
        self.logo_img = self.logo_img
        self.tree = self.tree

    def init_main(self):
        """
        Функция верхнего меню. Выводит кнопки
        """
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # Кнопка добавления новой записи в базу данных
        # Выводит на экран диалоговое окно добавления записи
        self.add_img = tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar,
                                    text='Добавить',
                                    command=self.open_dialog,
                                    bg='#d7d8e0', bd=0,
                                    compound=tk.TOP,
                                    image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)
        # Кнопка редактирования записи в базе данных
        # Выводит на экран диалоговое окно редактирования записи
        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar,
                                    text='Редакция',
                                    bg='#d7d8e0',
                                    bd=0,
                                    image=self.update_img,
                                    compound=tk.TOP,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)
        # Кнопка удаления записи из базы данных
        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar,
                               text='Удалить',
                               bg='#d7d8e0',
                               bd=0,
                               image=self.delete_img,
                               compound=tk.TOP,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        # Кнопка поиска записи в базе данных
        # Выводит на экран диалоговое окно поиска записи
        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar,
                               text='Поиск',
                               bg='#d7d8e0',
                               bd=0,
                               image=self.search_img,
                               compound=tk.TOP,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)
        # Кнопка обновления поля вывода на экран
        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar,
                                text='Обновить',
                                bg='#d7d8e0',
                                bd=0,
                                image=self.refresh_img,
                                compound=tk.TOP,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        # Кнопка создания резервной копии базы данных
        self.backupdb_img = tk.PhotoImage(file='backupdb.gif')
        btn_backupdb = tk.Button(toolbar,
                                 text='Backup',
                                 bg='#d7d8e0',
                                 bd=0,
                                 image=self.backupdb_img,
                                 compound=tk.TOP,
                                 command=self.backupdb)
        btn_backupdb.pack(side=tk.LEFT)
        # Логотип
        self.logo_img = tk.PhotoImage(file='logo_avtoelektrik.png')
        lbl_logo = tk.Label(toolbar,
                            text='',
                            bg='#d7d8e0',
                            bd=0,
                            image=self.logo_img,
                            compound=tk.TOP)
        lbl_logo.pack(side=tk.RIGHT)
        # Поля для отображения на экране
        # таблицы базы данных
        self.tree = ttk.Treeview(self, columns=('id',
                                                'mydata',
                                                'gosnomer',
                                                'brendauto',
                                                'batterybrend',
                                                'kolbattery',
                                                'description',
                                                'density_do',
                                                'density_posle'),
                                 height=50,
                                 show='headings')
        # Поля таблицы
        self.tree.column('id', width=35, anchor=tk.CENTER)
        self.tree.column('mydata', width=90, anchor=tk.CENTER)
        self.tree.column('gosnomer', width=90, anchor=tk.W)
        self.tree.column('brendauto', width=120, anchor=tk.W)
        self.tree.column('batterybrend', width=90, anchor=tk.W)
        self.tree.column('kolbattery', width=80, anchor=tk.W)
        self.tree.column('description', width=450, anchor=tk.W)
        self.tree.column('density_do', width=130, anchor=tk.CENTER)
        self.tree.column('density_posle', width=130, anchor=tk.CENTER)
        # Заголовки таблицы
        self.tree.heading('id', text='№')
        self.tree.heading('mydata', text='Дата')
        self.tree.heading('gosnomer', text='Гос номер')
        self.tree.heading('brendauto', text='Марка ТС')
        self.tree.heading('batterybrend', text='Марка АКБ')
        self.tree.heading('kolbattery', text='Кол-во АКБ')
        self.tree.heading('description', text='Вид работ')
        self.tree.heading('density_do', text='Плотность до:')
        self.tree.heading('density_posle', text='Плотность после:')
        self.tree.pack(side=tk.LEFT)
        # Полоса вертикальной прокрутки
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self,
                mydata,
                gosnomer,
                brendauto,
                batterybrend,
                kolbattery,
                description,
                density_do,
                density_posle):
        """
        Функция записывает данные в таблицу данных
        :param mydata:
        :param gosnomer:
        :param brendauto:
        :param batterybrend:
        :param kolbattery:
        :param description:
        :param density_do:
        :param density_posle:
        :return:
        """
        self.db.insert_data(mydata,
                            gosnomer.upper(),
                            brendauto.upper(),
                            batterybrend,
                            kolbattery,
                            description,
                            density_do,
                            density_posle)
        self.view_records()

    def update_record(self,
                      mydata,
                      gosnomer,
                      brendauto,
                      batterybrend,
                      kolbattery,
                      description,
                      density_do,
                      density_posle):
        """

        :param mydata:
        :param gosnomer:
        :param brendauto:
        :param batterybrend:
        :param kolbattery:
        :param description:
        :param density_do:
        :param density_posle:
        :return:
        """
        self.db.c.execute('''UPDATE battary SET mydata=?, gosnomer=?, brendauto=?, batterybrend=?, 
        kolbattery=?, description=?, density_do=?, density_posle=? WHERE ID=?''',
                          (mydata,
                           gosnomer,
                           brendauto,
                           batterybrend,
                           kolbattery,
                           description,
                           density_do,
                           density_posle,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        """

        :return:
        """
        self.db.c.execute('''SELECT * FROM battary''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        """
        Функция удаляет выбранную запись из базы данных
        """
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM battary WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
            self.update()
        self.db.conn.commit()
        self.view_records()
        mb.showinfo("Удаление", "Запись удалена из БД")

    def search_records(self, gosnomer):
        """
        Функция ищет по гос номеру запись в базе данных
        :param gosnomer:
        """
        gosnomer = ('%' + gosnomer + '%',)
        self.db.c.execute('''SELECT * FROM battary WHERE gosnomer LIKE ?''', gosnomer)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def backupdb(self):
        self.conn = sqlite3.connect('battary.db')
        self.c = self.conn.cursor()
        with open("backup_battary.sql", "w") as f:
            for sql in self.conn.iterdump():
                f.write(sql)
        mb.showinfo("Резервная копия", "Резервная копия БД создана!")


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        """

        :return:
        """
        self.title('Добавить запись об аккумуляторах')
        self.geometry('670x385+370+245')
        self.resizable(False, False)
        # Названия полей ввода данных в диалоговом окне
        label_mydata = tk.Label(self, text='Дата:')
        label_mydata.place(x=50, y=20)
        label_gosnomer = tk.Label(self, text='Гос номер:')
        label_gosnomer.place(x=50, y=50)
        label_brendauto = tk.Label(self, text='Марка ТС:')
        label_brendauto.place(x=50, y=80)
        label_batterybrend = tk.Label(self, text='Марка АКБ:')
        label_batterybrend.place(x=50, y=110)
        label_kolbattery = tk.Label(self, text='Кол-во АКБ:')
        label_kolbattery.place(x=50, y=140)
        label_description = tk.Label(self, text='Вид работ:')
        label_description.place(x=50, y=170)
        label_density_do = tk.Label(self, text='Плотность до:')
        label_density_do.place(x=50, y=200)
        label_density_posle = tk.Label(self, text='Плотность после:')
        label_density_posle.place(x=50, y=230)
        # Поля ввода данных в окне добавления записи
        self.mydata_entry = ttk.Entry(self, width=23)
        self.mydata_entry.place(x=200, y=20)
        self.entry_gosnomer = ttk.Entry(self, width=23)
        self.entry_gosnomer.place(x=200, y=50)
        self.brendauto_entry = ttk.Entry(self, width=23)
        self.brendauto_entry.place(x=200, y=80)
        self.batterybrend_combobox = ttk.Combobox(self, values=batterybrend, state="readonly")
        self.batterybrend_combobox.current(1)
        self.batterybrend_combobox.place(x=200, y=110)
        self.kolbattery_spinbox = ttk.Spinbox(self, from_=1, to=10, state="readonly")
        self.kolbattery_spinbox.place(x=200, y=140)
        self.description = tk.Entry(self, width=70, font=('Times New Roman', 9))
        self.description.place(x=200, y=170)
        self.density_do_combobox = ttk.Combobox(self, values=density_do, state="readonly")
        self.density_do_combobox.current(3)
        self.density_do_combobox.place(x=200, y=200)
        self.density_posle = ttk.Combobox(self, values=density_after, state="readonly")
        self.density_posle.current(2)
        self.density_posle.place(x=200, y=230)
        # Кнопка закрытия диалогового окна добавления записи
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=280)
        # Кнопка добавления записи в базу данных
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=200, y=280)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.mydata_entry.get(), 
                                                                       self.entry_gosnomer.get(), 
                                                                       self.brendauto_entry.get(),
                                                                       self.batterybrend_combobox.get(), 
                                                                       self.kolbattery_spinbox.get(), 
                                                                       self.description.get(),
                                                                       self.density_do_combobox.get(), 
                                                                       self.density_posle.get()
                                                                       ))

        self.grab_set()
        self.focus_set()
        

class Update(Child):
    """
    Класс редактирования записи в базе данных
    """
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактирование записи')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=200, y=280)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.mydata_entry.get(),  # 0
                                                                          self.entry_gosnomer.get(),  # 1
                                                                          self.brendauto_entry.get(),  # 2
                                                                          self.batterybrend_combobox.get(),  # 3
                                                                          self.kolbattery_spinbox.get(),  # 4
                                                                          self.description.get(),  # 5
                                                                          self.density_do_combobox.get(),  # 6
                                                                          self.density_posle.get(),))  # 7

        self.btn_ok.destroy()

    def default_data(self):
        """
        Функция вставляет из базы данных, данные для редактирования
        в поля окна редактирования
        """
        self.db.c.execute('''SELECT * FROM battary WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.mydata_entry.insert(0, row[1])
        self.entry_gosnomer.insert(0, row[2])
        self.brendauto_entry.insert(0, row[3])
        self.description.insert(0, row[6])


class Search(tk.Toplevel):
    """
    Класс  поиска записи в базе данных по гос номеру автомобиля
    """
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по номеру')
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


class DB:
    """
    Класс работы с базой данных
    """
    def __init__(self):
        self.conn = sqlite3.connect('battary.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS battary (
            id integer primary key, 
            mydata TEXT, 
            gosnomer TEXT, 
            brendauto TEXT, 
            batterybrend TEXT, 
            kolbattery TEXT, 
            description TEXT, 
            density_do TEXT, 
            density_posle TEXT)''')
        self.conn.commit()

    def insert_data(self,
                    mydata,
                    gosnomer,
                    brendauto,
                    batterybrend,
                    kolbattery,
                    description,
                    density_do,
                    density_posle):
        """
        Функция получает данные из полей ввода данных
        и заносит их в базу данных
        :param mydata: текущая дата
        :param gosnomer: государственный номер автомобиля
        :param brendauto: модель автомобиля
        :param batterybrend: ёмкость аккумуляторной батареи
        :param kolbattery: количество аккумуляторов, сданных на обслуживание
        :param description: описание произведённых работ с аккумулятором
        :param density_do: плотность электролита до обслуживания
        :param density_posle: плотность электролита после обслуживания
        :return:
        """
        self.c.execute('''INSERT INTO battary(
        mydata, gosnomer, brendauto, batterybrend, kolbattery, 
        description, density_do, density_posle ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (mydata,
                        gosnomer, brendauto,
                        batterybrend, kolbattery,
                        description,
                        density_do,
                        density_posle))
        self.conn.commit()
        mb.showinfo("Сохранение", "Запись об аккумуляторе в БД сделана!")


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Сведения об обслуживании и обороте аккумуляторных батарей")
    root.geometry("1240x470+20+100")
    root.resizable(False, False)
    root.iconphoto(True, PhotoImage(file="logo.png"))
    root.mainloop()
