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
    category_values = ["Спортивные товары", "Домашний текстиль", "Кухонная техника", "Электроника"]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Лабораторная по Монго №2')
        self.root.geometry('800x800')
        self.mongo_server = MongoDataB()
        self.current_collection = self.mongo_server.collection

        self.documents_text = tk.Text(self.root, width=90, height=20, state="disabled")
        self.documents_text.grid(row=7, column=0, columnspan=10, padx=40, pady=10)

        # ---------------------------Категории----------------------------------------
        self.collection_label = tk.Label(self.root, text="Категории")
        self.collection_label.grid(row=0, column=0)
        self.selected_option = tk.StringVar(value=self.category_values[0])
        self.collection_entry = ttk.Combobox(self.root, textvariable=self.selected_option, values=self.category_values)
        self.collection_entry.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky=tk.W)
        self.button_names = tk.Button(self.root, text="Названия", command=self.show_product_names)
        self.button_names.grid(row=0, column=2, padx=5, pady=5)
        self.button_characteristic = tk.Button(self.root, text="Характеристики",
                                               command=self.show_product_characteristic)
        self.button_characteristic.grid(row=0, column=3, padx=5, pady=5)
        # ---------------------------Товары----------------------------------------
        self.product_label = tk.Label(self.root, text="Товары")
        self.product_label.grid(row=1, column=0)
        self.product_entry = ttk.Combobox(self.root, values=[])
        self.product_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=tk.W)
        self.delivery_firm_entry = tk.Entry(self.root)
        self.delivery_firm_entry.grid(row=1, column=2, padx=5, pady=5)
        self.show_products_by_category()
        self.button_product = tk.Button(self.root, text="Покупатели", command=self.show_customers_with_delivery_firm)
        self.button_product.grid(row=1, column=3, padx=5, pady=5)
        self.collection_entry.bind("<<ComboboxSelected>>", self.show_products_by_category)
        # ---------------------------Покупатели----------------------------------------
        customers = self.fill_customer_names_combobox()
        self.customers_entry = ttk.Combobox(self.root, values=customers)
        self.customers_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky=tk.W)
        self.customers_label = tk.Label(self.root, text="Покупатели")
        self.customers_label.grid(row=2, column=0)
        self.button_purchase = tk.Button(self.root, text="Покупки", command=self.show_purchase_info_by_customer)
        self.button_purchase.grid(row=2, column=2, padx=5, pady=5)

        # ---------------------------Цвет----------------------------------------
        self.color_label = tk.Label(self.root, text="Цвет")
        self.color_label.grid(row=5, column=0)
        self.color_entry = tk.Entry(self.root)
        self.color_entry.grid(row=5, column=1, padx=5, pady=5)
        self.color_button = tk.Button(self.root, text="Получить", command=self.get_products_by_color)
        self.color_button.grid(row=5, column=2)

        # ---------------------------Сумма продаж----------------------------------------
        self.sales_button = tk.Button(self.root, text="Продано", command=self.calculate_total_sales)
        self.sales_button.grid(row=6, column=0)

        # ---------------------------Товар по категориям----------------------------------------
        self.products_button = tk.Button(self.root, text="Товаров в сумме", command=self.count_products_by_category)
        self.products_button.grid(row=6, column=1)

        self.root.mainloop()

    def show_product_names(self):
        category = self.selected_option.get()
        product_names = [product['name'] for product in self.current_collection.find({"category": category})]

        # Очищаем виджет Text и выводим названия товаров
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        for name in product_names:
            self.documents_text.insert("end", f"{name}\n")
        self.documents_text.config(state="disabled")

    def show_product_characteristic(self):
        category = self.selected_option.get()
        characteristics_text = ""
        for product in self.current_collection.find({"category": category}):
            characteristics_text += f"Product: {product['name']}\n"
            characteristics = product.get("characteristics", {})
            for key, value in characteristics.items():
                characteristics_text += f"{key}: {value}\n"
            characteristics_text += "\n"  # Добавляем пустую строку для разделения товаров

        # Очищаем виджет Text и выводим характеристики
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        self.documents_text.insert("end", characteristics_text)
        self.documents_text.config(state="disabled")

    @staticmethod
    def fill_customer_names_combobox():
        customer_names = set()

        # Проходимся по всем коллекциям и собираем имена покупателей
        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                customers = product.get("customers", [])
                for customer in customers:
                    customer_name = customer.get("name", "")
                    if customer_name:
                        customer_names.add(customer_name)

        # Заполняем Combobox значениями
        return list(customer_names)

    def show_purchase_info_by_customer(self):
        customer_name = self.customers_entry.get()
        purchase_info = ""
        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                customers = product.get("customers", [])
                for customer in customers:
                    if customer.get("name", "") == customer_name:
                        product_name = product.get("name", "Нет названия")
                        product_price = product.get("price", "Нет цены")
                        purchase_info += f"Товар: {product_name}, Стоимость: {product_price} USD\n"

        # Очищаем виджет Text и выводим информацию о покупках
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        self.documents_text.insert("end", purchase_info)
        self.documents_text.config(state="disabled")

    def get_products_by_color(self):
        color = self.color_entry.get()
        product_info = ""
        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                characteristics = product.get("characteristics", {})
                if "color" in characteristics and characteristics["color"].lower() == color.lower():
                    product_name = product.get("name", "Нет названия")
                    product_manufacturer = product.get("manufacturer", "Нет производителя")
                    product_price = product.get("price", "Нет цены")
                    product_info += f"Товар: {product_name}, Производитель: {product_manufacturer}, Цена: {product_price} USD\n"

        # Очищаем виджет Text и выводим информацию о товарах с заданным цветом
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        self.documents_text.insert("end", product_info)
        self.documents_text.config(state="disabled")

    def calculate_total_sales(self):
        total_sales = 0
        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                customers = product.get("customers", [])
                for i in customers:
                    product_price = product.get("price", 0)
                    total_sales += product_price

        # Очищаем виджет Text и выводим общую сумму продаж
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        self.documents_text.insert("end", f"Общая сумма продаж: {total_sales} USD\n")
        self.documents_text.config(state="disabled")

    def count_products_by_category(self):
        category_counts = {}

        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                category = product.get("category", "Неизвестная категория")
                category_counts[category] = category_counts.get(category, 0) + 1

        # Очищаем виджет Text и выводим количество товаров в каждой категории
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        for category, count in category_counts.items():
            self.documents_text.insert("end", f"Категория: {category}, Количество товаров: {count}\n")
        self.documents_text.config(state="disabled")

    def show_products_by_category(self, event=None):
        selected_category = self.selected_option.get()
        products_for_combo = []

        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                if product.get("category", "") == selected_category:
                    product_name = product.get("name", "Нет названия")
                    products_for_combo.append(product_name)

        # Обновляем Combobox с товарами выбранной категории
        self.product_entry['values'] = products_for_combo

    def show_customers_with_delivery_firm(self, event=None):
        selected_category = self.selected_option.get()
        selected_product = self.product_entry.get()
        selected_delivery_firm = self.delivery_firm_entry.get()

        customer_names_text = ""
        for collection in [kitchen.date, textile.date, electricity.date, sport.date]:
            for product in collection:
                if (
                        product.get("category", "") == selected_category
                        and product.get("name", "") == selected_product
                ):
                    # Проверяем наличие информации о фирме доставки
                    customers = product.get("customers", [])
                    for customer in customers:
                        delivery_firm = customer.get("delivery_service", "")
                        if not selected_delivery_firm or delivery_firm.lower() == selected_delivery_firm.lower():
                            # Выводим информацию о покупателях
                            customer_name = customer.get("name", "")
                            customer_names_text += f"{customer_name}\n"

        if not customer_names_text:
            customer_names_text = "Нет информации о покупателях для выбранного товара или фирмы доставки."

        # Очищаем виджет Text и выводим информацию
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        self.documents_text.insert("end", customer_names_text)
        self.documents_text.config(state="disabled")

        # Очищаем виджет Text и выводим информацию
        self.documents_text.config(state="normal")
        self.documents_text.delete(1.0, "end")
        self.documents_text.insert("end", customer_names_text)
        self.documents_text.config(state="disabled")


if __name__ == '__main__':
    main = MongoWindow()
