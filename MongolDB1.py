from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
import data_for_mongodb as exist_data


# ssh -L 6379:192.168.112.103:6379 -N -T rkuzmin@kappa.cs.petrsu.ru

class MongoDataB:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['22303']
        self.collection = self.db['rkuzmin-sport']
        self.fill_db()

    def fill_db(self):
        data = exist_data.DataMongo()
        self.collection.delete_many({})
        self.collection.insert_one(data.game)
        self.collection.insert_one(data.team)
        for i in self.collection.find():
            print(i)


class MongoWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Монго №1')
        self.root.geometry('500x500')
        # self.mongo_server = MongoDataB()
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
