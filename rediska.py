import ast
import tkinter as tk
from tkinter import ttk
from redis import Redis


class RedisData:
    def __init__(self):
        self.user_name: str = ""
        self.font_data = {'font_name': '',
                          'font_color': '',
                          'font_size': '',
                          'font_outline': ''}
        self.id = 0
        self.font_text: str = ""


class RedisServer:
    def __init__(self):
        self.connection = Redis(host='192.168.112.103', password='student')

    def post(self, data, u_id):
        try:
            self.connection.set(f'22303-Kuzmin-{u_id}', f'{data.__dict__}', ex=120)
            # self.connection.set(f'22303-Kuzmin-{u_id}-text', f'{text}', ex=30)
        except ConnectionError:
            print("Ошибка подключения")
            return 400

    def get(self, u_id):
        try:
            return self.connection.get(f'22303-Kuzmin-{u_id}').decode('utf-8')
        except ConnectionError:
            print("Ошибка подключения")
            return 400


class RedisWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Редиске №1')
        self.root.geometry('500x500')
        self.redis_server = RedisServer()
        self.text_font_size = tk.Entry(self.root)
        self.text_font_name = tk.Entry(self.root)
        self.text_font_color = tk.Entry(self.root)
        self.text_font_outline = tk.Entry(self.root)
        self.text_font_text = tk.Entry(self.root)
        self.user_combo = ttk.Combobox(self.root, values=self.user, state="readonly")
        try:
            self.user_combo.bind("<<ComboboxSelected>>", self.get_server_data_from_redis)
        except:
            self.user_combo.bind("<<ComboboxSelected>>", self.clear_text_fields)
        self.result_label = tk.Label(self.root, text="")
        self.label_window()
        self.text_window()
        self.listbox_window()
        self.root.mainloop()

    @property
    def user(self):
        return ['Иван Сергеевич Евстюнин', 'Вадим Анатольевич Громов', 'Сергей Степанович Прокопьев']

    def label_window(self):
        label_users_name = tk.Label(self.root, text='Настройки шрифта',
                                    font=('Arial', 14, 'bold'))
        label_users_name.grid(row=0, column=1, columnspan=2)
        label_font_name = tk.Label(self.root, text='Название шрифта',
                                   font=('Arial', 12))
        label_font_name.grid(row=1, column=0, sticky='w')
        label_font_color = tk.Label(self.root, text='Цвет шрифта', font=('Arial', 12))
        label_font_color.grid(row=2, column=0, sticky='w')
        label_font_outline = tk.Label(self.root, text='Начертание шрифта', font=('Arial', 12))
        label_font_outline.grid(row=3, column=0, sticky='w')
        label_font_size = tk.Label(self.root, text='Размер шрифта', font=('Arial', 12))
        label_font_size.grid(row=4, column=0, sticky='w')

        label_font_text = tk.Label(self.root, text='Текст', font=('Arial', 12))
        label_font_text.grid(row=7, column=0, sticky='w')

    def text_window(self):
        self.text_font_name.grid(row=1, column=2)
        self.text_font_color.grid(row=2, column=2)
        self.text_font_outline.grid(row=3, column=2)
        self.text_font_size.grid(row=4, column=2)
        self.text_font_text.grid(row=7, column=2)
        self.result_label.grid(row=13, column=3, sticky="w")

    def listbox_window(self):
        self.user_combo.grid(row=10, column=1, sticky='w')
        button_save = tk.Button(self.root, text='save!', command=self.save_data_from_entry,
                                font=('Arial', 12), width=10, anchor='center')
        button_save.grid(row=11, column=1, sticky='w')
        button_do_it = tk.Button(self.root, text='Do it', command=self.get_server_data_from_redis,
                                 font=('Arial', 12), width=10, anchor='center')
        button_do_it.grid(row=12, column=1, sticky='w')

    def clear_text_fields(self, event):
        self.text_font_name.delete(0, 'end')
        self.text_font_color.delete(0, 'end')
        self.text_font_outline.delete(0, 'end')
        self.text_font_size.delete(0, 'end')
        # self.text_font_text.delete(0, 'end')

    def save_data_from_entry(self):
        user_settings = RedisData()
        user_settings.user_name = self.user_combo.get()
        user_settings.font_data['font_name'] = self.text_font_name.get()
        user_settings.font_data['font_color'] = self.text_font_color.get()
        user_settings.font_data['font_size'] = self.text_font_size.get()
        user_settings.font_data['font_outline'] = self.text_font_outline.get()
        user_id = hash(user_settings.user_name)
        try:
            user_settings.id = self.redis_server.post(user_settings, user_id)
        except Exception as e:
            # Обработка исключения
            print(f"An exception occurred: {e}")
            return 400

    def get_server_data_from_redis(self, event=None):
        user_settings = RedisData()
        user_settings.user_name = self.user_combo.get()
        user_id = hash(user_settings.user_name)
        try:
            data_from_dict = self.redis_server.get(user_id)
            user_text = self.text_font_text.get()
            self.change_font(data_from_dict, user_text)
        except Exception as e:
            # Обработка исключения
            print(f"An exception occurred: {e}")
            return 400

    def change_font(self, settings, user_text):
        font_settings = ast.literal_eval(settings)['font_data']
        font_size = int(font_settings['font_size'])
        font_color = font_settings['font_color']
        font_outline = font_settings['font_outline']
        font_name = font_settings['font_name']

        self.result_label.config(text=user_text, fg=font_color, font=(font_name, font_size, font_outline))


if __name__ == "__main__":
    main = RedisWindow()
