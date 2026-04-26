from database_routine import ExamSchedule,SeatingRooms,Seating, SeatingConstraints
import copy
import os
from collections import defaultdict
#from fpdf import FPDF
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import heapq
import shutil
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from datetime import datetime
#import xlsxwriter
from pdf_operations import PdfOperations
import random


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
class Allocation():
    def __init__(self):
        self.course_data = ExamSchedule().load_course_data()
        self.packet_data = ExamSchedule().load_exam_packets(course_data=self.course_data)
        # load_exam_packets ensures all the students are counted
        self.rooms = SeatingRooms().fetch_rooms()
        self.courses_per_room = SeatingConstraints().fetch_settings()
        self.assign_rooms()

    def assign_rooms(self):
        assigned_rooms  = {}
        not_allocated = {}
        room_course_pairs = set()
        for slot in self.packet_data:

            room_course_pairs.clear()
            packets = self.packet_data[slot]
            """
            print(slot)
            print(packets)
            """

            # Use deepcopy to create a completely independent copy of self.rooms
            assigned_rooms[slot] = copy.deepcopy(self.rooms)
            # creatinga shallow copy will lead to same access for the inner dictionaries
            rooms_dict = assigned_rooms[slot]
            not_allocated[slot] = []
            rooms=[]
            for room in rooms_dict:
                rooms.append([room,rooms_dict[room]["remaining"]])



            need_to_split=[]
            #print(packets)
            for course,packet_id,packet_size in packets:
                check = False


                for i in range(len(rooms)):
                    room_name,remaining = rooms[i][0],rooms[i][1]
                    if len(rooms_dict[room_name]["assigned"]) > 0 or \
                            (room_name.split("__")[0], course) in room_course_pairs:
                        continue
                    if packet_size<=remaining:
                        rooms_dict[room_name]["assigned"].append([course,packet_id,packet_size])
                        rooms_dict[room_name]["current"] += packet_size
                        rooms_dict[room_name]["remaining"] -= packet_size
                        rooms[i][1] -= packet_size
                        room_course_pairs.add((room_name.split("__")[0], course))
                        check = True
                        break

                if not check:
                    need_to_split.append([course,packet_id,packet_size])


            need_to_split.sort(key=lambda x: x[2], reverse=True)
            second_last_pass = []
            for course,packet_id,packet_size in need_to_split:
                rooms.sort(key=lambda x: x[1], reverse=False) # ascending
                check = False
                for i in range(len(rooms)):
                    r1, r1_name = rooms[i][1], rooms[i][0]
                    if len(rooms_dict[r1_name]["assigned"]) > 0 or (r1_name.split("__")[0], course) in room_course_pairs:
                        continue

                    for j in range(i+1,len(rooms)):
                        r2_name, r2 = rooms[j][0], rooms[j][1]
                        if len(rooms_dict[r2_name]["assigned"]) > 0 or (r2_name.split("__")[0], course) in room_course_pairs \
                                or r2_name.split("__")[0] == r1_name.split("__")[0]:
                            continue

                        if r1+r2>= packet_size:

                            size1 , size2 = r1,abs(packet_size-r1)
                            part1=[course,packet_id,size1]
                            part2 =[course,packet_id + 1,size2]

                            check = True

                            rooms_dict[r1_name]["assigned"].append(part1)
                            rooms_dict[r1_name]["current"] += size1
                            rooms_dict[r1_name]["remaining"] -= size1
                            rooms[i][1] -= size1

                            rooms_dict[r2_name]["assigned"].append(part2)
                            rooms_dict[r2_name]["current"] += size2
                            rooms_dict[r2_name]["remaining"] -= size2
                            rooms[j][1] -= size2

                            room_course_pairs.add((r1_name.split("__")[0], course))
                            room_course_pairs.add((r2_name.split("__")[0], course))

                            break

                    if check:
                        break

                if not check:
                    second_last_pass.append([course,packet_id,packet_size])

            rooms.sort(key=lambda x: x[1], reverse=True)
            second_last_pass.sort(key=lambda x: x[2], reverse=True)
            last_pass = []
            for course,packet_id,packet_size in second_last_pass:
                rooms.sort(key=lambda x: x[1], reverse=True)
                to_assign = packet_size
                cursor = packet_id
                check = False
                for i in range(len(rooms)):
                    room_name, capacity = rooms[i][0], rooms[i][1]
                    if len(rooms_dict[room_name]["assigned"]) > 0 or \
                            (room_name.split("__")[0], course) in room_course_pairs:
                        continue
                    if capacity < to_assign and capacity > 0:
                        rooms_dict[room_name]["assigned"].append([course, cursor, capacity])
                        rooms_dict[room_name]["current"] += capacity
                        rooms_dict[room_name]["remaining"] -= capacity
                        rooms[i][1] -= capacity
                        cursor+=1
                        to_assign-=capacity
                        room_course_pairs.add((room_name.split("__")[0], course))
                    elif to_assign<=capacity:
                        rooms_dict[room_name]["assigned"].append([course, cursor, to_assign])
                        rooms_dict[room_name]["current"] += to_assign
                        rooms_dict[room_name]["remaining"] -= to_assign
                        rooms[i][1] -= to_assign
                        cursor += 1
                        to_assign -= to_assign
                        room_course_pairs.add((room_name.split("__")[0], course))
                        check = True
                        break

                if not check:
                    last_pass.append([course, cursor, to_assign])



            not_scheduled = not_allocated[slot]
            rooms.sort(key=lambda x: x[1], reverse=True)
            last_pass.sort(key=lambda x: x[2], reverse=True)

            for course, packet_id, packet_size in last_pass:
                rooms.sort(key=lambda x: x[1], reverse=True)
                to_assign = packet_size
                cursor = packet_id
                check = False
                for i in range(len(rooms)):

                    room_name, capacity = rooms[i][0], rooms[i][1]
                    if (room_name.split("__")[0], course) in room_course_pairs:
                        continue
                    if capacity < to_assign and capacity > 0:
                        rooms_dict[room_name]["assigned"].append([course, cursor, capacity])
                        rooms_dict[room_name]["current"] += capacity
                        rooms_dict[room_name]["remaining"] -= capacity
                        rooms[i][1] -= capacity
                        cursor += 1
                        to_assign -= capacity
                        room_course_pairs.add((room_name.split("__")[0], course))
                    elif to_assign <= capacity:
                        rooms_dict[room_name]["assigned"].append([course, cursor, to_assign])
                        rooms_dict[room_name]["current"] += to_assign
                        rooms_dict[room_name]["remaining"] -= to_assign
                        rooms[i][1] -= to_assign
                        cursor += 1
                        to_assign -= to_assign
                        room_course_pairs.add((room_name.split("__")[0], course))
                        check = True
                        break

                if not check:
                    not_scheduled.append(f"{course}__{cursor}__{to_assign}")
                    # not_scheduled ensures no student is missed





            """print(not_scheduled)
            print(rooms)
            print(rooms_dict)
            print("")"""




            if self.courses_per_room == 2:
                actual_dict={}
                actual_rooms =list(set(room.split("__")[0] for room,remaining in rooms))
                for room in actual_rooms:
                    actual_dict[room] ={'max_capacity': 0, 'current': 0, 'remaining': 0, 'assigned': []}


                for room in rooms_dict:
                    name = room.split("__")[0]
                    actual_dict[name]['max_capacity'] += rooms_dict[room]['max_capacity']
                    actual_dict[name]['current'] += rooms_dict[room]['current']
                    actual_dict[name]['remaining'] += rooms_dict[room]['remaining']
                    actual_dict[name]['assigned'] += rooms_dict[room]['assigned']

                assigned_rooms[slot] = actual_dict
                """
                print(actual_dict)
                print("")
                """


        Seating().autorun_write(assigned_rooms=assigned_rooms,not_allocated=not_allocated)

class SeatingPlan():
    def __init__(self,slot,assigned,autoprint_flag):
        self.slot = slot
        self.assigned = assigned
        self.autoprint_flag = autoprint_flag
        self.exam_slot_courses = ExamSchedule().fetch_exam_slot_course_items(slot=self.slot)

        self.course_wise_plan = defaultdict(lambda: defaultdict(dict)) # for nested dicts lambda used


        for room in self.assigned:
            for packet in self.assigned[room]["assigned"]:
                course,packet_id,packet_size = packet
                students = self.exam_slot_courses[course]["yet_to_assign"][:packet_size]
                self.exam_slot_courses[course]["yet_to_assign"] = self.exam_slot_courses[course]["yet_to_assign"][packet_size:]
                self.exam_slot_courses[course]["remaining"] -= packet_size
                self.course_wise_plan[course][room]["remaining"] = students
                self.course_wise_plan[course][room]["mapped"] = []


        #print(self.exam_slot_courses)
        #print(self.course_wise_plan['MAL100/IC153/IC202']['L205'])

        for course in self.exam_slot_courses:
            if self.exam_slot_courses[course]["yet_to_assign"] !=[] or self.exam_slot_courses[course]["remaining"] !=0:
                ConfirmationWidgets().error(text="An unexpected error has occurred. \n"
                                                 "This plan was unable to capture all the students of the exam slot.\n"
                                                 "if this error persists, kindly contact the developer at +918879466601, "
                                                 "shubhamy0023@gmail.com")


        room_seats= SeatingRooms().fetch_room_seats()

        for room in self.assigned:
            heap = []
            backup_seats = []
            for course,pid,psize in self.assigned[room]["assigned"]:
                heapq.heappush(heap,[-1*psize, course])

            cache = []
            while heap:

                remaining,course = heapq.heappop(heap)
                remaining *= -1

                if cache:
                    heapq.heappush(heap,cache)
                    cache = []

                students = self.course_wise_plan[course][room]["remaining"]
                mapping = self.course_wise_plan[course][room]["mapped"]

                if len(room_seats[room]) > 0:
                    row, n = room_seats[room].pop(0)
                    for i in range(1,n,2):
                        if remaining != 0:
                            s_id = students.pop(0)
                            mapping.append([s_id, row , i])
                            remaining-=1
                        else:
                            backup_seats.append([row,i])

                    if remaining > 0:
                        cache = [remaining*-1 , course]

                else:
                    while remaining:
                        r,j = backup_seats.pop(0)
                        s_id = students.pop(0)
                        mapping.append([s_id, r, j])
                        remaining -= 1



            # jab ek hi course hoga room me toh ek row ke baad sab cache se hi allot hoga
            if cache:
                remaining, course = cache
                remaining *= -1
                students = self.course_wise_plan[course][room]["remaining"]
                mapping = self.course_wise_plan[course][room]["mapped"]

                while remaining:
                    if len(room_seats[room]) > 0:
                        row, n = room_seats[room].pop(0)
                        for i in range(1, n, 2):
                            s_id = students.pop(0)
                            mapping.append([s_id, row, i])
                            remaining -= 1
                            if remaining == 0:
                                break
                    else:
                        # This will raise an indexError if there is a seat count and seat list mismatch
                        r, j = backup_seats.pop(0)
                        s_id = students.pop(0)
                        mapping.append([s_id, r, j])
                        remaining -= 1



        for course in self.course_wise_plan:
            for room in self.course_wise_plan[course]:
                if len(self.course_wise_plan[course][room]["remaining"]) > 0:
                    ConfirmationWidgets().error(text = f"CRITICAL ERROR \n"
                                                       f" {course}, {room}, {self.course_wise_plan[course][room]['remaining']}\n"
                                                       f"if this error persists, kindly contact the developer at +918879466601, "
                                                       f"shubhamy0023@gmail.com")


        #print(self.course_wise_plan)

        def shuffle_exam_seating(seating_plan, seed=None):
            """
            Shuffles seat assignments (row + seat number) within each room.

            Args:
                seating_plan: dict in the form {course: {room: {"mapped": [[roll, row, num], ...]}}}
                seed: optional int to make results reproducible (e.g., for debugging)
            """
            if seed is not None:
                random.seed(seed)

            for course, rooms in seating_plan.items():
                for room, details in rooms.items():
                    mapped = details.get('mapped', [])

                    # extract seat positions ('A', 1)
                    seat_positions = [(row, num) for _, row, num in mapped]

                    # shuffle seat positions
                    random.shuffle(seat_positions)

                    # reassign shuffled seats to the same roll numbers
                    for i, (row, num) in enumerate(seat_positions):
                        mapped[i][1], mapped[i][2] = row, num

            return seating_plan

        final_seating_plan = shuffle_exam_seating(self.course_wise_plan)
        #final_seating_plan = self.course_wise_plan

        try:
            PdfOperations(data = final_seating_plan, slot = self.slot).generate_seating_pdf()
            if not self.autoprint_flag:
                ConfirmationWidgets().success(text="PDFs generated successfully")
        except OSError:
            ConfirmationWidgets().error(text=f"Invalid filename - slot {self.slot},\n "
                                             f"ensure that the 'time field' OR 'room name' "
                                             f"doesn't contain the below symbols:\n"
                                             "( / | \ * ? \" < > )")






























if __name__ == "__main__":
    plan = SeatingPlan(slot=12,assigned=None)



