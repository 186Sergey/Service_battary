import tkinter as tk
from tkinter import filedialog, messagebox as mb
from tkinter import PhotoImage, ttk
from datetime import datetime, timedelta
import error as err
import os
import sqlite3
import sys

import settings
from settings import MDASH, LAQIO, RAQIO, BULLET, LES_THAN, CREATOR_THAN, battery_brand, density_up_to, density_after


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('battery.db')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS battery (
            id integer primary key, 
            my_data TEXT, 
            gos_nomer TEXT, 
            brand_auto TEXT, 
            brand_battery TEXT, 
            kol_battery INTEGER, 
            description TEXT, 
            density_up_to TEXT, 
            density_after TEXT)''')
        self.conn.commit()

    def insert_data(
            self,
            my_data,
            gos_nomer,
            brand_auto,
            brand_battery,
            kol_battery,
            description,
            density_up_to,
            density_after):
        self.c.execute('''INSERT INTO battery(
        my_data, 
        gos_nomer, 
        brand_auto, 
        brand_battery, 
        kol_battery, 
        description, 
        density_up_to, 
        density_after 
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (my_data,
                        gos_nomer,
                        brand_auto,
                        brand_battery,
                        kol_battery,
                        description,
                        density_up_to,
                        density_after))
        self.conn.commit()

class Main(tk.Frame):
    def __init__(self, root, db, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.init_main()

        self.db = db

        # Настраиваем теги
        self.tree.tag_configure('bad_density', background='#ffcccc', foreground='#b00000')
        self.tree.tag_configure('new_battery', background='#e0f7fa', foreground='#005f73')
        self.tree.tag_configure('normal', background='#ffffff', foreground='#000000')
        self.tree.tag_configure('my_date', background='#ffffff', foreground='#0000cc')

        self.view_records()

    def init_main(self):

        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = PhotoImage(file='add.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редакция', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.backupdb_img = PhotoImage(file='backupdb.gif')
        btn_backupdb = tk.Button(toolbar, text='Backup', bg='#d7d8e0', bd=0, image=self.backupdb_img,
                                compound=tk.TOP, command=self.backupdb)
        btn_backupdb.pack(side=tk.LEFT)

        self.restoredb_img = PhotoImage(file='restoredb.gif')
        btn_restoredb = tk.Button(toolbar, text='Restore', bg='#d7d8e0', bd=0, image=self.restoredb_img,
                                compound=tk.TOP, command=self.restoredb)
        btn_restoredb.pack(side=tk.LEFT)

        self.help_img = PhotoImage(file='helpmi.png')
        btn_help = tk.Button(toolbar, text='Помощь', bg='#d7d8e0', bd=0, image=self.help_img,
                                  compound=tk.TOP, command=self.show_help)
        btn_help.pack(side=tk.LEFT)

        self.avatarka = PhotoImage(file='AE_logo.png')
        btn_avatarka = tk.Button(toolbar, text="", bg='#d7d8e0', bd=0,
                                      image=self.avatarka, compound=tk.TOP, command=self.add_avatar)
        btn_avatarka.pack(side=tk.RIGHT, padx=8)

        self.tree = ttk.Treeview(self, columns=('ID', 'my_data', 'gos_nomer', 'brand_auto', 'brand_battery',
                                                'kol_battery', 'description', 'density_up_to', 'density_after'),
                                                height=50, show='headings')

        self.status_label = tk.Label(self,
                                     text="",
                                     fg="#000000",
                                     background="#f0f0f0",
                                     height=2,
                                     font=('Segoe UI', 12),
                                     anchor='w',
                                     padx=8,
                                     pady=4)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)

        self.tree.column('ID', width=35, anchor=tk.CENTER)
        self.tree.column('my_data', width=90, anchor=tk.CENTER)
        self.tree.column('gos_nomer', width=90, anchor=tk.W)
        self.tree.column('brand_auto', width=120, anchor=tk.W)
        self.tree.column('brand_battery', width=90, anchor=tk.W)
        self.tree.column('kol_battery', width=80, anchor=tk.W)
        self.tree.column('description', width=450, anchor=tk.W)
        self.tree.column('density_up_to', width=130, anchor=tk.CENTER)
        self.tree.column('density_after', width=130, anchor=tk.CENTER)

        self.tree.heading('ID', text='№')
        self.tree.heading('my_data', text='Дата')
        self.tree.heading('gos_nomer', text='Гос номер')
        self.tree.heading('brand_auto', text='Марка ТС')
        self.tree.heading('brand_battery', text='Марка АКБ')
        self.tree.heading('kol_battery', text='Кол-во АКБ')
        self.tree.heading('description', text='Вид работ')
        self.tree.heading('density_up_to', text='Плотность до:')
        self.tree.heading('density_after', text='Плотность после:')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def _get_row_tag(self, row):
        density_up = row['density_up_to']
        density_after = row['density_after']
        my_date = row['my_data']

        density_up_clean = self._clean_density(density_up)
        density_after_clean = self._clean_density(density_after)

        # Сначала проверяем «плохо»
        if isinstance(density_up, str) and density_up.strip().upper() == 'ВОДА':
            return 'bad_density'
        if density_up_clean is not None and density_up_clean <= 1.23:
            return 'bad_density'

        # Потом «новое»
        is_new_by_date = False
        if my_date:
            try:
                dt = datetime.strptime(str(my_date).strip(), '%d-%m-%Y')
                is_new_by_date = (datetime.now() - dt) <= timedelta(days=10)
            except ValueError:
                pass

        is_new_by_density = False
        if density_up_clean is not None and density_after_clean is not None:
            is_new_by_density = (density_up_clean >= 1.27 and density_after_clean >= 1.29)

        if is_new_by_date or is_new_by_density:
            return 'new_battery'

        return 'normal'

    @staticmethod
    def _clean_density(value):
        if value is None:
            return None
        s = str(value).strip()
        # Убираем единицы измерения
        for unit in ["г/см3", "г/см³", "g/cm3"]:
            s = s.replace(unit, "").strip()
        # Заменяем запятую на точку
        s = s.replace(",", ".").strip()
        try:
            return float(s)
        except (ValueError, TypeError):
            return None

    def set_status_label(self, text: str, color: str):
        # _set_status_label - это tk.Label для статуса
        if hasattr(self, "status_label") and self.status_label:
            self.status_label.config(text=text, fg=color)

    def records(self,
                my_data,
                gos_nomer,
                brand_auto,
                brand_battery,
                kol_battery,
                description,
                density_up_to,
                density_after):
        self.db.insert_data(my_data,
                            gos_nomer.upper(),
                            brand_auto.upper(),
                            brand_battery,
                            kol_battery,
                            description,
                            density_up_to,
                            density_after)
        self.view_records()
        self.set_status_label(f"Запись добавлена в БД", color="#00bb00")
        mb.showinfo('Запись', f'В базу данных добавлена новая запись.\n\nНе '
                              f'забудьте сделать резервную копию БД.'
                    )

    def update_record(self,
                      my_data,
                      gos_nomer,
                      brand_auto,
                      brand_battery,
                      kol_battery,
                      description,
                      density_up_to,
                      density_after):
        selected = self.tree.selection()
        if not selected:
            return
        record_id = self.tree.set(selected[0], '#1')
        self.db.c.execute('''UPDATE battery SET 
        my_data=?, 
        gos_nomer=?, 
        brand_auto=?, 
        brand_battery=?, 
        kol_battery=?,
        description=?, 
        density_up_to=?, 
        density_after=? 
        WHERE ID=?''', (my_data,
                        gos_nomer,
                        brand_auto,
                        brand_battery,
                        kol_battery,
                        description,
                        density_up_to,
                        density_after,
                        record_id))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rows = self.db.c.execute("SELECT * FROM battery").fetchall()
            for row in rows:
                values_tuple = (
                    row['id'],
                    row['my_data'],
                    row['gos_nomer'],
                    row['brand_auto'],
                    row['brand_battery'],
                    row['kol_battery'],
                    row['description'],
                    row['density_up_to'],
                    row['density_after']
                )

                tag = self._get_row_tag(row)
                self.tree.insert('', 'end', values=values_tuple, tags=(tag,))

            self.set_status_label(f"Отображено записей: {len(rows)}", color="#008000")

        except sqlite3.Error as e:
            err_msg = f"Ошибка при просмотре записей: {e}"
            err.Error.log(err_msg)
            self.set_status_label(err_msg, color="#ff0000")
        except Exception as e:
            err_msg = f"Неожиданная ошибка: {e}"
            err.Error.log(err_msg)
            self.set_status_label(err_msg, color="#ff0000")

    def delete_records(self):
        selected = self.tree.selection()

        if not selected:
            self.set_status_label("Сначала выделите запись для удаления", color="#8b4513")
            return

        count = len(selected)
        confirm_msg = (
            "Данная операция необратима!\n"
            f"Вы точно хотите удалить {count} запис{'и' if 2 <= count <= 4 else 'ь' if count == 1 else 'ей'}?\n"
            "Все данные будут потеряны."
        )

        # Спрашиваем ОДИН РАЗ перед удалением
        if not mb.askyesno("Удаление записи", confirm_msg):
            self.set_status_label("Удаление отменено пользователем", color="#8b4513")
            return

        deleted_ids = []

        try:
            with self.db.conn:
                for item in selected:
                    record_id = self.tree.set(item, '#1')
                    self.db.c.execute('DELETE FROM battery WHERE id=?', (record_id,))
                    deleted_ids.append(record_id)

            # После успешного коммита обновляем таблицу
            self.view_records()

            if len(deleted_ids) == 1:
                msg = f"Вы удалили запись под номером {deleted_ids[0]}"
            else:
                msg = f"Вы удалили {len(deleted_ids)} запис{'и' if 2 <= count <= 4 else 'ь' if count == 1 else 'ей'}"

            self.set_status_label(msg, color="#00bb00")

        except Exception as e:
            err.Error.log(f"Ошибка при удалении записей: {e}")
            self.set_status_label(f"Ошибка удаления: {e}", color="#ff0000")

    # --- Основной метод поиска ---

    def search_records(self, gos_nomer: str):
        """
        Поиск по гос. номеру: подсветка проблемных и новых АКБ.
        Приоритет: сначала проверяем «плохо» (красный), если не плохо — смотрим «новое» (голубой).
        """
        pattern = f'%{gos_nomer}%'

        # Очищаем дерево
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rows = self.db.c.execute(
                "SELECT * FROM battery WHERE gos_nomer LIKE ?",
                (pattern,)
            ).fetchall()

            if not rows:
                self.set_status_label(
                    f"Автомобиль с номером {gos_nomer} в таблице отсутствует",
                    color="#ff0000"
                )
                return

            for row in rows:
                values_tuple = (
                    row['id'],
                    row['my_data'],
                    row['gos_nomer'],
                    row['brand_auto'],
                    row['brand_battery'],
                    row['kol_battery'],
                    row['description'],
                    row['density_up_to'],
                    row['density_after']
                )

                tag = self._get_row_tag(row)
                self.tree.insert('', 'end', values=values_tuple, tags=(tag,))

            first = rows[0]
            msg = (
                f"Найдено записей: {len(rows)}. "
                f"Марка автомобиля {MDASH} {first['brand_auto']}, "
                f"государственный номер {MDASH} {first['gos_nomer']}."
            )
            self.set_status_label(msg, color="#00bb00")

        except sqlite3.Error as e:
            err_msg = f"Ошибка БД при поиске: {e}"
            err.Error.log(err_msg)
            self.set_status_label(err_msg, color="#ff0000")
        except Exception as e:
            err_msg = f"Неожиданная ошибка при поиске: {e}"
            err.Error.log(err_msg)
            self.set_status_label(err_msg, color="#ff0000")

    def _is_float_le(self, value, threshold: float) -> bool:
        """True, если value — число и <= threshold. Иначе False."""
        if value is None:
            return False
        try:
            # Нормализуем: убираем пробелы, приводим к строке, потом к float
            clean_val = str(value).strip()
            return float(clean_val) <= threshold
        except (ValueError, TypeError):
            return False

    def _is_float_ge(self, value, threshold: float) -> bool:
        """True, если value — число и >= threshold. Иначе False."""
        if value is None:
            return False
        try:
            clean_val = str(value).strip()
            return float(clean_val) >= threshold
        except (ValueError, TypeError):
            return False

    def backupdb(self):
        """
        Создание резервной копии БД с выбором файла, логами и цветной индикацией.
        """
        # Имя файла по умолчанию
        default_name = datetime.now().strftime("BackUp_%d-%m-%Y_%H-%M-%S.sql")
        # Выбор файла пользователем
        backup_path = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".sql",
            filetypes=[('SQL files', '*.sql'), ('All files', '*.*')],
            title="Выберите место и имя для резервной копии БД",
        )
        if not backup_path:
            self.set_status_label("Резервное копирование отменено пользователем.", color='#8b4513')
            return

        # Предупреждение о рисках

        confirm = mb.askyesno(
            "Предупреждение",
            "Если файл уже существует, он будет перезаписан.\n"
            "Продолжить?"
        )
        if not confirm:
            self.set_status_label("Резервное копирование отменено пользователем.", color='#8b4513')
            return
        try:
            # Дата и время для комментария в файле
            backup_timestamp = datetime.now().strftime("%d-%m-%Y | %H:%M:%S")
            # Отдельное соединение для дампа
            with sqlite3.connect("battery.db") as conn:
                with open(backup_path, 'w', encoding="utf-8",newline="\n") as backup:
                    # Комментарий с датой и временем, сразу видно, когда сделан дамп
                    backup.write(f"-- BackUp created: {backup_timestamp}\n")
                    # Страховочные команды для восстановления дампа
                    backup.write("DROP TABLE IF EXISTS battery;\n")
                    backup.write(
                        "CREATE TABLE IF NOT EXISTS battery ("
                        "id integer primary key, "
                        "my_data TEXT, "
                        "gos_nomer TEXT, "
                        "brand_auto TEXT, "
                        "brand_battery TEXT, "
                        "kol_battery INTEGER, "
                        "description TEXT, "
                        "density_up_to TEXT, "
                        "density_after TEXT);\n"
                    )
                    for line in conn.iterdump():
                        # Пропускаем строки создания таблицы, потому что уже написали свою
                        if line.startswith("CREATE TABLE battery"):
                            continue
                        # ЯВНЫЙ ПЕРЕВОД СТРОКИ - ТАК БЕЗОПАСТНЕЕ
                        backup.write(f"{line}\n")

            # Успех: зелёный цвет, сообщение
            success_msg = "Резервная копия успешно создана!"
            self.set_status_label(success_msg, color="#00bb00")
            mb.showinfo("Успех", success_msg)
        except err.Exception as e:
            # Ошибка: красный цвет, запись в лог, сообщение
            err_msg = f"Ошибка при создании резервной копии: {e}"
            # Запись в errors.log.txt
            err.Error.log(err_msg)
            self.set_status_label(err_msg, color="#ff0000")
            mb.showerror("Ошибка", err_msg)

    def restoredb(self):
        """Восстановление БД из резервной копии.\n
           Restoring a database from a backup.
        """
        restore_path = filedialog.askopenfilename(
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")],
            title="Выберите SQL-файл для восстановления"
        )
        if not restore_path:
            self.set_status_label("Восстановление отменено пользователем.", color='#8b4513')
            return

        confirm = mb.askyesno(
            "Внимание",
            "Это полностью перезапишет текущую базу данных!\n"
            "Все текущие данные будут потеряны!\n\nПродолжить?"
        )
        if not confirm:
            self.set_status_label("Восстановление отменено пользователем.", color="#8b4513")
            return

        try:
            with open(restore_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            # Текущее соединение должно быть ЗАКРЫТЫМ!!!
            if hasattr(self, "db") and self.db and self.db.conn:
                self.db.conn.close()
                self.db.conn = None

            with sqlite3.connect("battery.db") as conn:
                cursor = conn.cursor()
                cursor.executescript(sql_script)
                conn.commit()

                # После успешного восстановления, снова открываем соединение с БД
                self.db = DB()

                msg = "База данных успешно восстановлена из SQL-дампа."
                self.set_status_label(msg, color="#00bb00")
                mb.showinfo("Успех", msg)

                self.view_records()

                msg = "База данных успешно обновлена после восстановления из SQL-дампа."
                self.set_status_label(msg, color="#00bb00")

        except Exception as e:
            err_msg = f"Ошибка восстановления: {e}"
            err.Error.log(err_msg)
            self.set_status_label(err_msg, color="#ff0000")
            mb.showerror("Ошибка восстановления.", err_msg)

    def add_avatar(self):
        """Вывести фотографию работника, который авторизовался.\n
           Display a photo of the employee who logged in.
        """
        mb.showinfo("Авторизация", "Функция авторизации в разработке.\nСейчас Вы администратор.")

    def open_dialog(self):
        Child(self.master, self)

    def open_update_dialog(self):
        selected = self.tree.selection()
        if not selected:
            self.set_status_label("Сначала выделите запись для редактирования.", color="#8b4513")
            mb.showwarning("Внимание", "Пожалуйста, выделите одну из строк для редактирования в таблице БД.")
            return
        Update(self)

    def open_search_dialog(self):
        Search(self)

    def show_help(self):
        HelpWindow(self)


class Child(tk.Toplevel):
    """
    Окно добавления новой записи.
    Главное правило: здесь только собираем и проверяем данные.
    Сама запись в БД происходит в Main.records, сюда мы только передаём чистые данные.
    """

    def __init__(self, root, app):
        """
        root — родительское окно (обычно Main.root)
        app — экземпляр главного окна (Main), чтобы вызывать у него .records (INSERT)
        """
        super().__init__(root)

        # Сохраняем ссылку на главное окно, чтобы потом вызвать self.view.records
        self.view = app

        # Объявляем все поля заранее (None), чтобы IDE и линтер не ругались
        # Это хорошая привычка: сразу видно, какие виджеты будут у класса
        self.my_data_ent = None
        self.entry_gos_nomer = None
        self.brand_auto_entry = None
        self.brand_battery_combobox = None
        self.kol_battery_spinbox = None
        self.description = None
        self.density_up_to_combobox = None
        self.density_after = None

        self.init_child()

    def init_child(self):
        """Настройка внешнего вида окна и всех виджетов"""
        self.title('Добавить запись об аккумуляторах')
        self.geometry('670x385+370+245')
        self.resizable(False, False)  # Запрещаем менять размер — для формы это обычно удобнее

        # --- Подписи к полям ---
        labels = [
            ('Дата: (ДД-ММ-ГГГГ)', 50, 20),
            ('Гос номер:', 50, 50),
            ('Марка ТС:', 50, 80),
            ('Марка АКБ:', 50, 110),
            ('Кол-во АКБ:', 50, 140),
            ('Вид работ:', 50, 170),
            ('Плотность до:', 50, 200),
            ('Плотность после:', 50, 230),
        ]
        # Цикл для подписей — меньше повторяющегося кода
        for text, x, y in labels:
            tk.Label(self, text=text).place(x=x, y=y)

        # --- Поле: Дата ---
        self.my_data_ent = ttk.Entry(self, width=23)
        default_data = datetime.now().strftime("%d-%m-%Y")
        self.my_data_ent.insert(0, default_data)  # Подставляем текущую дату по умолчанию
        self.my_data_ent.place(x=200, y=20)

        # --- Поле: Гос. номер ---
        self.entry_gos_nomer = ttk.Entry(self, width=23)
        self.entry_gos_nomer.place(x=200, y=50)

        # --- Поле: Марка ТС ---
        self.brand_auto_entry = ttk.Entry(self, width=23)
        self.brand_auto_entry.place(x=200, y=80)

        # --- Выпадающий список: Марка АКБ ---
        self.brand_battery_combobox = ttk.Combobox(self, values=battery_brand, state="readonly")
        self.brand_battery_combobox.current(1)  # Выбираем второй элемент по умолчанию (индекс 1)
        self.brand_battery_combobox.place(x=200, y=110)

        # --- Счётчик: Кол-во АКБ ---
        self.kol_battery_spinbox = ttk.Spinbox(self, from_=1, to=10, state="readonly")
        self.kol_battery_spinbox.place(x=200, y=140)

        # --- Поле: Вид работ (описание) ---
        self.description = ttk.Entry(self, width=70, font=('Times New Roman', 9))
        self.description.place(x=200, y=170)

        # --- Выпадающий список: Плотность до ---
        self.density_up_to_combobox = ttk.Combobox(self, values=density_up_to, state="readonly")
        self.density_up_to_combobox.current(0)
        self.density_up_to_combobox.place(x=200, y=200)

        # --- Выпадающий список: Плотность после ---
        self.density_after = ttk.Combobox(self, values=density_after, state="readonly")
        self.density_after.current(4)
        self.density_after.place(x=200, y=230)

        # --- Кнопка: Отмена (передумал) ---
        btn_cancel = ttk.Button(self, text='Отмена', command=self.destroy)
        btn_cancel.place(x=350, y=280)
        # ВАЖНО: self.destroy() просто закрывает окно.
        # Никакой записи в БД не происходит — это и есть поведение «передумал».

        # --- Кнопка: Добавить ---
        self.btn_ok = ttk.Button(self, text='Добавить')
        # Не используем lambda здесь: логика проверки вынесена в отдельный метод on_add
        self.btn_ok.config(command=self.on_add)
        self.btn_ok.place(x=200, y=280)

        # Делаем окно модальным: пока оно открыто, нельзя кликать по главному окну.
        # Это помогает избежать случайных действий и чётко разделяет «думаем» и «делаем».
        self.grab_set()
        self.focus_set()

    # ---------------------------------------------------------
    # Вся валидация (проверка) происходит здесь, ДО записи в БД
    # ---------------------------------------------------------
    def on_add(self):
        # 1. Сбор данных
        my_data = self.my_data_ent.get().strip()
        gos_nomer = self.entry_gos_nomer.get().strip().upper()
        brand_auto = self.brand_auto_entry.get().strip().upper()
        brand_battery = self.brand_battery_combobox.get()
        kol_battery = self.kol_battery_spinbox.get()
        description = self.description.get().strip()
        density_up_to = self.density_up_to_combobox.get()
        density_after = self.density_after.get()

        # 2. Проверка на пустоту обязательных полей
        required = {
            'Дата': my_data,
            'Гос. номер': gos_nomer,
            'Марка ТС': brand_auto,
            'Марка АКБ': brand_battery,
            'Кол-во АКБ': kol_battery,
            'Вид работ': description,
        }
        for name, value in required.items():
            if not value:
                mb.showerror('Ошибка', f'Поле "{name}" не должно быть пустым.')
                return

        # 3. Проверка даты
        try:
            datetime.strptime(my_data, '%d-%m-%Y')
        except ValueError:
            mb.showerror(
                'Ошибка даты',
                'Дата должна быть строго в формате ДД-ММ-ГГГГ.\n'
                'Например: 25-07-2026'
            )
            return

        # ---------------------------------------------------------
        # ВАЛИДАЦИЯ ГОС. НОМЕРА ЧЕРЕЗ СПИСОК (без re)
        # Разрешённые буквы: А В У К Е Х О Р С М Т
        # Латиница: A B C E K X M P H O T
        # Цифры, дефис, пробел
        # ---------------------------------------------------------
        allowed_gos_chars = set(
            'АВУКЕХОРСМТ'           # кириллица
            'ABCEKXMPHOT'           # латиница
            '0123456789'            # цифры
            '- '                    # дефис и пробел
        )

        if any(ch not in allowed_gos_chars for ch in gos_nomer):
            mb.showerror(
                'Ошибка гос. номера',
                'В гос. номере разрешены только:\n'
                '- цифры,\n'
                '- дефис и пробел,\n'
                '- буквы: А, В, У, К, Е, Х, О, Р, С, М, Т\n'
                '(и их латинские аналоги: A, B, C, E, K, X, M, P, H, O, T).'
            )
            return

        # ---------------------------------------------------------
        # ВАЛИДАЦИЯ МАРКИ АВТО (тоже без re)
        # Тут можно разрешить все буквы кириллицы и латиницы + цифры, дефис, пробел.
        # Если хочешь строже — просто уменьши списки.
        # ---------------------------------------------------------
        allowed_auto_chars = set(
            'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # кириллица полная
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'         # латиница
            '0123456789'                         # цифры
            '- '                                 # дефис и пробел
        )

        if any(ch not in allowed_auto_chars for ch in brand_auto):
            mb.showerror(
                'Ошибка марки ТС',
                'Марка ТС может содержать только буквы (кириллица/латиница), цифры, дефис и пробел.'
            )
            return

        # 6. Передача в Main.records для записи в БД
        self.view.records(
            my_data,
            gos_nomer,
            brand_auto,
            brand_battery,
            kol_battery,
            description,
            density_up_to,
            density_after
        )

        self.destroy()

class Update(Child):
    def __init__(self, parent_main):
        # parent_main — это экземпляр Main (чтобы получить доступ к tree, db и т.д.)
        self.parent_main = parent_main
        self.selected_id = None

        # Сначала получаем ID выбранной строки, чтобы не потерять при создании окна
        selected = self.parent_main.tree.selection()
        if not selected:
            # Если ничего не выделено — просто закрываем, это уже обработано в Main
            self.destroy()
            return

        self.selected_id = self.parent_main.tree.set(selected[0], '#1')

        # Теперь правильно инициализируем родителя (Child)
        super().__init__(self.parent_main.master, self.parent_main)

        self.init_edit()
        self.default_data()

    def init_edit(self):
        self.title('Редактировать запись')
        # Убираем кнопку "Добавить" из Child, если она там есть
        if hasattr(self, 'btn_ok') and self.btn_ok:
            self.btn_ok.destroy()

        btn_edit = ttk.Button(self, text='Сохранить изменения')
        btn_edit.place(x=200, y=280)
        btn_edit.config(command=self.on_edit)

    def default_data(self):
        """Заполняем поля текущими данными из БД по ID"""
        if self.selected_id is None:
            mb.showerror('Ошибка', 'Не удалось определить ID записи для редактирования.')
            self.destroy()
            return

        try:
            row = self.parent_main.db.c.execute(
                'SELECT * FROM battery WHERE id=?',
                (self.selected_id,)
            ).fetchone()

            if not row:
                mb.showerror('Ошибка', 'Запись не найдена в базе данных.')
                self.destroy()
                return

            # Заполняем поля (индексы совпадают с SELECT *)
            self.my_data_ent.delete(0, tk.END)
            self.my_data_ent.insert(0, row['my_data'] or '')

            self.entry_gos_nomer.delete(0, tk.END)
            self.entry_gos_nomer.insert(0, row['gos_nomer'] or '')

            self.brand_auto_entry.delete(0, tk.END)
            self.brand_auto_entry.insert(0, row['brand_auto'] or '')

            # Для комбобоксов нужно найти индекс значения
            if row['brand_battery'] in battery_brand:
                idx = battery_brand.index(row['brand_battery'])
                self.brand_battery_combobox.current(idx)
            else:
                self.brand_battery_combobox.set(row['brand_battery'] or '')

            # Spinbox: просто устанавливаем значение
            self.kol_battery_spinbox.set(row['kol_battery'] or 1)

            self.description.delete(0, tk.END)
            self.description.insert(0, row['description'] or '')

            if row['density_up_to'] in density_up_to:
                idx = density_up_to.index(row['density_up_to'])
                self.density_up_to_combobox.current(idx)
            else:
                self.density_up_to_combobox.set(row['density_up_to'] or '')

            if row['density_after'] in density_after:
                idx = density_after.index(row['density_after'])
                self.density_after.current(idx)
            else:
                self.density_after.set(row['density_after'] or '')

        except Exception as e:
            err.Error.log(f'Ошибка при заполнении формы редактирования: {e}')
            mb.showerror('Ошибка заполнения', str(e))
            self.destroy()

    def on_edit(self):
        my_data = self.my_data_ent.get().strip()
        gos_nomer = self.entry_gos_nomer.get().strip().upper()
        brand_auto = self.brand_auto_entry.get().strip().upper()
        brand_battery = self.brand_battery_combobox.get()
        kol_battery = self.kol_battery_spinbox.get()
        description = self.description.get().strip()
        density_up_to = self.density_up_to_combobox.get()
        density_after = self.density_after.get()

        # Можно продублировать проверки из on_add, если нужно
        # (дата, гос. номер, марка авто и т.п.)

        # Вызываем метод обновления из Main
        self.parent_main.update_record(
            my_data,
            gos_nomer,
            brand_auto,
            brand_battery,
            kol_battery,
            description,
            density_up_to,
            density_after
        )
        self.destroy()

class Search(tk.Toplevel):
    """
    Окно поиска по номеру автомобиля
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.title('Поиск по гос номеру')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.on_cancel)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск', command=self.search_auto)
        btn_search.place(x=105, y=50)

    def on_cancel(self):
        self.parent.set_status_label("Поиск отменён пользователем.", color="#8b4513")
        self.destroy()

    def search_auto(self):
        query = self.entry_search.get().strip()
        if not query:
            self.parent.set_status_label("Введите хотя бы цифры номера автомобиля.", color="#8b4513")
            return
        self.parent.search_records(query)
        self.destroy()

class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Помощь. О программе.")
        self.geometry("850x650")
        self.resizable(False, False)

        lbl_title = tk.Label(self, text='Руководство пользователя', font=('Segoe UI', 14, 'bold'), anchor=tk.W)
        lbl_title.pack(fill=tk.X, padx=15, pady=(15, 5))

        help_text_parts = [
            "Программа учёта аккумуляторных батарей.\n",
            "НАЗНАЧЕНИЕ:\n",
            f"{settings.MDASH} контроль эксплуатации АКБ\n",
            f"{settings.MDASH} контроль обслуживания АКБ\n",
            f"{settings.MDASH} контроль плотности (до и после)\n",
            f"{settings.MDASH} поиск по гос. номеру автомобиля\n",
            f"{settings.MDASH} резервное копирование и восстановление\n",
            f'{settings.MDASH} при создании резервной копии, можно задать своё имя (лучше на латинице)\n',
            f'{settings.MDASH} возможность выбора восстанавливаемой копии БД\n',
            "КАК РАБОТАТЬ:\n",
            f'\t1. Кнопка {settings.LAQIO}Добавить{settings.RAQIO} {settings.MDASH} открыть форму ввода новой записи\n',
            f'\t2. Кнопка {settings.LAQIO}Редакция{settings.RAQIO} {settings.MDASH} отредактировать ранее добавленную запись, предваритель выделив её\n',
            f'\t3. Кнопка {settings.LAQIO}Удалить{settings.RAQIO} {settings.MDASH} безвозвратное удаление записи (ОБЯЗАТЕЛЬНОЕ ПОДТВЕРЖДЕНИЕ!)\n',
            f'\t4. Кнопка {settings.LAQIO}Поиск{settings.RAQIO} {settings.MDASH} поиск по гос. номеру (достаточно цифр номера)\n',
            f'\t5. Кнопка {settings.LAQIO}Backup{settings.RAQIO} {settings.MDASH} резервное копировани БД\n',
            f'\t6. Кнопка {settings.LAQIO}Restore{settings.RAQIO} {settings.MDASH} восстановление ранее сделанного резервного копирования БД\n',
            f'\t{settings.BULLET} Красный фон {settings.MDASH} низкая плотность ({settings.LES_THAN}1.23) или {settings.LAQIO}ВОДА{settings.RAQIO}\n',
            f'\t{settings.BULLET} Голубой фон {settings.MDASH} новый АКБ (по дате {settings.LES_THAN}10 дней или по плотности\n',
            f'\t{settings.BULLET} Белый фон {settings.MDASH} нормальный статус\n\n',
            f'\t{settings.BULLET} ВНИМАНИЕ: ОПЕРАЦИЯ УДАЛЕНИЯ НЕОБРАТИМА!!!\n'
            'ВАЖНО:\n',
            f'\t{settings.MDASH} Дата вводится строго в формате: ДД-ММ-ГГГГ.\n',
            f'\t{settings.MDASH} Гос. номер: только разрешённые буквы (согласно ГОСТу)\n',
            f'\t{settings.MDASH} При добавлении записи в БД, РЕКОМЕНДУЕТСЯ сделать резервную копию\n',
            "Версия программы: 1.0\n",
            "Разработчик: Гринченко Сергей\n"
        ]
        help_text = "".join(help_text_parts)
        # Текст с прокруткой
        text_frame = tk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 12),
            bg="#f5f5f5",
            relief=tk.FLAT
        )

        self.text_widget.insert(tk.END, help_text)
        self.text_widget.config(state=tk.DISABLED)  # Только чтение

        scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Панель кнопок внизу
        btn_frame = tk.Frame(self, pady=10)
        btn_frame.pack()

        btn_close = ttk.Button(btn_frame, text="Закрыть", command=self.destroy)
        btn_close.pack(side=tk.LEFT, padx=(0, 10))

        # Сюда потом подключим PDF
        btn_pdf = ttk.Button(
            btn_frame,
            text="Открыть PDF-инструкцию",
            command=self.open_pdf_manual
        )
        btn_pdf.pack(side=tk.LEFT)

        # Модальность и позиционирование
        self.transient(parent)
        self.grab_set()
        self.center_window()

    def center_window(self):
        """Центрирует окно относительно родителя"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.winfo_x() + (self.winfo_width() - width) // 2
        y = self.winfo_y() + (self.winfo_height() - height) // 2

        parent_x = self.master.winfo_rootx()
        parent_y = self.master.winfo_rooty()
        parent_w = self.master.winfo_width()
        parent_h = self.master.winfo_height()

        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def open_pdf_manual(self):
        """Заглушка: позже здесь будет открытие PDF-файла"""
        pdf_path = "manual.pdf"  # имя файла инструкции
        if os.path.exists(pdf_path):
            # Кроссплатформенное открытие PDF
            if sys.platform == "win32":
                os.startfile(pdf_path)
            else:
                import subprocess
                subprocess.run(["xdg-open", pdf_path], check=False)
        else:
            mb.showwarning(
                "Инструкция не найдена",
                f"Файл '{pdf_path}' не найден.\n"
                "Положите PDF-файл инструкции рядом с программой."
            )
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root, db)
    app.pack()
    root.title("ServiceBattery. V 1.0 Сведения об обслуживании и обороте аккумуляторных батарей")
    root.geometry("1240x470+20+100")
    root.resizable(False, False)
    root.iconphoto(True, PhotoImage(file="akb.png"))
    root.mainloop()
