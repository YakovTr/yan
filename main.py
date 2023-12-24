import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHBoxLayout, QWidget, \
    QPushButton, QComboBox, QVBoxLayout


class TableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.modified = {}

    def initUI(self):
        self.setWindowTitle('Table with Combo Boxes')
        self.setGeometry(100, 100, 800, 600)

        # Initialize the database connection
        self.conn = None
        self.cursor = None
        self.connectToDatabase('DB.sqlite')

        # Create a layout for combo boxes, table, and buttons
        layout = QVBoxLayout()

        # Create combo boxes for sorting options
        combo_layout = QHBoxLayout()
        self.tablecombo = QComboBox(self)
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table = [tables[0] for tables in self.cursor.fetchall()]
        self.tablecombo.addItems(table)

        self.classCombo = QComboBox(self)
        self.cursor.execute("SELECT distinct class FROM high_school")
        classes = [class_name[0] for class_name in self.cursor.fetchall()]
        self.classCombo.addItems(classes)

        self.lesson_nameCombo = QComboBox(self)
        self.cursor.execute("SELECT distinct lesson_name FROM high_school")
        names = [lesson_names[0] for lesson_names in self.cursor.fetchall()]
        self.lesson_nameCombo.addItems(names)

        self.dayCombo = QComboBox(self)
        self.cursor.execute("SELECT distinct day FROM high_school")
        day_name = [days[0] for days in self.cursor.fetchall()]
        self.dayCombo.addItems(day_name)

        self.lesson_numCombo = QComboBox(self)
        self.cursor.execute("SELECT distinct lesson_num FROM high_school")
        nums = [num[0] for num in self.cursor.fetchall()]
        self.lesson_numCombo.addItems(nums)

        combo_layout.addWidget(self.tablecombo)
        combo_layout.addWidget(self.classCombo)
        combo_layout.addWidget(self.lesson_nameCombo)
        combo_layout.addWidget(self.dayCombo)
        combo_layout.addWidget(self.lesson_numCombo)
        layout.addLayout(combo_layout)

        # Create a table widget
        self.tableWidget = QTableWidget(self)
        layout.addWidget(self.tableWidget)

        # Create buttons in a row
        button_layout = QHBoxLayout()
        self.updateButton = QPushButton('Update Table', self)
        self.deleteButton = QPushButton('Delete Row', self)
        self.addButton = QPushButton('Add Row', self)
        button_layout.addWidget(self.updateButton)
        button_layout.addWidget(self.deleteButton)
        button_layout.addWidget(self.addButton)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect button signals to functions
        self.updateButton.clicked.connect(self.save_results)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.addButton.clicked.connect(self.addRow)

        # Connect combo box signals to sorting functions
        self.classCombo.currentIndexChanged.connect(self.sortByClass)
        self.lesson_nameCombo.currentIndexChanged.connect(self.sortByLesson)
        self.dayCombo.currentIndexChanged.connect(self.sortByDay)
        self.lesson_numCombo.currentIndexChanged.connect(self.sortByNumber)

        self.showTable()

    def connectToDatabase(self, database_name):
        try:
            self.conn = sqlite3.connect(database_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)

    def showTable(self):
        # Retrieve data from the database and display it in the table widget
        table_name = self.tablecombo.currentText()

        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()

        # Clear the existing data in the table widget
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

        if data:
            # Populate the table widget with data
            column_names = [description[0] for description in self.cursor.description]
            self.tableWidget.setColumnCount(len(column_names))
            self.tableWidget.setHorizontalHeaderLabels(column_names)

            self.tableWidget.setRowCount(len(data))
            for row_num, row_data in enumerate(data):
                for col_num, cell_value in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_value))
                    self.tableWidget.setItem(row_num, col_num, item)


    def save_results(self):
        table_name = self.tablecombo.currentText()
        row_num = self.tableWidget.rowCount()

        if self.modified:
            cur = self.con.cursor()
            que = f"UPDATE {table_name} SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += f"WHERE id = {row_num}"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()
        self.showTable()

    def deleteRow(self):
        table_name = self.tablecombo.currentText()
        selected_row = self.tableWidget.currentRow()
        column_names = ["class", "lesson_name", "day", "lesson_num"]

        if selected_row >= 0:
            # Get the ID of the row to delete, assuming it's in the first column (index 0)
            row_id = self.tableWidget.item(selected_row, 0).text()
            try:
                self.cursor.execute(f"DELETE FROM {table_name} WHERE {column_names[0]} = ?", (row_id,))
                self.conn.commit()
                self.tableWidget.removeRow(selected_row)
            except sqlite3.Error as e:
                print(f"Error deleting row from the database: {e}")

    def addRow(self):
        data = ["New Class", "New Lesson", "New Day", "New Lesson Num"]
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            self.tableWidget.setItem(row_position, col, item)

        # Add the data to the database
        table_name = self.tablecombo.currentText()
        column_names = [description[0] for description in self.cursor.description]

        # Construct an INSERT statement with placeholders for the data
        insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['?'] * len(column_names))})"

        try:
            self.cursor.execute(insert_sql, data)
            self.conn.commit()
            print("Row inserted into the database successfully.")
        except sqlite3.Error as e:
            print(f"Failed to insert row into the database: {e}")

        self.showTable()

    def getTableRowItems(self, row):
        return [self.tableWidget.item(row, col) for col in range(self.tableWidget.columnCount())]

    def sortByClass(self):
        pass

    def sortByLesson(self):
        pass

    def sortByDay(self):
        pass

    def sortByNumber(self):
        pass

    def sortAndShowFilteredData(self, column_name, filter_value):
        pass


def except_hook(cls, exception, traceback):
    traceback_str = "".join(traceback.format_tb(exception.__traceback__))
    error_message = f"An exception of type {cls.__name__} occurred:\n{exception}\n{traceback_str}"
    print(error_message)
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
