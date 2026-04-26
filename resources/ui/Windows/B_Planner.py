from collections import defaultdict

from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QToolBar, QStatusBar, QHBoxLayout, QDialog, QCheckBox, QLabel, \
    QGridLayout, QDateEdit, QDialogButtonBox, QLineEdit, QMessageBox

from backend import ConfirmationWidgets, SeatingPlan
from database_routine import Seating
from styles import Styles


class PlanningWindow(QMainWindow):
    back_to_homepage_signal=pyqtSignal()
    def __init__(self,slot):
        super().__init__()
        self.back_button_clicked=False
        self.slot =slot
        self.assigned,self.not_allocated = Seating().fetch_seating(slot=self.slot)
        self.packet_ids = defaultdict(list)
        for room in self.assigned:
            for course,packet_id,size in self.assigned[room]["assigned"]:
                self.packet_ids[course].append(packet_id)

        for item in self.not_allocated:
            course, packet_id, size = item.split("__")
            self.packet_ids[course].append(int(packet_id))




        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Plan Seating for slot {self.slot} ")
        self.setMinimumSize(700,700)
        self.showMaximized()

        back_button = QPushButton("Back To Homepage")
        back_button.setStyleSheet(Styles().dark_red_push_button())
        back_button.clicked.connect(self.back_to_homepage)

        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #0099cc; spacing: 20px;")  # Set toolbar background color
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addWidget(back_button)

        export_button = QPushButton("Export Seating Plan to PDF")
        export_button.clicked.connect(self.export)

        export_button.setStyleSheet(Styles().green_push_button())
        toolbar.addWidget(export_button)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.table1 = QTableWidget()
        self.table1.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table1.setColumnCount(5)
        self.table1.setHorizontalHeaderLabels(("ROOM", "COURSE_PACKETS", "CURRENT", "REMAINING", "MAX_CAPACITY"))
        self.table1.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: lightgray; color: black; font-weight: bold }")

        # Set width for a particular column
        self.table1.setColumnWidth(1, 500)  # Set the width of the second column
        self.table1.setColumnWidth(2, 160)

        self.table1.verticalHeader().setVisible(False)
        self.load_seating()

        self.table2 = QTableWidget()
        self.table2.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table2.setColumnCount(3)
        self.table2.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: lightgray; color: black; font-weight: bold }")
        self.table2.verticalHeader().setVisible(False)
        self.table2.setColumnWidth(0, 200)
        self.table2.setColumnWidth(1, 200)  # Set the width of the second column
        self.table2.setColumnWidth(2, 200)
        self.load_not_allocated()

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table1)
        layout.addWidget(self.table2)


        """------------"""
        # Create stautus bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect a cell click

        self.table1.cellClicked.connect(self.cell_clicked_table1)
        self.table2.cellClicked.connect(self.cell_clicked_table2)



    def load_seating(self):
        result = [[room,self.assigned[room]["assigned"], self.assigned[room]["current"],
                   self.assigned[room]["remaining"], self.assigned[room]["max_capacity"]] for room in self.assigned]

        result.sort(key=lambda x: x[0], reverse=False)

        self.table1.setRowCount(0)
        # This command resets the table , thus whenever u run the program you wont get duplicate data
        for row_number, row_data in enumerate(result):
            self.table1.insertRow(row_number)
            # This inserts an empty row in the window
            for column_number, data in enumerate(row_data):
                # row_data is a tuple where each element of tuple is a column item
                item = QTableWidgetItem(str(data))

                item.setBackground(QColor("antiquewhite"))
                item.setForeground(QColor("black"))  # Set text color to purple



                self.table1.setItem(row_number, column_number, item)

    def load_not_allocated(self):


        self.table2.setColumnCount(3)
        # Use a list comprehension to create sublists
        result = [self.not_allocated[i:i + 3] for i in
                  range(0, len(self.not_allocated), 3)]

        self.table2.setRowCount(0)
        # This command resets the table , thus whenever u run the program you wont get duplicate data
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            # This inserts an empty row in the window
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setBackground(QColor("lightcyan"))
                item.setForeground(QColor("black"))  # Set text color to purple

                self.table2.setItem(row_number, column_number, item)
        self.table2.verticalHeader().setVisible(False)
        #self.table1.horizontalHeader().setVisible(False)



    def cell_clicked_table1(self):
        de_allocate_button = QPushButton("De-Allocate Course")
        de_allocate_button.clicked.connect(self.de_allocate)
        de_allocate_button.setFixedSize(200, 50)
        de_allocate_button.setStyleSheet(Styles().red_push_button())

        # the below steps were taken to avoid duplication of buttons when we click on multiple cells
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        selected_row = self.table1.currentRow()
        if self.table1.item(selected_row, 0).text() != "":
            self.statusbar.addWidget(de_allocate_button)

    def cell_clicked_table2(self):
        allocate_button = QPushButton("Assign Room")
        allocate_button.clicked.connect(self.assign_room)
        allocate_button.setFixedSize(200, 50)
        allocate_button.setStyleSheet(Styles().green_push_button())

        split_button = QPushButton("Split Packet")
        split_button.clicked.connect(self.split_packet)
        split_button.setFixedSize(200, 50)
        split_button.setStyleSheet(Styles().red_push_button())

        merge_button = QPushButton("Merge Packet")
        merge_button.clicked.connect(self.merge_packet)
        merge_button.setFixedSize(200, 50)
        merge_button.setStyleSheet(Styles().blue_push_button())


        # the below steps were taken to avoid duplication of buttons when we click on multiple cells
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        selected_row = self.table2.currentRow()
        if self.table2.item(selected_row, 0).text() != "":
            self.statusbar.addWidget(allocate_button)
            self.statusbar.addWidget(split_button)
            self.statusbar.addWidget(merge_button)


    def de_allocate(self):
        try:
            row = self.table1.currentRow()
            room= self.table1.item(row,0).text()
            courses = self.assigned[room]["assigned"]
            if courses !=[]:
                dialog = DescheduleDialog(courses=courses,room=room,slot= self.slot)
                dialog.exec()

                if dialog.course != None:
                    packet = dialog.course.split("__")
                    self.not_allocated.append(dialog.course)
                    packet[1], packet[2]= int(packet[1]), int(packet[2])
                    self.assigned[room]["assigned"].remove(packet)
                    self.assigned[room]["current"] -= packet[2]
                    self.assigned[room]["remaining"] += packet[2]
                    Seating().write_changes(slot=self.slot,assigned=self.assigned,not_allocated=self.not_allocated)
                    self.load_seating()
                    self.load_not_allocated()
                    ConfirmationWidgets().success(text=f"Course {dialog.course} Deallocated successfully ")


            else:
                ConfirmationWidgets().error(text="Kindly select a valid room")


        except AttributeError:  # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a cell")

    def assign_room(self):
        try:
            packet_item = self.table2.currentItem().text()

            if packet_item != "":
                first_column_data = [
                    self.table1.item(row, 0).text() if self.table1.item(row, 0) else ""
                    for row in range(self.table1.rowCount())
                ]

                dialog = AssignDialog(rooms=first_column_data, packet_item=packet_item)
                dialog.exec()

                if dialog.room != None:
                    packet = packet_item.split("__")
                    packet[1], packet[2] = int(packet[1]), int(packet[2])
                    packet_size = packet[2]
                    remaining = self.assigned[dialog.room]["remaining"]

                    if packet_size > remaining:
                        ConfirmationWidgets().error(text="Insufficient capacity")
                    else:
                        self.not_allocated.remove(packet_item)

                        merge_with=None
                        for c,i,s in self.assigned[dialog.room]["assigned"]:
                            if c == packet[0]:
                                merge_with = [c,i,s]
                                break

                        if merge_with:
                            c, i, s = merge_with
                            self.assigned[dialog.room]["assigned"].remove([c,i,s])
                            s += packet_size # merged
                            self.assigned[dialog.room]["assigned"].append([c,i,s])
                            self.packet_ids[c].remove(packet[1]) # merge kar rahe hai

                        else:
                            self.assigned[dialog.room]["assigned"].append(packet)


                        self.assigned[dialog.room]["current"] += packet_size
                        self.assigned[dialog.room]["remaining"] -= packet_size

                        Seating().write_changes(slot=self.slot,assigned=self.assigned,not_allocated=self.not_allocated)
                        self.load_seating()
                        self.load_not_allocated()
                        ConfirmationWidgets().success(text=f"Course {packet_item} assigned room {dialog.room} successfully ")

            else:
                ConfirmationWidgets().error(text="Kindly select a valid cell")


        except AttributeError:  # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a valid cell")

    def split_packet(self):
        try:
            packet_item = self.table2.currentItem().text()
            course = packet_item.split("__")[0]
            dialog = SplitDialog( packet_item=packet_item,packet_id_list=self.packet_ids[course])
            dialog.exec()

            if dialog.split:
                split_id = dialog.split_id
                split_size = dialog.split_size
                self.not_allocated.remove(packet_item)

                packet = packet_item.split("__")
                packet[1],packet[2] = int(packet[1]), int(packet[2])
                packet[2] -= split_size

                new_item1 = f"{course}__{packet[1]}__{packet[2]}"
                new_item2 = f"{course}__{split_id}__{split_size}"
                self.not_allocated.append(new_item1)
                self.not_allocated.append(new_item2)
                self.packet_ids[course].append(split_id)
                Seating().update_not_allocated(slot=self.slot,not_allocated=self.not_allocated)
                self.load_not_allocated()
                ConfirmationWidgets().success(text="New packet created successfully")


            
        except AttributeError:  # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a valid cell")

    def merge_packet(self):
        try:
            packet_item = self.table2.currentItem().text()
            course, packet_id, packet_size = packet_item.split("__")

            merge_options = []

            for item in self.not_allocated:
                item_course,item_id,item_size = item.split("__")
                if item_course == course and item_id != packet_id:
                    merge_options.append(item)

            if len(merge_options) > 0:
                dialog = MergeDialog(merge_options=merge_options,packet_item=packet_item)
                dialog.exec()

                if dialog.merge:
                    c , merge_id,merge_packet_size = dialog.merge_packet.split("__")
                    self.not_allocated.remove(packet_item)
                    self.not_allocated.remove(dialog.merge_packet)
                    self.packet_ids[course].remove(int(packet_id))


                    new_item = f"{course}__{merge_id}__{int(packet_size) + int(merge_packet_size)}"
                    self.not_allocated.append(new_item)

                    Seating().update_not_allocated(slot=self.slot, not_allocated=self.not_allocated)
                    self.load_not_allocated()
                    ConfirmationWidgets().success(text="packet merged created successfully")
            else:
                ConfirmationWidgets().error(text = "No merge options found.")


        except AttributeError:  # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a valid cell")

    def export(self):
        # ensures all students have seats assigned
        if len(self.not_allocated) == 0:
            SeatingPlan(slot=self.slot,assigned=self.assigned,autoprint_flag=False)
        else:
            ConfirmationWidgets().error(text = "Kindly assign rooms to all the packets first.")


    def back_to_homepage(self):
        self.back_button_clicked=True
        self.back_to_homepage_signal.emit()
        self.close()

    def closeEvent(self, event):
        #if not self.back_button_clicked: # means top right x was clicked
        #    Users().reset_login_flag(emp_code=self.logged_in_user)
        super().closeEvent(event)

class DescheduleDialog(QDialog):
    def __init__(self,courses,room,slot):
        try:
            super().__init__()
            self.slot = slot
            self.room = room
            self.course = None
            course_lst = [ c[0] + "__" + str(c[1]) + "__" + str(c[2]) for c in courses]
            self.setWindowTitle("De-Allocate Course")
            self.setFixedWidth(300)
            self.setFixedHeight(300)



            layout = QVBoxLayout()  # places widgets only vertically stacked as opposed to grid #

            label= QLabel(f"Room : {room}")
            label.setStyleSheet("font-weight: bold;")

            layout.addWidget(label)
            label.setFixedHeight(20)

            #  courses drop down list
            self.courses = QComboBox()
            self.courses.addItems(course_lst)
            layout.addWidget(self.courses)

            # update button
            button = QPushButton("Submit")
            button.clicked.connect(self.Deschedule)
            layout.addWidget(button)

            button2 = QPushButton("Cancel")
            button2.clicked.connect(self.close)
            layout.addWidget(button2)

            self.setLayout(layout)
        except AttributeError:
            pass

    def Deschedule(self):
        self.course = self.courses.itemText(self.courses.currentIndex())
        # self.course set to non None value only when submit button is clicked
        self.close()

class AssignDialog(QDialog):
    def __init__(self,packet_item,rooms):
        try:
            super().__init__()

            self.room = None
            self.setWindowTitle("Assign Room")
            self.setFixedWidth(300)
            self.setFixedHeight(300)

            layout = QVBoxLayout()  # places widgets only vertically stacked as opposed to grid #

            label= QLabel(f"Assign : {packet_item}")
            label.setStyleSheet("font-weight: bold;")

            layout.addWidget(label)
            label.setFixedHeight(20)

            #  courses drop down list
            self.room_dropdown = QComboBox()
            self.room_dropdown.addItems(rooms)
            layout.addWidget(self.room_dropdown)

            # update button
            button = QPushButton("Submit")
            button.clicked.connect(self.assign_trigger)
            layout.addWidget(button)

            button2 = QPushButton("Cancel")
            button2.clicked.connect(self.close)
            layout.addWidget(button2)

            self.setLayout(layout)
        except AttributeError:
            pass

    def assign_trigger(self):
        self.room = self.room_dropdown.itemText(self.room_dropdown.currentIndex())
        # self.course set to non None value only when submit button is clicked
        self.close()

class SplitDialog(QDialog):
    def __init__(self,packet_item,packet_id_list):
        try:
            super().__init__()

            self.split = False
            self.split_id = None
            self.split_size = None

            self.course,self.packet_id,self.packet_size = packet_item.split("__")
            self.packet_id,self.packet_size = int(self.packet_id), int(self.packet_size)
            self.id_list = packet_id_list
            self.setWindowTitle("Split Packet")
            self.setFixedWidth(300)
            self.setFixedHeight(300)

            layout = QVBoxLayout()  # places widgets only vertically stacked as opposed to grid #

            label= QLabel(f"Split : {packet_item}")
            label.setStyleSheet("font-weight: bold;")

            layout.addWidget(label)
            label.setFixedHeight(20)

            #  courses drop down list
            layout.addWidget(QLabel("Enter size of the new packet:"))
            self.split_size_edit = QLineEdit()
            self.split_size_edit.setToolTip("Enter an Integer")
            layout.addWidget(self.split_size_edit)

            # update button
            button = QPushButton("Submit")
            button.clicked.connect(self.split_trigger)
            layout.addWidget(button)

            button2 = QPushButton("Cancel")
            button2.clicked.connect(self.close)
            layout.addWidget(button2)

            self.setLayout(layout)
        except AttributeError:
            pass

    def split_trigger(self):
        try:
            self.split_size = int(self.split_size_edit.text())
            if self.split_size >= self.packet_size or self.split_size<1:
                ConfirmationWidgets().error(text="Kindly enter a valid integer")

            else:
                self.split = True
                #i = len(self.id_list)+1
                i=1
                while i in self.id_list:
                    i+=1

                self.split_id = i

                self.close()
        except ValueError:
            ConfirmationWidgets().error(text="Kindly enter a valid integer")

class MergeDialog(QDialog):
    def __init__(self,merge_options,packet_item):
        try:
            super().__init__()

            self.merge = False
            self.merge_packet = None

            self.setWindowTitle("Merge Packet")
            #self.setFixedWidth(300)
            self.setFixedHeight(300)

            layout = QVBoxLayout()  # places widgets only vertically stacked as opposed to grid #
            label = QLabel(f"Choose the packet with which {packet_item} will be merged")
            label.setStyleSheet("font-weight: bold;")

            layout.addWidget(label)
            label.setFixedHeight(20)

            self.option_dropdown = QComboBox()
            self.option_dropdown.addItems(merge_options)
            layout.addWidget(self.option_dropdown)

            # update button
            button = QPushButton("Submit")
            button.clicked.connect(self.merge_trigger)
            layout.addWidget(button)

            button2 = QPushButton("Cancel")
            button2.clicked.connect(self.close)
            layout.addWidget(button2)

            self.setLayout(layout)
        except AttributeError:
            pass

    def merge_trigger(self):
        self.merge = True
        self.merge_packet = self.option_dropdown.itemText(self.option_dropdown.currentIndex())
        # self.course set to non None value only when submit button is clicked
        self.close()

