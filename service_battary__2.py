import tkinter as tk
from tkinter import PhotoImage, ttk
#from tkcalendar import DateEntry, Calendar
import sqlite3



brend_auto = ("УАЗ", "НИВА", "ВАЗ", "ВОЛГА", "ГАЗ", "RENAULT", "NISSAN", "ŠKODA", "VOLKSWAGEN",
              "MITSUBISHI", "TOYOTA", "KIA", "HYUNDAI", "КАМАЗ", "КРАЗ", "УРАЛ", "MAN", "МАЗ")

battary_brend = ("6СТ-60", "6СТ-62", "6СТ-75", "6СТ-90", "6СТ-100", "6СТ-110",
                 "6СТ-132", "6СТ-140", "6СТ-180", "6СТ-190", "6СТ-192", "6СТ-225")

jobs_text = ("Откорректирован уровень электролита, стационарная зарядка",
             "Аккумуляторная батарея разряжена полностью. Стационарная зарядка АКБ.",
             "Аккумуляторная батарея замкнута. Установлен резервный.",
             "Стационарная зарядка, корректировка плотности", 
             "Стационарная зарядка", 
             "Корректировка плотности", 
             "Выработан срок службы аккумуляторов. Выданы новые."
             )

density_up_to = ("ВОДА", "1,10 г/см3", "1,11 г/см3", "1,12 г/см3", "1,13 г/см3", "1,14 г/см3", "1,15 г/см3", 
                "1,16 г/см3", "1,17 г/см3", "1,18 г/см3", "1,19 г/см3", "1,20 г/см3", "1,12 г/см3", "1,22 г/см3",
                 "1,23 г/см3", "1,24 г/см3", "1,25 г/см3", "1,26 г/см3", "1,27 г/см3", "1,28 г/см3", "1,29 г/см3")

density_after = ("1,25 г/см3", "1,26 г/см3", "1,27 г/см3", "1,28 г/см3", "1,29 г/см3", "1,30 г/см3", "1,31 г/см3")

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить запись', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'my_data', 'gos_nomer', 'brend_auto', 'brend_battary', 
                                                'kol_battary', 'description', 'density_do', 'density_posle'), 
                                                height=20, show='headings')

        self.tree.column('ID', width=35, anchor=tk.CENTER)
        self.tree.column('my_data', width=90, anchor=tk.CENTER)
        self.tree.column('gos_nomer', width=90, anchor=tk.W)
        self.tree.column('brend_auto', width=120, anchor=tk.W)
        self.tree.column('brend_battary', width=90, anchor=tk.W)
        self.tree.column('kol_battary', width=80, anchor=tk.W)
        self.tree.column('description', width=450, anchor=tk.W)
        self.tree.column('density_do', width=130, anchor=tk.W)
        self.tree.column('density_posle', width=130, anchor=tk.W)

        self.tree.heading('ID', text='№')
        self.tree.heading('my_data', text='Дата')
        self.tree.heading('gos_nomer', text='Гос номер')
        self.tree.heading('brend_auto', text='Марка ТС')
        self.tree.heading('brend_battary', text='Марка АКБ')
        self.tree.heading('kol_battary', text='Кол-во АКБ')
        self.tree.heading('description', text='Вид работ')
        self.tree.heading('density_do', text='Плотность до:')
        self.tree.heading('density_posle', text='Плотность после:')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, my_data, gos_nomer, brend_auto, brend_battary, 
                kol_battary, description, density_do, density_posle):
        self.db.insert_data(my_data, gos_nomer, brend_auto, brend_battary, 
                            kol_battary, description, density_do, density_posle)
        self.view_records()

    def update_record(self, my_data, gos_nomer, brend_auto, brend_battary, 
                      kol_battary, description, density_do, density_posle):
        self.db.c.execute('''UPDATE battary SET my_data=?, gos_nomer=?, brend_auto=?, brend_battary=?,
                             kol_battary=?, description=?, density_do=?, density_posle=? WHERE ID=?''',
                            (my_data, gos_nomer, brend_auto, brend_battary, kol_battary, description, 
                             density_do, density_posle, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM battary''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM battary WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, gos_nomer):
        gos_nomer = ('%' + gos_nomer + '%',)
        self.db.c.execute('''SELECT * FROM battary WHERE gos_nomer LIKE ?''', gos_nomer)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить запись об аккумуляторах')
        self.geometry('670x325+370+245')
        self.resizable(False, False)

        label_my_data = tk.Label(self, text='Дата:')
        label_my_data.place(x=50, y=20)
        label_gos_nomer = tk.Label(self, text='Гос номер:')
        label_gos_nomer.place(x=50, y=50)
        label_brend_auto = tk.Label(self, text='Марка ТС:')
        label_brend_auto.place(x=50, y=80)
        label_brend_battary = tk.Label(self, text='Марка АКБ:')
        label_brend_battary.place(x=50, y=110)
        label_kol_battary = tk.Label(self, text='Кол-во АКБ:')
        label_kol_battary.place(x=50, y=140)
        label_description = tk.Label(self, text='Вид работ:')
        label_description.place(x=50, y=170)
        label_density_do = tk.Label(self, text='Плотность до:')
        label_density_do.place(x=50, y=210)
        label_density_posle = tk.Label(self, text='Плотность после:')
        label_density_posle.place(x=50, y=240)

        self.my_data_combo = DateEntry(self, foreground="grey",
                                       normalforegraund="grey",
                                       selectforegraund="red",
                                       backgraund="white",
                                       date_pattern="dd-mm-YYYY")
        #self.my_data_combo.current(0)
        self.my_data_combo.place(x=200, y=20)

        self.entry_gos_nomer = ttk.Entry(self, width=23)
        self.entry_gos_nomer.place(x=200, y=50)

        self.brend_auto_combobox = ttk.Combobox(self, values=brend_auto, state="readonly")
        self.brend_auto_combobox.current(1)
        self.brend_auto_combobox.place(x=200, y=80)

        self.brend_battary_combobox = ttk.Combobox(self, values=battary_brend, state="readonly")
        self.brend_battary_combobox.current(1)
        self.brend_battary_combobox.place(x=200, y=110)

        self.kol_battary_spinbox = ttk.Spinbox(self, from_=1, to=10, state="readonly")
        self.kol_battary_spinbox.place(x=200, y=140)

        self.description = ttk.Combobox(self, values=jobs_text, width=70, state="readonly")# Поле ввода выполненных работ
        self.description.current(1)
        self.description.place(x=200, y=170)

        self.density_do_combobox = ttk.Combobox(self, values=density_up_to, state="readonly")
        self.density_do_combobox.current(0)
        self.density_do_combobox.place(x=200, y=210)

        self.density_posle = ttk.Combobox(self, values=density_after, state="readonly")
        self.density_posle.current(4)
        self.density_posle.place(x=200, y=240)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=280)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=200, y=280)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.my_data_combo.get(),
                                                                       self.entry_gos_nomer.get(),
                                                                       self.brend_auto_combobox.get(),
                                                                       self.brend_battary_combobox.get(),
                                                                       self.kol_battary_spinbox.get(),
                                                                       self.description.get(),
                                                                       self.density_do_combobox.get(),
                                                                       self.density_posle.get()
                                                                       ))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать запись')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=200, y=280)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.my_data_combo.get(),
                                                                          self.entry_gos_nomer.get(),
                                                                          self.brend_auto_combobox.get(),
                                                                          self.brend_battary_combobox.get(),
                                                                          self.kol_battary_spinbox.get(),
                                                                          self.description.get(),
                                                                          self.density_do_combobox.get(),
                                                                          self.density_posle.get(),
                                                                          ))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM battary WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_gos_nomer.insert(0, row[2])
        if row[2] != '':
            self.kol_battary_spinbox.insert(0, row[1])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
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


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('battary.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS battary (id integer primary key, my_data TEXT, gos_nomer TEXT, 
                                                   brend_auto TEXT, brend_battary TEXT, kol_battary TEXT, 
                                                   description TEXT, density_do TEXT, density_posle TEXT)''')
        self.conn.commit()

    def insert_data(self, my_data, gos_nomer, brend_auto, brend_battary, kol_battary, description, density_do, density_posle):
        self.c.execute('''INSERT INTO battary(my_data, gos_nomer, brend_auto, brend_battary, kol_battary, 
                                              description, density_do, density_posle) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (my_data, gos_nomer, brend_auto, brend_battary, kol_battary, description, density_do, density_posle))
        self.conn.commit()


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
    
