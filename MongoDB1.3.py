from tkinter import *
from tkinter import ttk
import json
from pymongo import MongoClient


class MongoDataB:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.database = self.client['22303']
        self.football_collection = self.database["rkuzmin-team"]
        self.game_collection = self.database["rkuzmin-game"]

        # Заполнение базы данных тестовыми данными
        self.fill_db()

    def fill_db(self):
        self.football_collection.delete_many({})
        self.game_collection.delete_many({})
        # Добавление тестовых данных в коллекции
        self.football_collection.insert_one(
            {'category': 'team', 'name': 'Spart', 'city': 'Petrozavodsk', 'coach_name': 'Leva D.S.',
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
             'reserve_players': ['Chetkov V.V.', 'Kuznetsov V.V.', 'Peshkin V.V.', 'Venchik V.V.', 'Semchik V.V.']})
        self.game_collection.insert_one({'category': 'game',
                                         'date': '01.01.2023',
                                         'test': '2',
                                         'score': '0:2',
                                         'rules_violations': [
                                             {'card': 'yellow', 'name': 'Andreev S. M.', 'minute': '12',
                                              'reason': 'Deliberate hand play'}],
                                         'goals': [{'name': 'Semenov V.M.', 'position': '4', 'minute': '19',
                                                    'pass': 'accurate pass'},
                                                   {'name': 'Tervoch K.K.', 'position': '3', 'minute': '5',
                                                    'pass': 'short pass'}],
                                         'penalties': [{'name': 'Sergeev I.I.', 'position': '6', 'minute': '6',
                                                        'pass': 'wall pass'}],
                                         'shots_number_goals': [
                                             {'name': 'Semenov V.M.', 'position': '4', 'minute': '19',
                                              'pass': 'accurate pass'},
                                             {'name': 'Tyrin S.S.', 'position': '10', 'minute': '16',
                                              'pass': 'chip pass'},
                                             {'name': 'Tervoch K.K.', 'position': '3', 'minute': '5',
                                              'pass': 'short pass'}]
                                         })


class SearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Лабораторная по Монго №1.3")

        # Создаем объект MongoDataB
        self.mongo_server = MongoDataB()

        self.key_label = Label(master, text="Ключ:")
        self.key_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.comparison_label = Label(master, text="Сравнение:")
        self.comparison_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.value_label = Label(master, text="Значение:")
        self.value_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.key_entry = Entry(master)
        self.key_entry.grid(row=0, column=1, padx=10, pady=10)

        self.comparison_var = StringVar()
        self.comparison_entry = ttk.Combobox(master, textvariable=self.comparison_var,
                                             values=['>', '>=', '=', '<=', '<', '!='])
        self.comparison_entry.grid(row=1, column=1, padx=10, pady=10)

        self.value_entry = Entry(master)
        self.value_entry.grid(row=2, column=1, padx=10, pady=10)

        self.collection_var = StringVar()
        self.collection_entry = ttk.Combobox(master, textvariable=self.collection_var,
                                             values=['Team', 'Game'])
        self.collection_entry.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky=W)
        self.collection_entry.bind("<<ComboboxSelected>>", lambda event: self.choose_current_collection())

        self.search_button = Button(master, text="Выполнить запрос", command=self.perform_search)
        self.search_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.documents_text = Text(master, width=90, height=20, state="disabled")
        self.documents_text.grid(row=7, column=0, columnspan=2, padx=40, pady=10)

        self.current_collection = self.mongo_server.football_collection

    def choose_current_collection(self):
        cur_collection = self.collection_var.get()
        if cur_collection == 'Game':
            self.current_collection = self.mongo_server.game_collection
        else:
            self.current_collection = self.mongo_server.football_collection

    def show_documents(self, query):
        self.documents_text.config(state=NORMAL)
        self.documents_text.delete(1.0, END)
        for document in self.current_collection.find(query):
            self.documents_text.insert(END, json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4,
                                                       ensure_ascii=False) + '\n\n\n')

        self.documents_text.config(state="disabled")

    def perform_search(self):
        key = self.key_entry.get()
        comparison = self.comparison_var.get()

        value = self.value_entry.get()

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
            print("Некорректное сравнение")

        self.show_documents(query)


# Запуск оконного приложения
root = Tk()
root.geometry('800x600')
root.title("Football Data Search App")
search_app = SearchApp(root)
root.mainloop()
