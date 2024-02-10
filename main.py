import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QPushButton
import sqlite3
from main_ui import Ui_MainWindow
from addEditCoffeeForm_ui import Ui_AddEditCoffeeForm


class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, old_value=None):
        super().__init__()
        self.setupUi(self)
        self.old_value = old_value
        if old_value:
            self.setFieldsValues(old_value)

        self.okButton.clicked.connect(self.saveCoffeeData)
        self.cancelButton.clicked.connect(self.close)

    def setFieldsValues(self, values):
        self.nameLineEdit.setText(values[1])
        self.roastLineEdit.setText(values[2])
        self.typeLineEdit.setText(values[3])
        self.descriptionLineEdit.setText(values[4])
        self.priceDoubleSpinBox.setValue(values[5])
        self.volumeLineEdit.setText(values[6])

    def saveCoffeeData(self):
        name = self.nameLineEdit.text()
        roast = self.roastLineEdit.text()
        coffee_type = self.typeLineEdit.text()
        description = self.descriptionLineEdit.text()
        price = self.priceDoubleSpinBox.value()
        volume = self.volumeLineEdit.text()

        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        if self.old_value:
            cursor.execute(f"UPDATE coffee SET name=?, roast=?, type=?, description=?, price=?, volume=? WHERE ID=?",
                           (name, roast, coffee_type, description, price, volume, self.old_value[0]))
        else:
            cursor.execute(
                f"INSERT INTO coffee (name, roast, type, description, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast, coffee_type, description, price, volume))
        conn.commit()
        conn.close()
        self.close()


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.show()
        self.load_coffee_data()
        self.addButton.clicked.connect(self.openAddCoffeeForm)
        self.editButton.clicked.connect(self.openEditCoffeeForm)

    def load_coffee_data(self):
        conn = sqlite3.connect('data/coffee.sqlite')
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

    def openAddCoffeeForm(self):
        form = AddEditCoffeeForm()
        form.exec_()
        self.load_coffee_data()

    def openEditCoffeeForm(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            row_data = []
            for col_num in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(selected_row, col_num)
                if col_num != 5:
                    row_data.append(item.text())
                else:
                    row_data.append(float(item.text()))

            form = AddEditCoffeeForm(old_value=row_data)
            form.exec_()
            self.load_coffee_data()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
