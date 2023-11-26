import json
from pprint import pprint

from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk

# ssh -L 27017:192.168.112.103:27017 -N -T rkuzmin@kappa.cs.petrsu.ru
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

template_game = {'category': '',
                 'date': '',
                 'score': '',
                 'rules_violations': [
                     {'card': '', 'name': '', 'minute': '', 'reason': ''}],
                 'goals': [{'name': '', 'position': '', 'minute': '', 'pass': ''}],
                 'penalties': [{'name': '', 'position': '', 'minute': '', 'pass': ''}],
                 'shots_number_goals': [{'name': '', 'position': '', 'minute': '', 'pass': ''}]
                 }
template_team = {'category': '', 'name': '', 'city': '', 'coach_name': '',
             'players': [{'name': '', 'position': ''}],
             'reserve_players': []}


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


class MongoWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Монго №1')
        self.root.geometry('1000x1000')
        self.mongo_server = MongoDataB()
        self.key_entry = tk.Entry(self.root)
        self.properties_entry = tk.Entry(self.root)
        self.combo = ttk.Combobox(self.root, values=['Teams', 'Games'], state="readonly")
        self.combo.grid(row=2, column=3)
        self.combo.bind("<<ComboboxSelected>>", lambda event: self.on_combobox_selected(event))
        self.button_window()
        self.date_entry = None
        self.entry_window()
        self.label_window()
        self.show_window()
        self.root.mainloop()

    def entry_window(self):
        self.key_entry.grid(row=2, column=1, padx=10)
        self.properties_entry.grid(row=2, column=2, padx=10)

    def label_window(self):
        key_label = tk.Label(self.root, text='Ключи', font=('Arial', 12))
        key_label.grid(row=1, column=1, padx=10)
        properties_label = tk.Label(self.root, text='Свойства', font=('Arial', 12))
        properties_label.grid(row=1, column=2, padx=10)
        combo_label = tk.Label(self.root, text="Выберите опцию", font=('Arial', 12))
        combo_label.grid(row=1, column=3)

    def button_window(self):
        button_add = tk.Button(self.root, text='Добавить ключ-значение!', command=self.add_key_value,
                               font=('Arial', 12), width=20, anchor='center')
        button_add.grid(row=1, column=4, sticky='e', padx=20, pady=10)
        button_save = tk.Button(self.root, text='Сохранить документ!', command=self.new_document,
                                font=('Arial', 12), width=20, anchor='center')
        button_save.grid(row=2, column=4, sticky='e', padx=20, pady=10)
        button_show = tk.Button(self.root, text='Показать документы!', command=self.show,
                                font=('Arial', 12), width=20, anchor='center')
        button_show.grid(row=3, column=4, sticky='e', padx=20, pady=10)

    def show_window(self):
        global documents_text
        documents_text = tk.Text(self.root)
        documents_text.place(x=20, y=180, width=860, height=350)
        documents_text.configure(state=tk.DISABLED)

    def on_combobox_selected(self, event):
        selected_value = self.combo.get()
        if selected_value == 'Games':
            self.show_date_entry()
        else:
            self.hide_date_entry()

    def show_date_entry(self):
        if self.date_entry is None:
            self.date_label = tk.Label(text="Дата")
            self.date_label.grid(row=3, column=1)
            self.date_entry = tk.Entry(self.root)
            self.date_entry.grid(row=4, column=1, padx=10)

    def hide_date_entry(self):
        if self.date_entry:
            self.date_entry.destroy()
            self.date_label.destroy()
            self.date_entry = None

    def add_key_value(self):
        key = self.key_entry.get()
        properties = self.properties_entry.get()
        combo_filter = self.combo.get()

        if combo_filter == 'Teams':
            field = key.split('.')
            new_value = properties.split('.')
            for i in self.mongo_server.collection.find({"category": "team"}):
                if i['name'] == f'{new_value[0]}':
                    good_team = i
                else:
                    continue

                # good_game[field[0]] = new_value
                if field[1] == 'players':
                    print(1)
                    new_dictiononary = {}
                    for i, j in zip(field[2:], new_value[1:]):
                        new_dictiononary[i] = j
                    good_team[field[1]].append(new_dictiononary)
                    self.mongo_server.collection.update_one({"category": "team", "name": new_value[0]},
                                                            {"$set": good_team}, upsert=True)
                elif field[1] == 'reserve_players':
                    good_team[field[1]].append(new_value[1])
                    self.mongo_server.collection.update_one({"category": "team", "name": new_value[0]},
                                                            {"$set": good_team}, upsert=True)
                else:
                    good_team[field[1]] = new_value[1]
                    self.mongo_server.collection.update_one({"category": "team", "name": new_value[0]},
                                                            {"$set": good_team}, upsert=True)

        elif combo_filter == 'Games':
            date = self.date_entry.get()
            field = key.split('.')
            new_value = properties.split('.')
            for i in self.mongo_server.collection.find({"category": "game"}):
                if i['date'] == f'{date}':
                    good_game = i
                else:
                    continue

                # good_game[field[0]] = new_value
            if field[0] in ['rules_violations', 'goals', 'penalties', 'shots_number_goals']:
                new_dictiononary = {}
                for i, j in zip(field[1:], new_value):
                    new_dictiononary[i] = j
                good_game[field[0]].append(new_dictiononary)
                self.mongo_server.collection.update_one({"category": "game", "date": date},
                                                        {"$set": good_game}, upsert=True)
            else:
                good_game[field[0]] = new_value
                self.mongo_server.collection.update_one({"category": "game", "date": date},
                                                        {"$set": good_game}, upsert=True)
        self.show()

    def new_document(self):
        key = self.key_entry.get()
        properties = self.properties_entry.get()
        combo_filter = self.combo.get()
        template_game['category'] = combo_filter.lower()
        if combo_filter == 'Games':
            date = self.date_entry.get()
            field = key.split('.')
            new_value = properties.split('.')
                # good_game[field[0]] = new_value
            if field[0] in ['rules_violations', 'goals', 'penalties', 'shots_number_goals']:
                for i, j in zip(field[1:], new_value):
                    template_game[i] = j
                template_game['date'] = date
                good_game = template_game
                self.mongo_server.collection.insert_one(good_game)
            else:
                template_game['date'] = date
                template_game[field[0]] = new_value
                good_game = template_game
                self.mongo_server.collection.insert_one(good_game)
        if combo_filter == 'Teams':
            field = key.split('.')
            new_value = properties.split('.')
            good_team = template_team
            good_team['category'] = 'team'
            good_team['name'] = new_value[0]
            if field[1] == 'players':
                new_dictionary = {}
                for i, j in zip(field[2:], new_value[1:]):
                    new_dictionary[i] = j
                good_team[field[1]].append(new_dictionary)
                self.mongo_server.collection.update_one({"category": "team", "name": new_value[0]},
                                                        {"$set": good_team}, upsert=True)
            elif field[1] == 'reserve_players':
                good_team[field[1]].append(new_value[1])
                self.mongo_server.collection.update_one({"category": "team", "name": new_value[0]},
                                                        {"$set": good_team}, upsert=True)
            else:
                good_team[field[1]] = new_value[1]
                self.mongo_server.collection.update_one({"category": "team", "name": new_value[0]},
                                                        {"$set": good_team}, upsert=True)


    def show(self):
        current_document = ""
        for i in self.mongo_server.collection.find():
            current_document += f'{i}\n\n'
        documents_text.configure(state=tk.NORMAL)
        documents_text.delete('1.0', tk.END)
        documents_text.insert(1.0, current_document)
        documents_text.configure(state=tk.DISABLED)


if __name__ == "__main__":
    main = MongoWindow()
