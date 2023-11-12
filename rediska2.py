import tkinter as tk
from tkinter import ttk
from redis import Redis


class RefereePointsSportsman:
    def __init__(self):
        self.name: str
        self.sportsman_name: str
        self.sportsman_points: int


class Names:
    sportsman_names = ['Иван Сергеевич Евстюнин', 'Вадим Анатольевич Громов', 'Сергей Степанович Прокопьев']
    referee_names = ["Василий Сюткин", "Антон Горбачев", "Константин Григорьев"]


class RedisServer:
    def __init__(self):
        self.connection = Redis(host='192.168.112.103', password='student')

    def post(self, data):
        referee = data.__dict__['name']
        sportsman = data.__dict__['sportsman_name']
        points = data.__dict__['sportsman_points']
        key = f'22303-Kuzmin-{referee}-{sportsman}'
        try:
            current_points = self.connection.get(key)
            if current_points is not None:
                current_points = int(current_points.decode('utf-8'))
                points = current_points + int(points)
            self.connection.set(key, str(points), ex=20)
        except ConnectionError:
            print("Ошибка подключения")
            return 400

    def get(self, name):
        result = 0
        for referee in Names.referee_names:
            try:
                points = self.connection.get(f'22303-Kuzmin-{referee}-{name}').decode('utf-8')
                if points:
                    result += int(points)
            except:
                continue
        return result


class RedisWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Редиске №2')
        self.root.geometry('500x600')
        self.redis_server = RedisServer()
        self.label_window()
        self.data_from_combo = self.combo_window()
        self.points = self.text_window()
        self.data_from_combo[0].bind("<<ComboboxSelected>>", lambda event: self.clear_entry(self.points))
        self.data_from_combo[1].bind("<<ComboboxSelected>>", lambda event: self.clear_entry(self.points))
        self.tree = self.tree_window()
        self.button_confirm()
        self.root.mainloop()

    def label_window(self):
        referee_label = tk.Label(self.root, text='Судья', font=('Arial', 12))
        referee_label.grid(row=1, column=0, sticky='w', padx=10)
        points_label = tk.Label(self.root, text='Баллы', font=('Arial', 12))
        points_label.grid(row=1, column=1, sticky='w', padx=10)
        sportsman_label = tk.Label(self.root, text='Спортсмен', font=('Arial', 12))
        sportsman_label.grid(row=1, column=2, sticky='w', padx=10)

    def clear_entry(self, entry):
        entry.delete(0, 'end')

    def combo_window(self):
        referee_combo = ttk.Combobox(self.root, values=Names.referee_names, state="readonly")
        referee_combo.grid(row=2, column=0, sticky='w', padx=10)
        sportsman_combo = ttk.Combobox(self.root, values=Names.sportsman_names, state="readonly")
        sportsman_combo.grid(row=2, column=2, sticky='w', padx=10)
        return referee_combo, sportsman_combo

    def text_window(self):
        points_text = tk.Entry(self.root)
        points_text.grid(row=2, column=1, sticky='w', padx=20)
        return points_text

    def button_confirm(self):
        button_save = tk.Button(self.root, text='Do it', command=self.save_data_from_entry,
                                font=('Arial', 12), width=10)
        button_save.grid(row=3, column=1, sticky='', pady=10)

    def tree_window(self):
        columns = ("Спортсмен", "Очки")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        tree.grid(row=4, columnspan=4, pady=10)
        tree.heading("Спортсмен", text="Спортсмен")
        tree.heading("Очки", text="Очки")
        return tree

    def save_data_from_entry(self):
        referee = RefereePointsSportsman()
        referee.name = self.data_from_combo[0].get()
        referee.sportsman_name = self.data_from_combo[1].get()
        referee.sportsman_points = self.points.get()
        try:
            self.redis_server.post(referee)
            self.get_server_data_from_redis()
        except Exception as e:
            # Обработка исключения
            print(f"An exception occurred: {e}")
            return 400

    def get_server_data_from_redis(self):
        sportsman_points = {key: 0 for key in Names.sportsman_names}
        try:
            for sportsman in Names.sportsman_names:
                sportsman_points[f'{sportsman}'] = self.redis_server.get(sportsman)
            for item in self.tree.get_children():
                self.tree.delete(item)
            sorted_sportsman_points = sorted(sportsman_points.items(), key=lambda x: int(x[1]), reverse=True)
            for name, points in sorted_sportsman_points:
                self.tree.insert("", "end", values=(name, points))

        except Exception as e:
            # Обработка исключения
            print(f"An exception occurred: {e}")
            return 400


if __name__ == "__main__":
    main = RedisWindow()
