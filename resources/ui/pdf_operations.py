import os

from PyQt6.QtWidgets import QMessageBox
from fpdf import FPDF
import csv

from database_routine import ExamDateTime


def load_student_names(csv_file):
    student_name = {}

    with open(csv_file, mode='r', encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Safely skip header if present

        for line in reader:
            # Skip completely blank rows
            if not any(cell.strip() for cell in line):
                continue

            # Take only the first 2 columns (ignore extras)
            cleaned = [cell.strip() for cell in line[:2]]

            # Ensure we have both enrollment number and name
            if len(cleaned) < 2 or any(c == "" for c in cleaned):
                continue

            enrollment_no, student_name_value = cleaned
            student_name[enrollment_no] = student_name_value

    return student_name


class ConfirmationWidgets(): # every page uses this except login and signup ( they have their own)
    def success(self,text):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText(text)
        confirmation_widget.exec()

    def error(self,text):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Error")
        confirmation_widget.setText(text)
        confirmation_widget.exec()

    def warning(self,text):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Warning")
        confirmation_widget.setText(text)
        confirmation_widget.exec()

class PdfOperations():
    def __init__(self,slot,data):
        self.slot= slot
        self.data = data
        self.student_names = load_student_names(csv_file="student_name_input.csv")
        date,time = ExamDateTime().fetch_slot_datetime(slot=self.slot)
        self.date = date.strip()
        self.time = time.strip()


    def generate_seating_pdf(self):
        dir_path = f"SEATING_PLANNER_OUTPUT/{self.slot}"  # Define directory path

        elements = self.time.split(":")
        filename_time = "-".join(elements)
        filename = f"{dir_path}/seating_plan_{self.date}_{filename_time}.pdf"
        os.makedirs(dir_path, exist_ok=True)  # Create directories if they don't exist

        data = self.data
        #print(data.keys())
        #print(data)

        pdf = FPDF(format='A4')
        pdf.set_auto_page_break(auto=True, margin=7) # 290 y pe auto break
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)

        columns_per_row = 5  # Number of ID-seat pairs per row


        cell_height = 5
        id_cell_width = 25
        seat_cell_width = 12
        vertical_limit = 260


        colors = [[200, 230, 255],[180, 255, 180],[255, 255, 224]] # blue,green,yellow
        color_cursor = 0
        pdf.add_page()

        for course, rooms in data.items():
            for room, details in rooms.items():
                pdf.set_font("Arial", "B", 10)  # Reduced font size

                if pdf.get_y() > vertical_limit - 10:  # at top of page y = 0 nad range of y = 0 to 297 (x is 0 to 210)
                    pdf.add_page()

                pdf.set_fill_color(255, 182, 193) # light pink hard code
                pdf.ln(7)
                pdf.cell(185, 8, f"{course} - {room}, {self.date}, {self.time}", border=1, ln=True, align='C',fill=True)
                pdf.ln(2)

                # Table Header
                pdf.set_font("Arial", "B", 8)  # Reduced font size for header
                for _ in range(columns_per_row):
                    pdf.cell(id_cell_width, cell_height + 1, "ID Number", border=1, align='C',fill=True)
                    pdf.cell(seat_cell_width, cell_height + 1, "Seat", border=1, align='C',fill= True)
                pdf.ln()

                color_cursor +=1
                i = color_cursor % 3
                pdf.set_fill_color(colors[i][0], colors[i][1], colors[i][2])
                # Table Rows
                pdf.set_font("Arial", "", 7)  # Reduced font size for table content
                row_data = []

                for student in details['mapped']:
                    id_number, row, seat = student
                    row_data.append((id_number, f"{row}{seat}"))

                    if len(row_data) == columns_per_row:
                        if pdf.get_y() > vertical_limit:
                            pdf.cell(0, 8, f"To be continued ...", border=0, ln=True, align='C')
                            pdf.add_page()
                            pdf.cell(0, 8, f"... Continuation", border=0, ln=True, align='C')

                        for pair in row_data:
                            pdf.cell(id_cell_width, cell_height, pair[0], border=1, align='C',fill=True)
                            pdf.cell(seat_cell_width, cell_height, pair[1], border=1, align='C',fill=True)
                        pdf.ln()
                        row_data = []


                # Fill remaining columns in last row if needed
                if row_data:
                    if pdf.get_y() > vertical_limit:
                        pdf.cell(0, 8, f"To be continued ...", border=0, ln=True, align='C')
                        pdf.add_page()
                        pdf.cell(0, 8, f"... Continuation", border=0, ln=True, align='C')

                    for pair in row_data:
                        pdf.cell(id_cell_width, cell_height, pair[0], border=1, align='C',fill=True)
                        pdf.cell(seat_cell_width, cell_height, pair[1], border=1, align='C',fill=True)
                    empty_cells = columns_per_row - len(row_data)
                    for _ in range(empty_cells):
                        pdf.cell(id_cell_width, cell_height, "", border=1,fill=True)
                        pdf.cell(seat_cell_width, cell_height, "", border=1,fill=True)
                    pdf.ln()

                self.generate_attendance_sheet(course=course,room=room)


        pdf.output(filename)


    # will be called per table ?

    def generate_attendance_sheet(self,course, room):
        slot = self.slot
        data = self.data
        course_name_items = course.split("/")
        name = "-".join(course_name_items)
        dir_path = f"SEATING_PLANNER_OUTPUT/{slot}/{room}"  # Define directory path
        filename = f"{dir_path}/attendance_{name}_{room}.pdf"

        number_of_students_assigned = len(data[course][room]['mapped'])
        number_of_students_printed = 0
        os.makedirs(dir_path, exist_ok=True)  # Create directories if they don't exist

        pdf = FPDF(format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)

        page_number = 1
        def add_table_header():
            pdf.set_font("Arial", "B", 10)
            headers = ["ID Number", "Name", "Seat", "Signature 1", "Signature 2"]
            col_widths = [25, 70, 15, 40, 40]
            for header, width in zip(headers, col_widths):
                pdf.cell(width, 8, header, border=1, align='C')
            pdf.ln()
            return col_widths

        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Attendance Sheet for {course} in {room}, {self.date}, {self.time}", ln=True, align='C')
        pdf.ln(5)
        col_widths = add_table_header()

        # Table Rows (1 students per row)
        pdf.set_font("Arial", "", 10)
        row_data = []
        for student in data[course][room]['mapped']:
            id_number, row, seat = student

            try:
                row_data.append((id_number, self.student_names[id_number], f"{row}{seat}", "", ""))
            except KeyError:
                row_data.append((id_number, "Name not found", f"{row}{seat}", "", ""))


            if len(row_data) == 1:  # one students per row
                if pdf.get_y() > 260:  # If near the bottom of the page, add a new page
                    pdf.cell(0, 8, f"To be continued ...", border=0, ln=True, align='C')
                    page_number += 1
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, f"(Page {page_number}) Attendance Sheet for {course} in {room}, "
                                    f"{self.date}, {self.time}", ln=True, align='C')
                    pdf.ln(5)
                    col_widths = add_table_header()
                    pdf.set_font("Arial", "", 10)

                for pair in row_data:
                    for i, width in enumerate(col_widths):
                        pdf.cell(width, 8, pair[i], border=1, align='C')

                    number_of_students_printed += 1

                pdf.ln()
                row_data = []

        # Fill remaining cells if last row is incomplete
        if row_data:
            if pdf.get_y() > 260:
                pdf.cell(0, 8, f"To be continued ...", border=0, ln=True, align='C')
                page_number += 1
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"(Page {page_number}) Attendance Sheet for {course} in {room}, {self.date}, {self.time} ", ln=True, align='C')
                pdf.ln(5)
                col_widths = add_table_header()
                pdf.set_font("Arial", "", 10)

            for pair in row_data:
                for i, width in enumerate(col_widths):
                    pdf.cell(width, 8, pair[i], border=1, align='C')

                number_of_students_printed += 1

            empty_cells = 2 - len(row_data)
            for _ in range(empty_cells):
                for width in col_widths:
                    pdf.cell(width, 8, "", border=1)
            pdf.ln()

        if number_of_students_assigned != number_of_students_printed:
            ConfirmationWidgets().error(text=f"CRITICAL ERROR \n"
                                             f" {course}, {room}, {slot}\n All students could not be printed in the attendance sheet. "
                                             f"If this error persists, kindly contact the developer at +918879466601, "
                                             f"shubhamy0023@gmail.com")

        else:

            pdf.ln(h=10)

            if pdf.get_y() > 270:
                pdf.cell(0, 8, f"To be continued ...", border=0, ln=True, align='C')
                page_number += 1
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"(Page {page_number}) Attendance Sheet for {course} in {room}, {self.date}, {self.time} ",
                         ln=True, align='C')
                pdf.ln(5)
                col_widths = add_table_header()
                pdf.set_font("Arial", "", 10)
            # Set font
            pdf.set_font("Arial", size=10)

            # Define column widths
            col_widths = [50, 50, 50, 40]
            headers = ["Total Number of Students", "Number of Students Present", "Number of Students Absent",
                       "Invigilators Signature"]
            data_row = [str(number_of_students_assigned), "", "", ""]

            # Print table header
            for i in range(len(headers)):
                pdf.cell(col_widths[i], 8, headers[i], border=1, align="C")
            pdf.ln()

            # Print data row
            for i in range(len(data_row)):
                pdf.cell(col_widths[i], 8, data_row[i], border=1, align="C")
            pdf.ln()


            pdf.output(filename)
