from tkinter import *
from os import *
from sys import *
from tkinter import font
from tkinter.ttk import Combobox
from tkinter import scrolledtext
from tkinter.ttk import Progressbar
from tkinter import Frame, Text, Scrollbar, Pack, Grid, Place
from tkinter.constants import RIGHT, LEFT, Y, BOTH
from tkinter import messagebox
from datetime import date
from reg_user import Reg_user

def messeng_save():
    messagebox.showinfo("Всё получилось!", "Данные записаны!")
    
def btn_print():
    messagebox.showinfo("Печать!", "Печать документа!")
    
current_date = date.today().strftime("%d-%m-%Y")


combo_auto = ['MITSUBISHI', 'KREMCO', 'MAN', 'УАЗ', 'НИВА', 'КАМАЗ',
              'КРАЗ','УРАЛ', 'МАЗ', 'НАСОСНЫЙ БЛОК']

combo_akb = ("6СТ-62", "6СТ-75", "6СТ-90", "6СТ-100", "6СТ-132",
             "6СТ-140", "6СТ-180", "6СТ-182", "6СТ-190", "6СТ-225")

combo_density_up_to = ("1.20 г/см3", "1.21 г/см3", "1.21 г/см3", "1.22 г/см3", "1.23 г/см3",
                       "1.24 г/см3", "1.25 г/см3", "1.26 г/см3", "1.27 г/см3", "1.28 г/см3",
                       "1.29 г/см3")

combo_density_after = ("1.25 г/см3", "1.26 г/см3", "1.27 г/см3",
                       "1.28 г/см3", "1.29 г/см3", "1.30 г/см3")

class Battery:
    def __init__(self, width, height, title="Ремонт и оборот аккумуляторных батарей",
                 resizable=(False, False)):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+250+230")
        self.root.resizable(resizable[0], resizable[1])
        self.root.iconphoto(True, PhotoImage(file=("resources/logo_sto.png")))    
        
    def b_quit(self):
        choise = messagebox.askyesno("Выход", "Вы точно хотите выйти?")
        if choise:
            self.root.destroy()
            
    def add_auto(self):
        self.combo_auto = self.combo_auto.append()
        ad_auto = messagebox.askokcancel("Добавление ТС", "Добавить марку автомобиля?")
        if ad_auto:
            self.root.destroy()
            
    def draw_widget(self):
        
        # Заголовок
        self.lbl1 = Label(self.root, text="Информация об аккумуляторных батареях", font=16, fg="green")
        self.lbl1.grid(row=0, column=0, columnspan=3, ipadx=8, ipady=10, padx=5)
        
        # Вывод даты, гос.номера, марки автомобиля, марки АКБ и прочего (ПЕРВЫЙ СТОЛБЕЦ)
        self.lbl_cur_data = Label(self.root, text="Дата: ", width=18, anchor="w")
        self.lbl_gos_nomer = Label(self.root, text="Гос. номер: ", anchor="w", width=18)
        self.lbl_brend_auto = Label(self.root, text="Марка ТС: ", width=18, anchor="w")
        self.lbl_battary_brend = Label(self.root, text="Марка АКБ: ", width=18, anchor="w")
        self.lbl_completed_works = Label(self.root, text="Вид работ: ", width=18, anchor="w")
        self.lbl_density_up_to = Label(self.root, text="Плотность до: ", width=18, anchor="w")
        self.lbl_density_after = Label(self.root, text="Плотность после: ", width=18, anchor="w")
                
        self.lbl_cur_data.grid(row=1, column=0, sticky="e", padx=18, pady=5)        
        self.lbl_gos_nomer.grid(row=2, column=0, sticky="e", padx=18, pady=5)        
        self.lbl_brend_auto.grid(row=3, column=0, sticky="e", padx=18, pady=5)       
        self.lbl_battary_brend.grid(row=4, column=0, sticky="e", padx=18, pady=5)
        self.lbl_completed_works.grid(row=5, column=0, sticky="ne", padx=18, pady=5)
        self.lbl_density_up_to.grid(row=6, column=0, sticky="e", padx=18, pady=5)        
        self.lbl_density_after.grid(row=7, column=0, sticky="e", padx=18, pady=5)
        
        # Вывод даты, гос.номера, марки автомобиля, марки АКБ и прочего (ВТОРОЙ СТОЛБЕЦ)
        self.ent_data = Combobox(self.root, width=16, values=current_date, state='readonly')# Дата
        self.ent_gos_nomer = Entry(self.root, width=18) # Гос. номер автомобиля
        self.combo_auto = Combobox(self.root, width=16, values=combo_auto, state='readonly') # Марка автомобиля
        self.combo_akb = Combobox(self.root, width=16, values=combo_akb, state='readonly') # Марка аккумулятора
        self.completed_works = scrolledtext.ScrolledText(self.root, width=53, height=3, wrap=WORD)
        self.combo_density_up_to = Combobox(self.root, width=16, values=combo_density_up_to, state='readonly') # Плотность электролита до выполненных работ
        self.combo_density_after = Combobox(self.root, width=16, values=combo_density_after, state='readonly') # Плотность электролита после выполненных работ
        
        # Ввод даты
        self.ent_data.current("0")
        self.ent_data.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Ввод гос. номера
        self.ent_gos_nomer.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Модель транспортного средства
        self.combo_auto.current("3")
        self.combo_auto.grid(row=3, column=1,  sticky="w", padx=5, pady=5)
        
        # Марка аккумуляторной батареи
        self.combo_akb.current("0")
        self.combo_akb.grid(row=4, column=1,  sticky="w", padx=5, pady=5)
        
        # Вывод о выполненых работах
        self.completed_works.grid(row=5, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Плотность электролита до
        self.combo_density_up_to.current("5")
        self.combo_density_up_to.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        
        # Плотность электролита после
        self.combo_density_after.current("3")      
        self.combo_density_after.grid(row=7, column=1, sticky="w", padx=5, pady=5)
        
        # Кнопка добавления марки автомобиля в список
        self.add_marka_auto = Button(self.root, text="Дабавить", width=14, 
                                     bg="#87CEFA", activebackground="lightgreen", command=self.add_auto)
        self.add_marka_auto.grid(row=3, column=2, sticky="e", padx=5, pady=5)
        
        # Выбор колличества АКБ
        self.add_kol_akb = Spinbox(self.root, width=15, from_=1, to=10, state="readonly")
        self.add_kol_akb.grid(row=4, column=2, sticky="e", padx=5, pady=5)
        
        # Кнопки "Сохранить", "Печать", "Выход"
        self.btn_save = Button(self.root, text="Сохранить", width=14, bg="#87CEFA",
                               activebackground="lightgreen", command=messeng_save)
        self.btn_print = Button(self.root, text="Печать", width=14, bg="#87CEFA",
                                activebackground="lightgreen", command=btn_print)
        self.btn_quit = Button(self.root, text="Выход", width=14, bg="#87CEFA",
                               activebackground="red", command=self.b_quit)
        
        # Кнопки "Сохранить", "Печать", "Выход"
        self.btn_save.grid(row=8, column=0, sticky='w', padx=12, pady=15)
        self.btn_print.grid(row=8, column=2, sticky='e', padx=12)
        self.btn_quit.grid(row=9, column=2, sticky='e', padx=12)
        
    def progress(self):
        pass
             
    # Окно регистрации работника
    def registration(self, width, height, title="Регистрация работника", resizable=(False, False)):
        Reg_user(self.root, width, height, title, resizable)
        
    def start(self):
        self.draw_widget()
        self.root.mainloop()

if __name__ == "__main__":
    akb = Battery(650, 450)
    akb.registration(370, 180)
    akb.start()
