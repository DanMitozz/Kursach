import sys
import sqlite3
from datetime import datetime
from functools import partial

from PyQt5 import uic
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QSpinBox, QMessageBox, \
    QDateTimeEdit
from IS_compl import *





class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        #
        # Установить ширину первого столбца на 90 пикселей
        self.main_ui.tableProduct.setColumnWidth(0, 90)
        # Установить ширину второго столбца на 140 пикселей
        self.main_ui.tableProduct.setColumnWidth(1, 155)
        # Установить ширину шестого столбца на 145 пикселей
        self.main_ui.tableProduct.setColumnWidth(5, 144)
        # Установить ширину седьмого столбца на 90 пикселей
        self.main_ui.tableProduct.setColumnWidth(6, 85)
        #
        # Установить ширину седьмого столбца на 90 пикселей
        self.main_ui.tableCollectOrder.setColumnWidth(0, 90)
        self.main_ui.tableCollectOrder.setColumnWidth(1, 100)
        self.main_ui.tableCollectOrder.setColumnWidth(2, 89)
        self.main_ui.tableCollectOrder.setColumnWidth(3, 59)
        #

        #

        #

        #
        # Кнопка для вкладки товаров
        self.main_ui.pushButton_Product.clicked.connect(self.clickProduct)
        # Кнопки на вкладке Product
        self.main_ui.pushButton_AddProductMove.clicked.connect(self.clickAddProductMove)
        self.main_ui.pushButton_ChangeProductMove.clicked.connect(self.clickChangeProductMove)
        self.main_ui.tableProduct.doubleClicked.connect(self.clickChangeProductMove)
        self.main_ui.pushButton_DeleteProduct.clicked.connect(self.clickDeleteProduct)
        self.main_ui.pushButton_CreateOrder.clicked.connect(self.clickCreateOrder)
        # Кнопки на вкладке AddProduct
        self.main_ui.pushButton_AddProduct.clicked.connect(self.clickAddProduct)
        self.main_ui.pushButton_CancelAddProduct.clicked.connect(self.clickCancelAddChangeProduct)
        # Кнопки на вкладке ChangeProduct
        self.main_ui.pushButton_ChangeProduct.clicked.connect(self.clickChangeProduct)
        self.main_ui.pushButton_CancelChangeProduct.clicked.connect(self.clickCancelAddChangeProduct)
        #
        self.selected_product_id = None
        #
        # Кнопка для вкладки категории
        self.main_ui.pushButton_Category.clicked.connect(self.clickCategory)
        # Кнопки на вкладке Categoty
        self.main_ui.pushButton_AddCategoryMove.clicked.connect(self.clickAddCategoryMove)
        self.main_ui.pushButton_ChangeCategoryMove.clicked.connect(self.clickChangeCategoryMove)
        self.main_ui.tableCategory.doubleClicked.connect(self.clickChangeCategoryMove)
        self.main_ui.pushButton_DeleteCategory.clicked.connect(self.clickDeleteCategory)
        # Кнопки на вкладке AddCategory
        self.main_ui.pushButton_AddCategory.clicked.connect(self.clickAddCategory)
        self.main_ui.pushButton_CancelAddCategory.clicked.connect(self.clickCancelAddChangeCategory)
        # Кнопки на вкладке ChangeCategory
        self.main_ui.pushButton_ChangeCategory.clicked.connect(self.clickChangeCategory)
        self.main_ui.pushButton_CancelChangeCategory.clicked.connect(self.clickCancelAddChangeCategory)
        #

        #
        # Кнопка для вкладки заказов
        self.main_ui.pushButton_Order.clicked.connect(self.clickOrder)
        # Кнопки на вкладке Order
        self.main_ui.pushButton_DeleteOrder.clicked.connect(self.clickDeleteOrder)
        self.main_ui.pushButton_OrderInfoMove.clicked.connect(self.clickOrderInfoMove)
        self.main_ui.tableOrder.doubleClicked.connect(self.clickOrderInfoMove)
        # Кнопки на вкладке OrderInfo
        self.main_ui.pushButton_CancelOrderInfo.clicked.connect(self.clickCancelOrderInfo)
        #

        #
        # Кнопка для вкладки отчетов
        self.main_ui.pushButton_Report.clicked.connect(self.clickReport)
        # Кнопка для создания отчетов
        self.main_ui.pushButton_CreateReport.clicked.connect(self.clickCreateReport)
        #
        self.AddReportType()
        #

        # Подключение к базе данных
        self.connection = sqlite3.connect('torg.db')
        self.cursor = self.connection.cursor()

        # Заполнение таблицы категорий
        self.showCategoryTable()
        # Заполнение таблицы товары
        self.showProductTable()
        # Заполнение таблицы заказы
        self.showOrderTable()

        self.order_data = {}  # Словарь для хранения информации о заказах

        # Создаем экземпляр QIntValidator и устанавливаем его для QLineEdit
        int_validator = QIntValidator()
        self.main_ui.lineEdit_AddQuantyProduct.setValidator(int_validator)
        self.main_ui.lineEdit_ChangeQuantyProduct.setValidator(int_validator)

        # Создаем экземпляр QDoubleValidator и устанавливаем его для QLineEdit
        double_validator = QDoubleValidator()
        self.main_ui.lineEdit_AddPriceProduct.setValidator(double_validator)
        self.main_ui.lineEdit_ChangePriceProduct.setValidator(double_validator)

    #
    #
    #
    def showOrderTable(self):
        # Очищаем таблицу перед заполнением
        self.main_ui.tableOrder.setRowCount(0)

        # Выполняем SQL-запрос для получения данных из таблицы Orders
        self.cursor.execute("SELECT id_order, date_order ,price_order  FROM Orders")
        orders_data = self.cursor.fetchall()

        # Заполняем таблицу значениями
        for row, (id_order, date_order, price_order) in enumerate(orders_data):
            self.main_ui.tableOrder.insertRow(row)
            self.main_ui.tableOrder.setItem(row, 0, QTableWidgetItem(str(id_order)))
            self.main_ui.tableOrder.setItem(row, 1, QTableWidgetItem(str(date_order)))
            self.main_ui.tableOrder.setItem(row, 2, QTableWidgetItem(str(price_order)))

    #
    #
    #
    def showCategoryTable(self):
        # Выполнение SQL-запроса для выборки данных из таблицы Category
        self.cursor.execute("SELECT id_category, category_name FROM Category")
        result = self.cursor.fetchall()

        # Очистка таблицы перед заполнением новыми данными
        self.main_ui.tableCategory.setRowCount(0)

        # Заполнение таблицы данными из результата запроса
        for row_num, row_data in enumerate(result):
            self.main_ui.tableCategory.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.main_ui.tableCategory.setItem(row_num, col_num, item)

                item.setToolTip(str(col_data))

    #
    #
    #
    def showProductTable(self):
        # Выполнение SQL-запроса для выборки данных из таблицы Product
        self.cursor.execute(
            "SELECT id_product, product_name, id_category, quanty_in_stock, unit_price, id_manufacturer FROM Product")
        result = self.cursor.fetchall()

        # Очистка таблицы перед заполнением новыми данными
        self.main_ui.tableProduct.setRowCount(0)

        # Заполнение таблицы данными из результата запроса
        for row_num, row_data in enumerate(result):
            self.main_ui.tableProduct.insertRow(row_num)

            # Получение названия категории по её id
            category_id = row_data[2]
            category_name = self.get_category_name(category_id)

            # Получение названия изготовителя по его id
            manufacturer_id = row_data[5]
            manufacturer_name = self.get_manufacturer_name(manufacturer_id)

            # Замена id на названия в данных перед добавлением в таблицу
            row_data = list(row_data)
            row_data[2] = category_name
            row_data[5] = manufacturer_name

            for col_num, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.main_ui.tableProduct.setItem(row_num, col_num, item)

                item.setToolTip(str(col_data))

        # Получаем количество строк в таблице
        row_count = self.main_ui.tableProduct.rowCount()

        # Создаем кнопку для каждой строки
        for row in range(row_count):
            button = QPushButton("+")
            button.clicked.connect(partial(self.pushButton_AddProductToOrder_clicked, row))

            # Устанавливаем кнопку в ячейку
            self.main_ui.tableProduct.setCellWidget(row, self.main_ui.tableProduct.columnCount() - 1, button)

    def get_category_name(self, category_id):
        # SQL-запрос для получения названия категории по её id
        self.cursor.execute("SELECT category_name FROM Category WHERE id_category = ?", (category_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "Unknown Category"

    def get_manufacturer_name(self, manufacturer_id):
        # SQL-запрос для получения названия изготовителя по его id
        self.cursor.execute("SELECT manufacturer_name FROM Manufacturer WHERE id_manufacturer = ?", (manufacturer_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "Unknown Manufacturer"

    # Функции связанные с Product /////

    def update_order_price_label(self):
        total_price = 0
        for product_number, item_data in self.order_data.items():
            quantity = item_data['quantity']
            price = item_data.get('price', 0)
            total_price += quantity * price

        self.main_ui.label_OrderPrice.setText(f"Стоимость заказа: {total_price} руб.")

    def pushButton_AddProductToOrder_clicked(self, row):
        product_number = self.main_ui.tableProduct.item(row, 0).text()
        product_name = self.main_ui.tableProduct.item(row, 1).text()
        available_quantity = int(self.main_ui.tableProduct.item(row, 3).text())
        price = float(self.main_ui.tableProduct.item(row, 4).text())

        if product_number in self.order_data:
            item_data = self.order_data[product_number]
            if item_data['quantity'] < available_quantity:
                item_data['quantity'] += 1
                spin_box = item_data['spin_box']
                spin_box.setValue(item_data['quantity'])
        else:
            current_row = self.main_ui.tableCollectOrder.rowCount()
            self.main_ui.tableCollectOrder.insertRow(current_row)

            self.main_ui.tableCollectOrder.setItem(current_row, 0, QTableWidgetItem(product_number))
            self.main_ui.tableCollectOrder.setItem(current_row, 1, QTableWidgetItem(product_name))

            spin_box = QSpinBox()
            spin_box.setProperty("row", current_row)
            spin_box.setMinimum(0)
            spin_box.setMaximum(available_quantity)  # Ограничение на максимальное количество товара
            spin_box.setValue(1)
            spin_box.valueChanged.connect(self.spinBoxQuantityProductInOrder_changed)
            self.main_ui.tableCollectOrder.setCellWidget(current_row, 2, spin_box)

            remove_button = QPushButton("✖")
            remove_button.setProperty("row", current_row)
            remove_button.clicked.connect(self.pushButton_RemoveItem_clicked)
            self.main_ui.tableCollectOrder.setCellWidget(current_row, 3, remove_button)

            # Запрещаем редактирование для первых двух столбцов
            for col in range(2):
                item = self.main_ui.tableCollectOrder.item(current_row, col)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            self.order_data[product_number] = {'row': current_row, 'quantity': 1, 'spin_box': spin_box, 'price': price}

        self.update_order_price_label()

    def spinBoxQuantityProductInOrder_changed(self, value):
        sender = self.sender()
        row = sender.property("row")
        total_quantity_item = self.main_ui.tableCollectOrder.item(row, 2)

        # Запрещаем редактирование для первых двух столбцов
        for col in range(2):
            item = self.main_ui.tableCollectOrder.item(row, col)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        if total_quantity_item is not None:
            total_quantity_item.setText(str(value))
        product_number = self.main_ui.tableCollectOrder.item(row, 0).text()

        self.order_data[product_number]['quantity'] = value

        if value == 0:
            del self.order_data[product_number]
            self.main_ui.tableCollectOrder.removeRow(row)

        self.update_order_price_label()

    def pushButton_RemoveItem_clicked(self):
        try:
            selected_row = self.main_ui.tableCollectOrder.currentRow()

            if selected_row != -1:  # -1 означает, что ни одна строка не выбрана
                product_number_item = self.main_ui.tableCollectOrder.item(selected_row, 0)

                if product_number_item is not None:
                    product_number = product_number_item.text()

                    if product_number in self.order_data:
                        self.main_ui.tableCollectOrder.removeRow(selected_row)
                        del self.order_data[product_number]
                        self.update_order_price_label()  # Обновляем сразу после удаления строки
                    else:
                        print(f"Error: Product number '{product_number}' not found in order_data.")
                else:
                    print("Error: product_number_item is None.")
            else:
                print("Error: No row selected.")
        except Exception as e:
            print(f"Error in pushButton_RemoveItem_clicked: {e}")

    # Функция перехода на вкладку Product
    def clickProduct(self):
        print("Переход на вкладку Product")
        self.showProductTable()
        self.main_ui.stackedWidget.setCurrentIndex(0)

    # Функция перехода на вкладку добавления товара
    def clickAddProductMove(self):
        self.AddCategoryAndManufscturer()


        self.main_ui.lineEdit_AddProductName.clear()
        self.main_ui.lineEdit_AddQuantyProduct.clear()
        self.main_ui.lineEdit_AddPriceProduct.clear()

        print("Переход на вкладку добавления товара")
        self.main_ui.stackedWidget.setCurrentIndex(1)

    # Функция перехода на вкладку изменения товара
    def clickChangeProductMove(self):
        print("Падение программы в точке 1")
        self.ChangeCategoryAndManufscturer()
        print("Падение программы в точке 1.2")

        # Получаем выделенную строку
        selected_row = self.main_ui.tableProduct.currentRow()

        print("Падение программы в точке 2")

        # Проверяем, что строка не выделена (selected_row равен -1)
        if selected_row == -1:
            # Если строка не была выбрана, выбираем первую строку
            selected_row = 0
            # Выделение первой строки в таблице
            self.main_ui.tableProduct.setCurrentCell(selected_row, 0)

        # Проверяем, что строка выделена (после возможного изменения selected_row в блоке выше)
        if selected_row >= 0:
            # Очищаем данные перед изменением товара
            self.main_ui.lineEdit_ChangeProductName.clear()
            self.main_ui.lineEdit_ChangeQuantyProduct.clear()
            self.main_ui.lineEdit_ChangePriceProduct.clear()
            self.main_ui.comboBox_ChangeCategoryProduct.setCurrentIndex(0)
            self.main_ui.comboBox_ChangeManufacturer.setCurrentIndex(0)
            self.selected_product_id = None

            print("Падение программы в точке 3")

            # Получаем ID, название товара и другие данные из выделенной строки
            product_id = int(self.main_ui.tableProduct.item(selected_row, 0).text())
            product_name = self.main_ui.tableProduct.item(selected_row, 1).text()
            category_name = self.main_ui.tableProduct.item(selected_row, 2).text()
            quantity = self.main_ui.tableProduct.item(selected_row, 3).text()
            price = self.main_ui.tableProduct.item(selected_row, 4).text()
            manufacturer_name = self.main_ui.tableProduct.item(selected_row, 5).text()

            print("Падение программы в точке 4")

            # Заполняем соответствующие поля на вкладке изменения товара
            self.main_ui.lineEdit_ChangeProductName.setText(product_name)
            self.main_ui.lineEdit_ChangeQuantyProduct.setText(quantity)
            self.main_ui.lineEdit_ChangePriceProduct.setText(price)

            # Устанавливаем соответствующие значения в comboBox_ChangeCategoryProduct и comboBox_ChangeManufacturer
            index_category = self.main_ui.comboBox_ChangeCategoryProduct.findText(category_name)
            if index_category != -1:
                self.main_ui.comboBox_ChangeCategoryProduct.setCurrentIndex(index_category)

            index_manufacturer = self.main_ui.comboBox_ChangeManufacturer.findText(manufacturer_name)
            if index_manufacturer != -1:
                self.main_ui.comboBox_ChangeManufacturer.setCurrentIndex(index_manufacturer)

            # Сохраняем данные для последующего использования
            self.selected_product_id = product_id

        print("Падение программы в точке 5")
        print("Переход на вкладку изменения товара")
        self.main_ui.stackedWidget.setCurrentIndex(2)

    # Функция удаления товара
    def clickDeleteProduct(self):
        selected_row = self.main_ui.tableProduct.currentRow()
        if selected_row >= 0:
            # Получаем ID записи, которую нужно удалить
            id_to_delete = int(self.main_ui.tableProduct.item(selected_row, 0).text())

            # Удаляем запись из базы данных
            self.cursor.execute("DELETE FROM Product WHERE id_product = ?", (id_to_delete,))
            self.connection.commit()
            # Заполнение таблицы Товары
            self.showProductTable()
        print("Товар удален!!!")

    # Функция добавления товара и переход на вкладку Product
    def clickAddProduct(self):


        category = self.main_ui.comboBox_AddCategoryProduct.currentText()
        manufacturer = self.main_ui.comboBox_AddManufacturer.currentText()
        price = self.main_ui.lineEdit_AddPriceProduct.text()
        product_name = self.main_ui.lineEdit_AddProductName.text()
        quantity = self.main_ui.lineEdit_AddQuantyProduct.text()

        # Проверка на пустое поле названия товара
        if not product_name:
            self.main_ui.label_3.setStyleSheet("color: red;")
            return

        if float(price) < 0:
            price = str(float(price) * -1)

        if int(quantity) < 0:
            quantity = str(int(quantity) * -1)

        # Получение id_category по названию категории
        self.cursor.execute("SELECT id_category FROM Category WHERE category_name = ?", (category,))
        id_category = self.cursor.fetchone()[0]

        # Получение id_manufacturer по названию производителя
        self.cursor.execute("SELECT id_manufacturer FROM Manufacturer WHERE manufacturer_name = ?", (manufacturer,))
        id_manufacturer = self.cursor.fetchone()[0]

        try:
            # Добавление товара в таблицу Product
            self.cursor.execute("""
                        INSERT INTO Product (product_name, id_category, unit_price, id_manufacturer, quanty_in_stock)
                        VALUES (?, ?, ?, ?, ?)
                    """, (product_name, id_category, price, id_manufacturer, quantity))
            print("Товар успешно добавлен.")
        except Exception as e:
            # В случае ошибки откатываем изменения
            self.connection.rollback()
            print(f"Ошибка при добавлении товара: {e}")
            return

        self.connection.commit()

        print("Добавление товара и переход на вкладку Product")

        # Очистка полей после добавления товара
        self.main_ui.lineEdit_AddPriceProduct.clear()
        self.main_ui.lineEdit_AddProductName.clear()
        self.main_ui.lineEdit_AddQuantyProduct.clear()

        self.main_ui.label_3.setStyleSheet("color: black;")

        # Заполнение таблицы товары
        self.showProductTable()

        self.main_ui.stackedWidget.setCurrentIndex(0)

    def AddCategoryAndManufscturer(self):
        # Заполнение comboBox_AddCategoryProduct
        # Очищение QComboBox перед заполнением
        self.main_ui.comboBox_AddCategoryProduct.clear()

        # Выполните SQL-запрос для выборки названий категорий из таблицы Category
        self.cursor.execute("SELECT category_name FROM Category")
        result = self.cursor.fetchall()

        # Добавьте полученные названия категорий в QComboBox
        for category_name in result:
            self.main_ui.comboBox_AddCategoryProduct.addItem(category_name[0])
        # Завершение заполнения comboBox_AddCategoryProduct

        # Заполнение comboBox_AddManufacturer
        # Очищение QComboBox перед заполнением
        self.main_ui.comboBox_AddManufacturer.clear()

        # Выполните SQL-запрос для выборки названий категорий из таблицы Manufacturer
        self.cursor.execute("SELECT manufacturer_name FROM Manufacturer")
        result = self.cursor.fetchall()

        # Добавьте полученные названия категорий в QComboBox
        for category_name in result:
            self.main_ui.comboBox_AddManufacturer.addItem(category_name[0])
        # Завершение заполнения comboBox_AddManufacturer

    def ChangeCategoryAndManufscturer(self):
        # Заполнение comboBox_ChangeCategoryProduct
        # Очищение QComboBox перед заполнением
        self.main_ui.comboBox_ChangeCategoryProduct.clear()

        # Выполните SQL-запрос для выборки названий категорий из таблицы Category
        self.cursor.execute("SELECT category_name FROM Category")
        result = self.cursor.fetchall()

        # Добавьте полученные названия категорий в QComboBox
        for category_name in result:
            self.main_ui.comboBox_ChangeCategoryProduct.addItem(category_name[0])
        # Завершение заполнения comboBox_ChangeCategoryProduct

        # Заполнение comboBox_ChangeManufacturer
        # Очищение QComboBox перед заполнением
        self.main_ui.comboBox_ChangeManufacturer.clear()

        # Выполните SQL-запрос для выборки названий категорий из таблицы Manufacturer
        self.cursor.execute("SELECT manufacturer_name FROM Manufacturer")
        result = self.cursor.fetchall()

        # Добавьте полученные названия категорий в QComboBox
        for category_name in result:
            self.main_ui.comboBox_ChangeManufacturer.addItem(category_name[0])
        # Завершение заполнения comboBox_ChangeManufacturer

    # Функция изменения информации о товаре и переход на вкладку Product
    def clickChangeProduct(self):
        print("Падение программы в точке 6")
        # Получаем данные из полей ввода
        product_name = self.main_ui.lineEdit_ChangeProductName.text()
        quantity = self.main_ui.lineEdit_ChangeQuantyProduct.text()
        price = self.main_ui.lineEdit_ChangePriceProduct.text()
        category_name = self.main_ui.comboBox_ChangeCategoryProduct.currentText()
        manufacturer_name = self.main_ui.comboBox_ChangeManufacturer.currentText()

        # Проверка на пустое поле названия товара
        if not product_name:
            self.main_ui.label_10.setStyleSheet("color: red;")
            return

        if not price:
            price = "0"

        if not quantity:
            quantity = "0.0"

        if float(price) < 0:
            price = str(float(price) * -1)
        #
        if int(quantity) < 0:
            quantity = str(int(quantity) * -1)

        print("Падение программы в точке 7")
        try:
            # Получение id_category по названию категории
            self.cursor.execute("SELECT id_category FROM Category WHERE category_name = ?", (category_name,))
            id_category = self.cursor.fetchone()[0]

            # Получение id_manufacturer по названию производителя
            self.cursor.execute("SELECT id_manufacturer FROM Manufacturer WHERE manufacturer_name = ?",
                                (manufacturer_name,))
            id_manufacturer = self.cursor.fetchone()[0]

            # Выполнение SQL-запроса для изменения данных о товаре
            self.cursor.execute("""
                            UPDATE Product 
                            SET product_name=?, id_category=?, unit_price=?, id_manufacturer=?, quanty_in_stock=?
                            WHERE id_product=?
                        """, (product_name, id_category, price, id_manufacturer, quantity, self.selected_product_id))
            print("ошибка 3")
        except Exception as e:
            # В случае ошибки откатываем изменения
            self.connection.rollback()
            print(f"Ошибка при изменении товара: {e}")
        print("Падение программы в точке 8")
        self.connection.commit()

        # Очистка полей после изменения товара
        self.main_ui.lineEdit_ChangeProductName.clear()
        self.main_ui.lineEdit_ChangeQuantyProduct.clear()
        self.main_ui.lineEdit_ChangePriceProduct.clear()
        self.main_ui.comboBox_ChangeCategoryProduct.clear()
        self.main_ui.comboBox_ChangeManufacturer.clear()
        self.selected_product_id = None
        print("Падение программы в точке 9")

        self.main_ui.label_10.setStyleSheet("color: black;")

        # Заполнение таблицы товары
        self.showProductTable()

        print("Изменение товара и переход на вкладку Product")
        self.main_ui.stackedWidget.setCurrentIndex(0)

    # Функция отмены добавления или изменения товара и переход на вкладку Product
    def clickCancelAddChangeProduct(self):
        print("Отмена добавления или изменения товара")

        self.main_ui.lineEdit_AddProductName.clear()
        self.main_ui.lineEdit_AddQuantyProduct.clear()
        self.main_ui.lineEdit_AddPriceProduct.clear()

        self.main_ui.stackedWidget.setCurrentIndex(0)

    def clickCreateOrder(self):
        client_full_name = self.main_ui.lineEdit_ClientFullName.text().strip()
        client_contact = self.main_ui.lineEdit_ClientNumber.text().strip()

        if client_full_name and ' ' in client_full_name:
            if not self.order_data:
                QMessageBox.warning(self, " ", "Добавьте товары в заказ перед созданием.")
                return

            client_surname, client_name = client_full_name.split(' ', 1)

            current_date_time = QDateTime.currentDateTime().toString("yyyy-MM-dd")

            total_price = 0
            for product_number, item_data in self.order_data.items():
                quantity = item_data['quantity']
                price = item_data.get('price', 0)
                total_price += quantity * price

            try:
                # Start a transaction
                self.connection.commit()

                # Insert into Orders
                self.cursor.execute(
                    "INSERT INTO Orders (client_surname, client_name, client_contact, date_order, price_order) VALUES (?, ?, ?, ?, ?)",
                    (client_surname, client_name, client_contact, current_date_time, total_price)
                )
                new_order_id = self.cursor.lastrowid

                # Insert into OrderProduct and update Product
                for product_number, item_data in self.order_data.items():
                    id_product = int(product_number)
                    quantity_in_order = item_data['quantity']

                    # Insert into OrderProduct
                    self.cursor.execute(
                        "INSERT INTO OrderProduct (id_order, id_product, quanty_product_in_order) VALUES (?, ?, ?)",
                        (new_order_id, id_product, quantity_in_order)
                    )

                    # Update Product quantity_in_stock
                    current_quantity = self.get_current_quantity_in_stock(id_product)
                    new_quantity = current_quantity - quantity_in_order

                    self.cursor.execute(
                        "UPDATE Product SET quanty_in_stock = ? WHERE id_product = ?",
                        (new_quantity, id_product)
                    )

                self.connection.commit()

                # Очистка данных заказа
                self.main_ui.lineEdit_ClientFullName.clear()
                self.main_ui.lineEdit_ClientNumber.clear()
                self.order_data = {}
                self.main_ui.tableCollectOrder.setRowCount(0)
                self.update_order_price_label()

                self.showProductTable()

                QMessageBox.information(self, " ", f"Заказ успешно создан с ID: {new_order_id}!")
                self.main_ui.labelClientFullName.setStyleSheet("color: black;")

                print(f"Создание заказа с ID: {new_order_id}")

                # Здесь можете добавить дополнительные действия или переход на другую страницу/окно при необходимости

            except Exception as e:
                print("Error during order creation:", e)
                self.connection.rollback()
                QMessageBox.warning(self, " ", f"Произошла ошибка при создании заказа: {str(e)}")



        else:
            self.main_ui.labelClientFullName.setStyleSheet("color: red")

    def get_current_quantity_in_stock(self, id_product):

        self.cursor.execute("SELECT quanty_in_stock FROM Product WHERE id_product = ?", (id_product,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 0

    # Функции связанные с Product /////

    # Функции связанные с Category /////
    # Функция перехода на вкладку Category
    def clickCategory(self):
        print("Переход на вкладку Category")
        self.showCategoryTable()
        self.main_ui.stackedWidget.setCurrentIndex(3)

    # Функция перехода на вкладку добавления категории
    def clickAddCategoryMove(self):
        print("Переход на вкладку добавления категории")
        self.main_ui.lineEdit_AddCategory.clear()
        self.main_ui.stackedWidget.setCurrentIndex(4)

    # Функция перехода на вкладку изменения категории
    def clickChangeCategoryMove(self):
        print("Переход на вкладку изменения категории")

        # Получаем выделенную строку
        selected_row = self.main_ui.tableCategory.currentRow()

        # Проверяем, что строка не выделена (selected_row равен -1)
        if selected_row == -1:
            # Если строка не была выбрана, выбираем первую строку
            selected_row = 0
            # Выделение первой строки в таблице
            self.main_ui.tableCategory.setCurrentCell(selected_row, 0)

            # Получаем ID и название категории из выделенной строки
            category_id = int(self.main_ui.tableCategory.item(selected_row, 0).text())
            category_name = self.main_ui.tableCategory.item(selected_row, 1).text()

            # Заполняем lineEdit_ChangeCategory
            self.main_ui.lineEdit_ChangeCategory.setText(category_name)

            # Сохраняем данные для последующего использования
            self.selected_category_id = category_id
            self.selected_category_name = category_name

            # Переключаемся на вкладку изменения категории
            self.main_ui.stackedWidget.setCurrentIndex(5)

    # Функция удаления категории
    def clickDeleteCategory(self):
        selected_row = self.main_ui.tableCategory.currentRow()
        if selected_row >= 0:
            # Получаем ID записи, которую нужно удалить
            id_to_delete = int(self.main_ui.tableCategory.item(selected_row, 0).text())

            # Удаляем запись из базы данных
            self.cursor.execute("DELETE FROM Category WHERE id_category = ?", (id_to_delete,))
            self.connection.commit()
            # Заполнение таблицы категорий
            self.showCategoryTable()
        print("Категория удалена!!!")

    # Функция добавления категории и переход на вкладку Category
    def clickAddCategory(self):
        print("ER1")
        category_name = self.main_ui.lineEdit_AddCategory.text()

        if not category_name:
            self.main_ui.label_AddCategoryName.setStyleSheet("color: red;")
            return
        print(category_name)
        try:
            # Добавление категории в таблицу Category
            self.cursor.execute("""
                                INSERT INTO Category (category_name)
                                VALUES (?)
                            """, (category_name,))
            print("ошибка 3")
        except Exception as e:
            # В случае ошибки откатываем изменения
            self.connection.rollback()
            print(f"Ошибка при добавлении товара: {e}")

        self.connection.commit()

        print("ошибка после запросов")

        # Очистка полей после добавления товара
        self.main_ui.lineEdit_AddCategory.clear()

        # Заполнение таблицы категорий
        self.showCategoryTable()

        self.main_ui.label_AddCategoryName.setStyleSheet("color: black;")

        print("Категория добавлена")
        self.main_ui.stackedWidget.setCurrentIndex(3)

    # Функция изменения категории и переход на вкладку Category
    def clickChangeCategory(self):
        print("Категория изменена")
        if self.selected_category_id is not None:
            new_category_name = self.main_ui.lineEdit_ChangeCategory.text()

            if not new_category_name:
                self.main_ui.label_ChangeCategoryName.setStyleSheet("color: red;")
                return

            try:
                self.cursor.execute("UPDATE Category SET category_name = ? WHERE id_category = ?",
                                    (new_category_name, self.selected_category_id))
            except Exception as e:
                self.connection.rollback()
                print(f"Ошибка при изменении категории: {e}")

            self.connection.commit()

            # Очищаем переменные после изменения
            self.selected_category_id = None
            self.selected_category_name = None
            self.main_ui.lineEdit_ChangeCategory.clear()

            self.main_ui.label_ChangeCategoryName.setStyleSheet("color: black;")

            self.showCategoryTable()

            # Переключаемся обратно на вкладку категорий
            self.main_ui.stackedWidget.setCurrentIndex(3)

    # Функция отмены добавления или изменения категории и переход на вкладку Category
    def clickCancelAddChangeCategory(self):
        print("Отмена добавления или изменения категории")

        self.main_ui.lineEdit_AddCategory.clear()

        self.main_ui.stackedWidget.setCurrentIndex(3)

    # Функции связанные с Category /////

    # Функции связанные с Order /////
    # Функция перехода на вкладку Order
    def clickOrder(self):
        self.showOrderTable()
        print("Переход на вкладку Order")
        self.main_ui.stackedWidget.setCurrentIndex(6)

    def clickOrderInfoMove(self):
        print("Переход на вкладку с информацией о заказе")

        # Получаем выделенные строки
        selected_items = self.main_ui.tableOrder.selectedItems()

        # Если нет выделенных элементов, выбираем первую запись
        if not selected_items:
            self.main_ui.tableOrder.selectRow(0)
            selected_items = self.main_ui.tableOrder.selectedItems()

        # Если всё еще нет выделенных элементов, выходим из функции
        if not selected_items:
            return

        # Получаем id_order для выделенной строки
        selected_row = selected_items[0].row()
        id_order = int(self.main_ui.tableOrder.item(selected_row, 0).text())

        # Выполняем SQL-запрос для получения данных о продуктах в заказе по id_order
        self.cursor.execute(
            "SELECT Product.id_product, Product.product_name, OrderProduct.quanty_product_in_order "
            "FROM OrderProduct "
            "JOIN Product ON OrderProduct.id_product = Product.id_product "
            "WHERE OrderProduct.id_order = ?",
            (id_order,))
        order_product_data = self.cursor.fetchall()

        # Очищаем таблицу перед добавлением новых данных
        self.main_ui.tableOrderProductInfo.setRowCount(0)

        for row, data in enumerate(order_product_data):
            id_product, product_name, quanty_product_in_order = data

            # Вставляем новую строку в таблицу
            self.main_ui.tableOrderProductInfo.insertRow(row)

            # Заполняем ячейки значениями из запроса
            self.main_ui.tableOrderProductInfo.setItem(row, 0, QtWidgets.QTableWidgetItem(str(id_product)))
            self.main_ui.tableOrderProductInfo.setItem(row, 1, QtWidgets.QTableWidgetItem(product_name))
            self.main_ui.tableOrderProductInfo.setItem(row, 2, QtWidgets.QTableWidgetItem(str(quanty_product_in_order)))

        # Выполняем SQL-запрос для получения данных о заказе по id_order
        self.cursor.execute(
            "SELECT id_order, price_order, client_surname, client_name, client_contact FROM Orders WHERE id_order = ?",
            (id_order,))
        order_data = self.cursor.fetchone()

        if order_data:
            # Распаковываем данные из запроса
            id_order, order_price, client_surname, client_name, client_contact = order_data

            # Добавляем отладочный вывод
            print(f"Данные о заказе: {id_order}, {order_price}, {client_surname}, {client_name}, {client_contact}")

            # Устанавливаем значения для элементов интерфейса
            self.main_ui.stackedWidget.setCurrentIndex(7)
            self.main_ui.OrderNumber.setText(f"Заказ №{id_order}")
            self.main_ui.label_OrderCost.setText(f"Стоимость заказа: {order_price} руб.")
            self.main_ui.label_ClientSurnameOrder.setText(f"{client_surname}")
            self.main_ui.label_ClientNameOrder.setText(f"{client_name}")
            self.main_ui.label_ClientContactOrder.setText(f"{client_contact}")
        else:
            # Обработка случая, если заказ с указанным id_order не найден в базе данных
            print(f"Заказ №{id_order} не найден.")

        self.main_ui.stackedWidget.setCurrentIndex(7)



    # Функция перехода на вкладку Order с вкладки информации о заказе
    def clickCancelOrderInfo(self):
        print("Выход со вкладке с информацией о заказе")
        self.main_ui.stackedWidget.setCurrentIndex(6)

    # Функция удаления заказа
    def clickDeleteOrder(self):
        # Получаем выделенную строку
        selected_items = self.main_ui.tableOrder.selectedItems()

        if not selected_items:
            # Если нет выделенных элементов, выходим из функции
            return

        # Получаем id_order для выделенной строки
        selected_row = selected_items[0].row()
        id_order = int(self.main_ui.tableOrder.item(selected_row, 0).text())

        # Выполняем SQL-запрос для удаления заказа по id_order
        self.cursor.execute("DELETE FROM Orders WHERE id_order = ?", (id_order,))
        self.cursor.execute("DELETE FROM OrderProduct WHERE id_order = ?", (id_order,))
        self.connection.commit()

        print(f"Заказ №{id_order} удален.")

        # Обновляем отображение таблицы заказов
        self.showOrderTable()

    # Функции связанные с Order /////

    def clickReport(self):
        print('Переход на вкладку Report')
        self.main_ui.stackedWidget.setCurrentIndex(8)

    def AddReportType(self):
        self.main_ui.comboBox_TypeReport.addItem("Отчет о финансовой активности по месяцам")
        self.main_ui.comboBox_TypeReport.addItem("Отчет суммарной выручки по категориям")

    def clickCreateReport(self):
        # Получаем выбранный тип отчета
        report_type = self.main_ui.comboBox_TypeReport.currentText()

        self.main_ui.tableWidget_Report.setRowCount(0)
        self.main_ui.tableWidget_Report.setColumnCount(0)

        # Определите ваш SQL-запрос в соответствии с выбранным типом отчета
        if report_type == "Отчет о финансовой активности по месяцам":
            query = """
                SELECT
                    strftime('%m-%Y', Orders.date_order) AS month,
                    COUNT(Orders.id_order) AS total_orders,
                    SUM(Orders.price_order) AS total_revenue,
                    AVG(Orders.price_order) AS average_order_price
                FROM
                    Orders
                WHERE
                    Orders.date_order BETWEEN '2023-01-01' AND '2023-12-31'
                GROUP BY
                    month;
            """
            columns = ["Дата", "Всего заказов", "Общий доход", "Средняя цена заказа"]
        elif report_type == "Отчет суммарной выручки по категориям":
            query = """
                SELECT
                    Category.category_name AS product_category,
                    SUM(Orders.price_order) AS total_revenue
                FROM
                    Product
                JOIN
                    Category ON Product.id_category = Category.id_category
                JOIN
                    OrderProduct ON Product.id_product = OrderProduct.id_product
                JOIN
                    Orders ON OrderProduct.id_order = Orders.id_order
                GROUP BY
                    product_category;
            """
            columns = ["Категория товаров", "Доход"]
        else:
            print("Выбран неизвестный тип отчета.")
            return

        try:
            # Очищаем таблицу перед добавлением новых данных
            self.main_ui.tableWidget_Report.clear()
            self.main_ui.tableWidget_Report.setColumnCount(len(columns))
            self.main_ui.tableWidget_Report.setHorizontalHeaderLabels(columns)

            # Выполняем запрос и получаем данные
            self.cursor.execute(query)
            report_data = self.cursor.fetchall()

            # Заполняем таблицу значениями
            for row, data in enumerate(report_data):
                self.main_ui.tableWidget_Report.insertRow(row)
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    self.main_ui.tableWidget_Report.setItem(row, col, item)

            # Распределяем ширину колонок
            table_width = self.main_ui.tableWidget_Report.width()
            total_width = sum(self.main_ui.tableWidget_Report.columnWidth(col) for col in
                              range(self.main_ui.tableWidget_Report.columnCount()))
            scaling_factor = (table_width - 23) / total_width  # Вычесть 5 пикселей

            for col in range(self.main_ui.tableWidget_Report.columnCount()):
                new_width = self.main_ui.tableWidget_Report.columnWidth(col) * scaling_factor
                self.main_ui.tableWidget_Report.setColumnWidth(col, int(new_width))

            print(f"Создан отчет: {report_type}")
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении SQL-запроса: {e}")

    #
    #
    #
    def __del__(self):
        # Закрытие соединения с базой данных при завершении приложения
        self.connection.close()
    #
    #
    #


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())