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
        self.connection = Redis(host='127.0.0.1', password='student')

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
        except AttributeError:
            return None


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
        self.fill_input_fields_with_default_settings()
        self.user_combo = ttk.Combobox(self.root, values=self.user, state="readonly")
        try:
            self.user_combo.bind("<<ComboboxSelected>>", self.get_server_data_from_redis)
        except:
            self.user_combo.bind("<<ComboboxSelected>>", self.clear_text_fields)
        self.text_font_text.bind("<KeyRelease>",
                                 self.get_server_data_from_redis)  # Добавляем обработчик события KeyRelease
        self.result_label = tk.Label(self.root, text="")
        self.label_window()
        self.text_window()
        self.listbox_window()
        self.root.mainloop()

    @property
    def user(self):
        return ['Иван Сергеевич Евстюнин', 'Вадим Анатольевич Громов', 'Сергей Степанович Прокопьев']

    @property
    def normal_settings(self):
        return {
            'user_name': '', 'font_data': {'font_name': 'Arial',
                                           'font_color': 'black',
                                           'font_size': '12',
                                           'font_outline': 'normal'},
            'id': 0, 'font_text': ''
        }

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

    def fill_input_fields_with_data(self, data):
        font_settings = ast.literal_eval(data)['font_data']
        self.text_font_name.delete(0, 'end')
        self.text_font_name.insert(0, font_settings.get('font_name', ''))
        self.text_font_color.delete(0, 'end')
        self.text_font_color.insert(0, font_settings.get('font_color', ''))
        self.text_font_outline.delete(0, 'end')
        self.text_font_outline.insert(0, font_settings.get('font_outline', ''))
        self.text_font_size.delete(0, 'end')
        self.text_font_size.insert(0, font_settings.get('font_size', ''))

    def fill_input_fields_with_default_settings(self):
        default_settings = self.normal_settings['font_data']
        self.text_font_name.delete(0, 'end')
        self.text_font_name.insert(0, default_settings['font_name'])
        self.text_font_color.delete(0, 'end')
        self.text_font_color.insert(0, default_settings['font_color'])
        self.text_font_outline.delete(0, 'end')
        self.text_font_outline.insert(0, default_settings['font_outline'])
        self.text_font_size.delete(0, 'end')
        self.text_font_size.insert(0, default_settings['font_size'])

    def listbox_window(self):
        self.user_combo.grid(row=10, column=1, sticky='w')
        button_save = tk.Button(self.root, text='save!', command=self.save_data_from_entry,
                                font=('Arial', 12), width=10, anchor='center')
        button_save.grid(row=11, column=1, sticky='w')
        # button_do_it = tk.Button(self.root, text='Do it', command=self.get_server_data_from_redis,
        #                          font=('Arial', 12), width=10, anchor='center')
        # button_do_it.grid(row=12, column=1, sticky='w')

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
            self.get_server_data_from_redis()
        except Exception as e:
            # Обработка исключения
            print(f"An exception occurred: {e}")
            return 400

    def get_server_data_from_redis(self, event=None):
        user_settings = RedisData()
        user_settings.user_name = self.user_combo.get()
        user_id = hash(user_settings.user_name)
        user_text = self.text_font_text.get()
        data_from_dict = self.redis_server.get(user_id)
        if data_from_dict is not None:
            self.change_font(user_text, data_from_dict)
            self.fill_input_fields_with_data(data_from_dict)
            return 0
        self.fill_input_fields_with_default_settings()
        self.change_font(user_text)  # Используйте метод по умолчанию

    def change_font(self, user_text, settings=None, ):
        if settings:
            font_settings = ast.literal_eval(settings)['font_data']
            font_size = int(font_settings['font_size']) if font_settings['font_size'] else 12
            font_color = font_settings.get('font_color', 'black')
            font_outline = font_settings.get('font_outline', 'normal')
            font_name = font_settings.get('font_name', 'Arial')
        else:
            # Используйте метод по умолчанию, если настройки отсутствуют
            font_size = int(self.normal_settings['font_data']['font_size'])
            font_color = self.normal_settings['font_data']['font_color']
            font_outline = self.normal_settings['font_data']['font_outline']
            font_name = self.normal_settings['font_data']['font_name']
        self.result_label.config(text=user_text, fg=font_color, font=(font_name, font_size, font_outline))


if __name__ == "__main__":
    main = RedisWindow()
