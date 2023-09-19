from tkinter import *



class Reg_user:
    def __init__(self, parent, width, height, title="Регистрация работника", resizable=(False, False)):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+390+180")
        self.root.resizable(resizable[0], resizable[1])
        self.root.iconphoto(True, PhotoImage(file=("resources/logo_sto.png")))
        
        self.reg_User()
        self.modal_window()
        
    def modal_window(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
    
        
    def reg_User(self):
        self.lbl_description = Label(self.root, text="Регистрация или вход работника", font=16, fg="green")
        self.lbl_description.grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
        
        self.user_name = Label(self.root, text="ИМЯ РАБОТНИКА")
        self.user_name.grid(row=1, column=0, sticky="w", padx=12, pady=5)
        
        self.user_pass = Label(self.root, text="ПАРОЛЬ")
        self.user_pass.grid(row=2, column=0, sticky="w", padx=12, pady=5)
        
        
        self.user_name_ent = Entry(self.root, width=24)
        self.user_name_ent.grid(row=1, column=1, padx=10, pady=5)
        
        self.user_pass_ent = Entry(self.root, width=24, show="*")
        self.user_pass_ent.grid(row=2, column=1, padx=10, pady=5)
        
        self.in_btn = Button(self.root, text="Войти", width=8, bg="#87CEFA", activebackground="lightgreen")
        self.in_btn.grid(row=5, column=1, padx=8, pady=15, sticky="w")
        
        self.save_btn = Button(self.root, text="Сохранить", width=8, bg="#87CEFA", activebackground="lightgreen")
        self.save_btn.grid(row=5, column=1, padx=8, pady=15, sticky="e")

    def verification():
        username = user_name_ent.get()
        passwd = user_pass_ent.get()
        x = f"SELECT username, passwd FROM users WHERE username = '{username}' AND passwd = '{passwd}';"
        cur.execute(x)
    
        if not cur.fetchall():
            mb.showinfo("Регистрация работника", f"{username}, пароль не совпадает!")
        else:    
            mb.showinfo("Регистрация работника", f"Вы авторизованы, {username}!")
            root.destroy()

