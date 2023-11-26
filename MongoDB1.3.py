from pymongo import MongoClient
from tkinter import *
from tkinter import ttk
import json

data_team = {'category': 'team', 'name': 'Spart', 'city': 'Petrozavodsk', 'coach_name': 'Leva D.S.',
             'players': [{'name': 'Petrov V.V.', 'position': '1'},
                         {'name': 'Ivanov V.V.', 'position': '2'},
                         {'name': 'Tervoch K.K.', 'position': '3'},
                         {'name': 'Semenov V.M.', 'position': '4'},
                         {'name': 'Laitenen H.D.', 'position': '5'},
                         {'name': 'Sergeev I.I.', 'position': '6'},
                         {'name': 'Zubkov I.L.', 'position': '7'},
                         {'name': 'Lekander O.N.', 'position': '8'},
                         {'name': 'Gromov V.A.', 'position': '9'},
                         {'name': 'Tyrin S.S.', 'position': '10'},
                         {'name': 'Jorjev K.A.', 'position': '11'}],
             'reserve_players': ['Chetkov V.V.', 'Kuznetsov V.V.', 'Peshkin V.V.', 'Venchik V.V.', 'Semchik V.V.']}

data_game = {'category': 'game',
             'date': '01.01.2023',
             'score': '0:2',
             'rules_violations': [
                 {'card': 'yellow', 'name': 'Andreev S. M.', 'minute': '12', 'reason': 'Deliberate hand play'}],
             'goals': [{'name': 'Semenov V.M.', 'position': '4', 'minute': '19', 'pass': 'accurate pass'},
                       {'name': 'Tervoch K.K.', 'position': '3', 'minute': '5', 'pass': 'short pass'}],
             'penalties': [{'name': 'Sergeev I.I.', 'position': '6', 'minute': '6', 'pass': 'wall pass'}],
             'shots_number_goals': [{'name': 'Semenov V.M.', 'position': '4', 'minute': '19', 'pass': 'accurate pass'},
                                    {'name': 'Tyrin S.S.', 'position': '10', 'minute': '16', 'pass': 'chip pass'},
                                    {'name': 'Tervoch K.K.', 'position': '3', 'minute': '5', 'pass': 'short pass'}]
             }


# Подключение
class MongoDataB:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['22303']
        self.collection = self.db['rkuzmin-sport']
        self.fill_bd()

    def fill_bd(self):
        self.collection.delete_many({})
        self.collection.insert_one(data_game)
        self.collection.insert_one(data_team)


# Создание коллекции

"""
Оконное приложение для поиска и отображения результатов
"""


class SearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Football Data Search App")

        self.key_label = Label(master, text="Ключ:")
        self.key_label.grid(row=0, column=0)

        self.comparison_label = Label(master, text="Сравнение:")
        self.comparison_label.grid(row=1, column=0)

        self.value_label = Label(master, text="Значение:")
        self.value_label.grid(row=2, column=0)

        self.key_entry = Entry(master)
        self.key_entry.grid(row=0, column=1)

        self.comparison_var = StringVar()
        self.comparison_entry = ttk.Combobox(master, textvariable=self.comparison_var,
                                             values=['>', '>=', '=', '<=', '<', '!='])
        self.comparison_entry.grid(row=1, column=1)

        self.value_entry = Entry(master)
        self.value_entry.grid(row=2, column=1)

        self.collection_var = StringVar()
        self.collection_entry = ttk.Combobox(master, textvariable=self.collection_var, values=collections_names)
        self.collection_entry.grid(row=3, column=0, columnspan=1)
        self.collection_entry.bind("<<ComboboxSelected>>", lambda event: self.choose_current_collection())

        self.search_button = Button(master, text="Выполнить запрос", command=self.perform_search)
        self.search_button.grid(row=4, column=0, columnspan=2)

        self.current_collection_label = Label(master, text="Текущая коллекция:")
        self.current_collection_label.grid(row=5, column=0)

        self.current_collection_label2 = Label(master, text="Футбольные команды")
        self.current_collection_label2.grid(row=5, column=1)

        self.documents_text = Text(master, width=90, height=20, state="disabled")
        self.documents_text.grid(row=7, column=0, columnspan=2, padx=40, pady=10)

        self.current_collection = football_collection

    def choose_current_collection(self):
        cur_collection = self.collection_var.get()
        if (cur_collection == collections_names[1]):
            self.current_collection = game_collection
            self.current_collection_label2.config(text=collections_names[1])
        else:
            self.current_collection = football_collection
            self.current_collection_label2.config(text=collections_names[0])

        print(self.current_collection)

    def show_documents(self, query):
        self.documents_text.config(state=NORMAL)  # Включаем режим редактирования
        self.documents_text.delete(1.0, END)  # Очищаем Text перед выводом новых данных

        for document in self.current_collection.find(query):
            self.documents_text.insert(END, json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4,
                                                       ensure_ascii=False) + '\n_______________________________________\n\n')

        self.documents_text.config(state="disabled")

    def perform_search(self):
        key = self.key_entry.get()
        comparison = self.comparison_var.get()
        value = self.value_entry.get()

        # Преобразование значения в соответствующий тип (int, float, str)
        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass  # Если не удалось преобразовать в число, оставляем как строку

        # Определение оператора сравнения
        if comparison == '>':
            query = {key: {'$gt': value}}
        elif comparison == '>=':
            query = {key: {'$gte': value}}
        elif comparison == '=':
            query = {key: {'$eq': value}}
        elif comparison == '<=':
            query = {key: {'$lte': value}}
        elif comparison == '<':
            query = {key: {'$lt': value}}
        elif comparison == '!=':
            query = {key: {'$ne': value}}
        else:
            # Обработка некорректного сравнения
            print("Некорректное сравнение")

        # Выполнение запроса к коллекции
        self.show_documents(query)


# Запуск оконных приложений
root2 = Tk()
root2.geometry('800x600')
search_app = SearchApp(root2)

root2.mainloop()
