from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3
import sys


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("main.ui", self)
        self.show()
        self.load_coffee_data()

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        coffee_data = cursor.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(coffee_data))
        self.tableWidget.setColumnCount(7)

        for row_num, row_data in enumerate(coffee_data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_num, col_num, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    sys.exit(app.exec_())
