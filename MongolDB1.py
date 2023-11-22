import json
from pprint import pprint

from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
import data_for_mongodb as exist_data

# ssh -L 6379:192.168.112.103:6379 -N -T rkuzmin@kappa.cs.petrsu.ru
team = {'name': 'Kyshtym', 'city': 'Kyshtym_team', 'coach_name': 'Leva D.S.',
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

data_game = {'date': '01.01.2023', 'score': '0:2', 'rules violations': {
    'card': 'yellow',
    'name': 'Andreev S. M.',
    'minute': '12',
    'reason': 'Deliberate hand play'
}, 'goals': [{
    'name': 'Semenov V.M.',
    'position': '4',
    'minute': '19',
    'pass': 'accurate pass'
}, {
    'name': 'Tervoch K.K.',
    'position': '3',
    'minute': '5',
    'pass': 'short pass'
}],
             'penalties': {
                 'name': 'Sergeev I.I.',
                 'position': '6',
                 'minute': '6',
                 'pass': 'wall pass'
             }, 'shots_number_goals': [{'name': 'Semenov V.M.',
                                        'position': '4',
                                        'minute': '19',
                                        'pass': 'accurate pass'
                                        }, {
                                           'name': 'Tyrin S.S.',
                                           'position': '10',
                                           'minute': '16',
                                           'pass': 'chip pass'
                                       },
                                       {
                                           'name': 'Tervoch K.K.',
                                           'position': '3',
                                           'minute': '5',
                                           'pass': 'short pass'
                                       }]}


class MongoDataB:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['22303']
        self.collection = self.db['rkuzmin-sport']


class MongoWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Монго №1')
        self.root.geometry('500x500')
        self.mongo_server = MongoDataB()
        self.key_entry = tk.Entry(self.root)
        self.properties_entry = tk.Entry(self.root)
        self.button_window()
        self.entry_window()
        self.label_window()
        self.root.mainloop()

    def entry_window(self):
        self.key_entry.grid(row=2, column=1, padx=10)
        self.properties_entry.grid(row=2, column=2, padx=10)

    def button_window(self):
        button_add = tk.Button(self.root, text='Добавить ключ-значение!', command=self.add,
                               font=('Arial', 12), width=20, anchor='center')
        button_add.grid(row=1, column=3, sticky='w', padx=20)
        button_save = tk.Button(self.root, text='Сохранить документ!', command=self.save,
                                font=('Arial', 12), width=20, anchor='center')
        button_save.grid(row=2, column=3, sticky='w', padx=20)
        button_show = tk.Button(self.root, text='Показать документы!', command=self.show,
                                font=('Arial', 12), width=20, anchor='center')
        button_show.grid(row=3, column=3, sticky='w', padx=20)

    def add(self):
        pass

    def save(self):
        pass

    def show(self):
        pass

    def label_window(self):
        key_label = tk.Label(self.root, text='Ключи', font=('Arial', 12))
        key_label.grid(row=1, column=1, padx=10)
        properties_label = tk.Label(self.root, text='Свойства', font=('Arial', 12))
        properties_label.grid(row=1, column=2, padx=10)


if __name__ == "__main__":
    main = MongoWindow()
