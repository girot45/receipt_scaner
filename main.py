import json
import sys
from datetime import datetime

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from config import INPUT_DATE_FORMATE, OUTPUT_DATE_FORMATE
from read_qr import decode_qr_code


class TableViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Table Viewer")
        self.setGeometry(100, 100, 1000, 600)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)
        self.central_widget.setLayout(self.layout)

        # Создаем заголовки столбцов
        column_headers = ["#", "Название", "Цена", "Кол.", "Сумма"]
        self.table_widget.setColumnCount(len(column_headers))
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        # Пример данных для заполнения таблицы
        data = prepare_data()

        # Заполняем таблицу данными
        for row_data in data:
            row_idx = self.table_widget.rowCount()
            self.table_widget.insertRow(row_idx)
            for col_idx, cell_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx,
                                          QTableWidgetItem(cell_data))

        # Устанавливаем растягивание последнего столбца
        self.table_widget.horizontalHeader().setStretchLastSection(True)

def prepare_data(img):
    decoded_data = decode_qr_code(img)
    if decoded_data is None:
        print("Неправильное фото чека")
        return []
    else:

        url = "https://proverkacheka.com/api/v1/check/get"
        data = {
            "token": "23306.aCEXzF1zJg260dfSp",
            "qrraw": decoded_data
        }

        resp = requests.post(url, data=data)
        receipt_info = json.loads(resp.text)
        # pprint.pprint(receipt_info)

        receipt = receipt_info["data"]["json"]

        print(datetime.strptime(receipt['dateTime'],
                                INPUT_DATE_FORMATE).strftime(
            OUTPUT_DATE_FORMATE))
        print(receipt["totalSum"] / 100)
        table = []
        for item in receipt["items"]:
            row = ["1", item['name'], str(item['price'] / 100),
                   str(item['quantity']), str(item['sum'] / 100)]
            print(f"Стоимость: {item['price'] / 100} | Кол-во: "
                  f"{item['quantity']} | Сумма: {item['sum'] / 100} | "
                  f"Название:"
                  f" {item['name']}")
            table.append(row)
        print(table)
        return table


def main():
    app = QApplication(sys.argv)
    window = TableViewerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()