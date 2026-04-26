from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtGui import QFont, QColor, QAction
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QToolBar, QStatusBar, QGroupBox, QDialog, QComboBox, QMessageBox, \
    QHBoxLayout, QDateEdit, QDialogButtonBox, QTextEdit, QLineEdit

from database_routine import ExamSchedule, SeatingConstraints, SeatingRooms, ExamDateTime, Seating
from backend import ConfirmationWidgets, Allocation, SeatingPlan
from Windows.B_Planner import PlanningWindow

from styles import Styles

class HomePage(QMainWindow):
    logout_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Homepage")
        self.setMinimumSize(700, 700)
        self.showMaximized()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        about_menu_item = self.menuBar().addMenu("&About")
        about_action = QAction("About", self)
        about_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        self.table1 = QTableWidget()
        self.table1.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table1.setColumnCount(3)
        self.table1.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: lightgray; color: black; font-weight: bold }")
        self.table1.verticalHeader().setVisible(False)
        self.load_slots()

        self.table2 = QTableWidget()
        self.table2.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table2.setColumnCount(3)
        self.table2.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: lightgray; color: black; font-weight: bold }")
        self.table2.setHorizontalHeaderLabels(("Slot", "Date", "Time"))
        self.table2.setColumnWidth(1, 150)  # Set the width of the second column
        self.table2.setColumnWidth(2, 160)

        self.table2.verticalHeader().setVisible(False)
        self.load_dates()


        autorun_button = QPushButton("Autorun")
        autorun_button.clicked.connect(self.autorun)
        autorun_button.setFixedSize(200, 50)
        autorun_button.setStyleSheet(Styles().blue_push_button())

        autoprint_button = QPushButton("Auto Print ALL")
        autoprint_button.clicked.connect(self.autoprint)
        autoprint_button.setFixedSize(200, 50)
        autoprint_button.setStyleSheet(Styles().blue_push_button())


        change_type_button = QPushButton("Change Settings")
        change_type_button.clicked.connect(self.change_type)
        change_type_button.setFixedSize(200, 50)
        change_type_button.setStyleSheet(Styles().blue_push_button())

        reload_rooms_button = QPushButton("Reload Rooms")
        reload_rooms_button.clicked.connect(self.reload_rooms)
        reload_rooms_button.setFixedSize(200, 50)
        reload_rooms_button.setStyleSheet(Styles().blue_push_button())

        refresh_dates_button = QPushButton("Refresh Dates")
        refresh_dates_button.clicked.connect(self.refresh_dates)
        refresh_dates_button.setFixedSize(200, 50)
        refresh_dates_button.setStyleSheet(Styles().blue_push_button())



        layout = QVBoxLayout(central_widget)
        
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table1)
        table_layout.addWidget(self.table2)
        
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(autorun_button)
        button_layout.addWidget(autoprint_button)
        button_layout.addWidget(change_type_button)
        button_layout.addWidget(reload_rooms_button)
        button_layout.addWidget(refresh_dates_button)


        layout.addLayout(table_layout)
        layout.addLayout(button_layout)



        """------------"""
        # Create stautus bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)


        self.table1.cellClicked.connect(self.cell_clicked_table1)
        self.table2.cellClicked.connect(self.cell_clicked_table2)


    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def load_slots(self):
        slots = ExamSchedule().fetch_slots()

        self.table1.setColumnCount(3)
        # Use a list comprehension to create sublists
        result = [slots[i:i + 3] for i in
                  range(0, len(slots), 3)]

        self.table1.setRowCount(0)
        # This command resets the table , thus whenever u run the program you wont get duplicate data
        for row_number, row_data in enumerate(result):
            self.table1.insertRow(row_number)
            # This inserts an empty row in the window
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setBackground(QColor("lightcyan"))
                item.setForeground(QColor("black"))  # Set text color to purple

                self.table1.setItem(row_number, column_number, item)
        self.table1.verticalHeader().setVisible(False)
        #self.table1.horizontalHeader().setVisible(False)

    def load_dates(self):
        result = ExamDateTime().fetch_dates()
        self.table2.setRowCount(0)
        # This command resets the table , thus whenever u run the program you wont get duplicate data
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            # This inserts an empty row in the window
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setBackground(QColor("antiquewhite"))
                item.setForeground(QColor("black"))  # Set text color to purple

                self.table2.setItem(row_number, column_number, item)
        self.table2.verticalHeader().setVisible(False)

    def cell_clicked_table1(self):

        plan_slot = QPushButton("Go to planner")
        plan_slot.clicked.connect(self.goto_planner)
        plan_slot.setFixedSize(200, 50)
        plan_slot.setStyleSheet(Styles().rectangle_lightgreen_button())

        # the below steps were taken to avoid duplication of buttons when we click on multiple cells
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        selected_row=self.table1.currentRow()
        if self.table1.item(selected_row,0).text()!="":
            self.statusbar.addWidget(plan_slot)
            
    def cell_clicked_table2(self):

        edit_date_button = QPushButton("Update date")
        edit_date_button.clicked.connect(self.date_edit)
        edit_date_button.setFixedSize(200, 50)
        edit_date_button.setStyleSheet(Styles().rectangle_lightgreen_button())

        edit_time_button = QPushButton("Update time")
        edit_time_button.clicked.connect(self.time_edit)
        edit_time_button.setFixedSize(200, 50)
        edit_time_button.setStyleSheet(Styles().rectangle_lightgreen_button())


        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_date_button)
        self.statusbar.addWidget(edit_time_button)
    


    def goto_planner(self):
        try:
            slot = self.table1.currentItem().text()
            self.planner = PlanningWindow(slot=slot)
            self.planner.back_to_homepage_signal.connect(self.show)
            self.planner.show()
            self.hide()
        except AttributeError:  # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a cell")

    def date_edit(self):
        try:
            row = self.table2.currentRow()
            slot = self.table2.item(row, 0).text()
            dialog = DateInputDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                selected_date = dialog.selectedDate()
                ExamDateTime().update_date(slot=slot, value=selected_date.toString("dd-MM-yyyy"))

                self.load_dates()
        except AttributeError:
            ConfirmationWidgets().error(text="Kindly Select a cell")

    def time_edit(self):
        try:
            row = self.table2.currentRow()
            old_value = self.table2.item(row, 2).text()
            slot = self.table2.item(row, 0).text()
            dialog = TimeInputDialog(old_value=old_value, parent=self)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                time = dialog.selectedTime()
                ExamDateTime().update_time(slot=slot, value=time)

                self.load_dates()
        except AttributeError:
            ConfirmationWidgets().error(text="Kindly Select a cell")
    def autorun(self):
        Allocation()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Automated Seating plan has been created")
        confirmation_widget.exec()

    def autoprint(self):
        slots = ExamSchedule().fetch_slots()

        for slot in slots:
            assigned, not_allocated = Seating().fetch_seating(slot=slot)
            if len(not_allocated) == 0:
                SeatingPlan(slot=slot,assigned=assigned,autoprint_flag=True)
            else:
                ConfirmationWidgets().error(text=f"Not all courses have been assigned rooms in slot {slot}")

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("PDFs for valid slot plans have been generated successfully.")
        confirmation_widget.exec()

    def change_type(self):
        constraints_dialog = ConstraintsDialog()
        constraints_dialog.exec()

    def reload_rooms(self):
        total_capacity = SeatingRooms().json_to_db()
        if type(total_capacity) == int:
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("Lecture halls refreshed.\n"
                                        f"Total Capacity Detected = {total_capacity}\n"
                                        f"Kindly ensure the exam was scheduled with max capacity <= {total_capacity}\n"
                                        f"(To check - open exam scheduler application >settings > Change Constraints)")
            confirmation_widget.exec()
        else:
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Error in 'seating_input.json' file")
            confirmation_widget.setText(f"{total_capacity}")
            confirmation_widget.exec()


    def refresh_dates(self):
        ExamDateTime().refresh_dates()
        self.load_dates()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The date and time data has been refreshed")
        confirmation_widget.exec()



    def closeEvent(self, event):
        #Users().reset_login_flag(emp_code=self.logged_in_user)
        super().closeEvent(event)


class ConstraintsDialog(QDialog):
    def __init__(self):
        try:
            super().__init__()

            self.setWindowTitle("Change Constraints")
            self.setMinimumSize(300,300)
            current = SeatingConstraints().fetch_settings()

            layout = QVBoxLayout()  # places widgets only vertically stacked as opposed to grid #

            label=QLabel("Number of courses per room:")
            self.dropdown = QComboBox()
            self.dropdown.setStyleSheet("background-color: lightyellow;")
            self.dropdown.addItem("1")
            self.dropdown.addItem("2")
            self.dropdown.setCurrentText(str(current))

            # update button
            button = QPushButton("Apply")
            button.clicked.connect(self.apply)
            button.setFixedHeight(25)

            button2 = QPushButton("Cancel")
            button2.clicked.connect(self.close)
            button2.setFixedHeight(25)


            """Adding Widgets"""
            layout.addWidget(label)
            layout.addWidget(self.dropdown)
            layout.addWidget(button)
            layout.addWidget(button2)


            self.setLayout(layout)
        except AttributeError: # attribute error for invalid q line edit input
            pass


    def apply(self):


        self.close()
        selected_value = int(self.dropdown.currentText())
        SeatingConstraints().toggle_seating_mode(new=selected_value)

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The constraints changed successfully")
        confirmation_widget.exec()

class DateInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Date')

        layout = QVBoxLayout()

        # Create a QDateEdit widget
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)  # Allow calendar popup to choose date
        # Set the initial date to the current date
        current_date = QDate.currentDate()
        self.date_edit.setDate(current_date)

        # Set the minimum allowed date to the current date
        #self.date_edit.setMinimumDate(current_date)

        layout.addWidget(self.date_edit)

        # Create buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def selectedDate(self):
        return self.date_edit.date()

class TimeInputDialog(QDialog):
    def __init__(self,old_value,parent=None):
        super().__init__(parent)

        self.setWindowTitle('Input Time')

        layout = QVBoxLayout()

        # Create a QDateEdit widget
        self.time_edit = QLineEdit(old_value)


        layout.addWidget(self.time_edit)

        # Create buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def selectedTime(self):
        return self.time_edit.text()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        content = "This Software was created to aid Office of Academic Affairs in creating Seating Plans for the university exams of IIT Bhilai.\n\n" \
                  "'Examination_Seating_Planner' was developed by Shubham Yogesh Mahajan\n (ID No. - 12241730) of BTech CSE - IIT Bhilai.\n\n" \
                  "In case of any query, feel free to reach out to the developer -\n\n" \
                  "Email: shubhamy0023@gmail.com\n" \
                  "Alternate Email: mahajanshubham54321@gmail.com\n\n" \
                  "Phone: +91 8879466601"

        self.setText(content)
        # self itself is the Mesage box instance

