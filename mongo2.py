import json
from tkinter import ttk

import pymongo
import tk

client = pymongo.MongoClient('localhost')
database = client['22303']
# Создание коллекции
collection = database["rkuzmin-shop_data"]
class ProductQueryApp:
    # listCategory = sorted(list(collection.distinct("category")))
    # listCustomer = sorted(list(collection.distinct("customer_info.customer_name")))
    # listColors = sorted(list(collection.distinct("characteristics.color")))
    # listProducts = sorted(list(collection.distinct("product_name")))
    # listDeliveries = sorted(list(collection.distinct("customer_info.delivery_service")))

    def __init__(self, master, collection):
        self.master = master
        self.master.title("Product Query App")

        self.collection = collection

        # Первый запрос
        self.category_label1 = tk.Label(self.master, text="Категория:")
        self.category_label1.grid(row=0, column=0, padx=10, pady=10)

        self.collection_var1 = tk.StringVar()
        self.collection_entry1 = ttk.Combobox(master, textvariable=self.collection_var1, values=self.listCategory)
        self.collection_entry1.grid(row=1, column=0)

        self.query_button_1 = tk.Button(self.master, text="1. Названия товаров по категории",
                                        command=self.get_product_names_by_catregory)
        self.query_button_1.grid(row=2, column=0, padx=10, pady=10)

        # Второй запрос
        self.category_label2 = tk.Label(self.master, text="Категория:")
        self.category_label2.grid(row=0, column=1, padx=10, pady=10)

        self.collection_var2 = tk.StringVar()
        self.collection_entry2 = ttk.Combobox(master, textvariable=self.collection_var2, values=self.listCategory)
        self.collection_entry2.grid(row=1, column=1)

        self.query_button_2 = tk.Button(self.master, text="2. Характеристики товаров по категории",
                                        command=self.get_product_characteristics_by_category)
        self.query_button_2.grid(row=2, column=1, padx=10, pady=10)

        # Третий запрос
        self.category_label2 = tk.Label(self.master, text="Покупатели:")
        self.category_label2.grid(row=0, column=2, padx=10, pady=10)

        self.collection_var3 = tk.StringVar()
        self.collection_entry3 = ttk.Combobox(master, textvariable=self.collection_var3, values=self.listCustomer)
        self.collection_entry3.grid(row=1, column=2)

        self.query_button_3 = tk.Button(self.master, text="3. Товары, купленные заданным покупателем",
                                        command=self.get_products_by_customer)
        self.query_button_3.grid(row=2, column=2, padx=10, pady=10)

        # Четвертый запрос
        self.category_label4 = tk.Label(self.master, text="Цвета:")
        self.category_label4.grid(row=0, column=3, padx=10, pady=10)

        self.collection_var4 = tk.StringVar()
        self.collection_entry4 = ttk.Combobox(master, textvariable=self.collection_var4, values=self.listColors)
        self.collection_entry4.grid(row=1, column=3)

        self.query_button_4 = tk.Button(self.master, text="4. Товары с заданным цветом",
                                        command=self.get_products_by_color)
        self.query_button_4.grid(row=2, column=3, padx=10, pady=10)

        # Пятый запрос
        self.category_label5 = tk.Label(self.master, text="Общая сумма:")
        self.category_label5.grid(row=3, column=0, padx=10, pady=10)

        self.query_button_5 = tk.Button(self.master, text="5. Общая сумма проданных товаров",
                                        command=self.get_total_sold_amount)
        self.query_button_5.grid(row=5, column=0, padx=10, pady=10)

        # Шестой запрос
        self.category_label6 = tk.Label(self.master, text="Товары в категориях:")
        self.category_label6.grid(row=3, column=1, padx=10, pady=10)

        self.query_button_6 = tk.Button(self.master, text="6. Количество товаров в каждой категории",
                                        command=self.get_products_count_by_category)
        self.query_button_6.grid(row=5, column=1, padx=10, pady=10)

        # Седьмой запрос
        self.category_label7 = tk.Label(self.master, text="Товары:")
        self.category_label7.grid(row=3, column=2, padx=10, pady=10)

        self.collection_var7 = tk.StringVar()
        self.collection_entry7 = ttk.Combobox(master, textvariable=self.collection_var7, values=self.listProducts)
        self.collection_entry7.grid(row=4, column=2)

        self.query_button_7 = tk.Button(self.master, text="7. Имена покупателей заданного товара",
                                        command=self.get_customer_names_by_product)
        self.query_button_7.grid(row=5, column=2, padx=10, pady=10)

        # Восьмой запрос
        self.category_label8 = tk.Label(self.master, text="Товары:")
        self.category_label8.grid(row=3, column=3, padx=10, pady=10)

        self.collection_var8 = tk.StringVar()
        self.collection_entry8 = ttk.Combobox(master, textvariable=self.collection_var8, values=self.listProducts)
        self.collection_entry8.grid(row=4, column=3)

        self.category_label8_1 = tk.Label(self.master, text="Службы доставки")
        self.category_label8_1.grid(row=5, column=3, padx=10, pady=10)

        self.collection_var8_1 = tk.StringVar()
        self.collection_entry8 = ttk.Combobox(master, textvariable=self.collection_var8_1, values=self.listDeliveries)
        self.collection_entry8.grid(row=6, column=3)

        self.query_button_8 = tk.Button(self.master, text="8. Имена покупателей с доставкой от заданной фирмы",
                                        command=self.get_customer_names_by_product_and_delivery)
        self.query_button_8.grid(row=7, column=3, padx=10, pady=10)

        # Блок с результатом
        self.result_label = tk.Label(self.master, text="Результат:")
        self.result_label.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

        self.result_text = tk.Text(self.master, height=10, width=50, state="disabled")
        self.result_text.grid(row=9, column=1, columnspan=2, padx=10, pady=10)

    #####################################################
    # 1 запрос
    def get_product_names_by_catregory(self):
        category = self.collection_var1.get()
        result_text = f"1. Названия товаров по категории '{category}':\n"

        pipeline = [
            {
                "$match": {"category": category}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )

        for name in a:
            result_text += name['product_name'] + '\n'

        self.update_result_text(result_text)

    # 2 запрос
    def get_product_characteristics_by_category(self):
        category = self.collection_var2.get()
        result_text = f"2. Характеристики товаров по категории '{category}':\n"

        pipeline = [
            {
                "$match": {"category": category}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": 1,
                    "characteristics": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n_______________________________________\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    # 3 запрос
    def get_products_by_customer(self):
        customer = self.collection_var3.get()

        result_text = f"3. Товары, купленные покупателем '{customer}':\n"

        pipeline = [
            {
                "$match": {"customer_info.customer_name": customer}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": "$product_name",
                    "price": "$price"
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n_______________________________________\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    # 4 запрос
    def get_products_by_color(self):
        color = self.collection_var4.get()
        result_text = f"4. Товары с цветом '{color}':\n"

        pipeline = [
            {
                "$match": {"characteristics.color": color}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": "$product_name",
                    "manufacturer": "$manufacturer",
                    "price": "$price"
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n_______________________________________\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_total_sold_amount(self):
        result_text = f"5. Общая сумма проданных товаров: "

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": "$price"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "total_sales": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = doc["total_sales"]
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_products_count_by_category(self):
        result_text = f"6. Количество товаров в каждой категории:\n"

        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "total_products": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "total_products": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n_______________________________________\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_customer_names_by_product(self):
        product_name = self.collection_var7.get()
        result_text = f"7. Имена покупателей товара '{product_name}':\n"

        pipeline = [
            {
                "$match": {"product_name": product_name}
            },
            {
                "$group": {
                    "_id": "$customer_info.customer_name"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer_name": "$_id"
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n_______________________________________\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_customer_names_by_product_and_delivery(self):
        product_name = self.collection_var8.get()
        delivery_service = self.collection_var8_1.get()

        result_text = f"8. Имена покупателей товара '{product_name}' с доставкой от '{delivery_service}':\n"

        pipeline = [
            {
                "$match": {"product_name": product_name, "customer_info.delivery_service": delivery_service}
            },
            {
                "$unwind": "$customer_info"
            },
            {
                "$match": {"customer_info.delivery_service": delivery_service}
            },
            {
                "$group": {
                    "_id": "$customer_info.customer_name"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer_name": "$_id"
                }
            }
        ]
        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = doc["customer_name"]
            self.result_text.insert(tk.END, "-" + json_str + ",\n")

        self.result_text.config(state="disabled")

    def update_result_text(self, text):
        self.result_text.config(state=tk.NORMAL)  # Включаем режим редактирования
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")


root = tk.Tk()
app = ProductQueryApp(root, collection)
root.mainloop()
