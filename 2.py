import json

from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
from dateForLab import kitchen, textile, electricity, sport


class MongoDataB:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['22303']
        self.collection = self.db['rkuzmin-shop']
        self.fill_bd()

    def fill_bd(self):
        self.collection.delete_many({})
        self.collection.insert_many(kitchen.date)
        self.collection.insert_many(textile.date)
        self.collection.insert_many(electricity.date)
        self.collection.insert_many(sport.date)


class MongoWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Монго №2')
        self.root.geometry('800x800')
        self.mongo_server = MongoDataB()
        self.current_collection = self.mongo_server.collection
        self.documents_text = tk.Text(self.root, width=90, height=20, state="disabled")
        self.documents_text.grid(row=7, column=0, columnspan=2, padx=40, pady=10)

        self.category_values = ["Спортивные товары", "Домашний текстиль", "Кухонная техника","Электроника"]
        self.selected_option = tk.StringVar(value=self.category_values[0])
        self.collection_entry = ttk.Combobox(self.root, textvariable=self.category_values, values=self.category_values)
        self.collection_entry.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky=tk.W)
        self.collection_entry.bind("<<ComboboxSelected>>", self.combo_with_category_query)
        self.root.mainloop()

    def show_documents(self, query):
        self.documents_text.config(state=tk.NORMAL)
        self.documents_text.delete(1.0, tk.END)
        for document in self.current_collection.find(query):
            self.documents_text.insert(tk.END,
                                       json.dumps({x: document[x] for x in document if x not in "_id"}, indent=4,
                                                  ensure_ascii=False) + '\n\n\n')

        self.documents_text.config(state="disabled")

    def combo_with_category_query(self, event):
        key = "category"
        query = {key: self.collection_entry.get()}
        self.show_documents(query)


if __name__ == '__main__':
    main = MongoWindow()
