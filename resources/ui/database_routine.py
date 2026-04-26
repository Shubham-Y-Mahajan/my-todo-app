import json
import sqlite3
from datetime import datetime

#import backend
class DatabaseConnection():
    def __init__(self):
        self.db_filepath= "Data.db"


    def connect(self):
        connection = sqlite3.connect(self.db_filepath)
        return connection

class SeatingConstraints():
    def __init__(self):
        self.connection = DatabaseConnection().connect()



    def toggle_seating_mode(self,new):
        cursor = self.connection.cursor()

        query = f"UPDATE seating_constraints SET courses_per_room = '{new}' "

        cursor.execute(query)

        self.connection.commit()

        cursor.close()
        self.connection.close()

        return True

    def fetch_settings(self):
        cursor = self.connection.cursor()

        query = f"SELECT courses_per_room from seating_constraints  "

        cursor.execute(query)

        row = cursor.fetchone()

        return row[0]

class SeatingRooms():
    def __init__(self):
        self.connection = DatabaseConnection().connect()

    def load_json_file(self):
        with open("seating_input.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def json_to_db(self):
        total_capacity = 0
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM seating_rooms")

        try:
            data = self.load_json_file()

            for room in data:
                room_data = data[room]
                seating_list = room_data["seating"]

                # ✅ Validation: check seating total equals capacity_1
                seating_sum = sum(count for _, count in seating_list)

                if seating_sum < room_data["max_capacity"] or seating_sum//2 < room_data["capacity_1"]:
                    raise ValueError(
                        f"Seating total mismatch in room '{room}': "
                        f"expected {room_data['max_capacity']}, got {seating_sum}"
                    )

                # Prepare and insert the row
                entry = [
                    room,
                    room_data["capacity_1"],
                    room_data["capacity_2"],
                    room_data["max_capacity"],
                    json.dumps(seating_list),
                    1
                ]

                cursor.execute(
                    "INSERT INTO seating_rooms VALUES (?,?,?,?,?,?)", entry
                )

                total_capacity += room_data["capacity_1"]

            self.connection.commit()
            cursor.close()
            self.connection.close()
            return total_capacity

        except Exception as e:
            cursor.close()
            self.connection.close()
            return e

    def fetch_rooms(self):
        cursor=self.connection.cursor()
        courses_per_room= SeatingConstraints().fetch_settings()

        query = f"SELECT name,capacity_1,capacity_2 FROM seating_rooms WHERE availability = 1 "

        cursor.execute(query)

        rows = cursor.fetchall()

        output = {}
        for room in rows:
            name=room[0]
            capacity_1 =room[1]
            capacity_2 = room[2]
            if courses_per_room == 1:

                output[name] ={"max_capacity":capacity_1}
                output[name]["current"] =0
                output[name]["remaining"] = capacity_1
                output[name]["assigned"] = []

            else:
                name1 = name + "__1"
                name2 = name + "__2"
                output[name1] = {"max_capacity": capacity_2}
                output[name1]["current"] = 0
                output[name1]["remaining"] = capacity_2
                output[name1]["assigned"] = []

                output[name2] = {"max_capacity": capacity_2}
                output[name2]["current"] = 0
                output[name2]["remaining"] = capacity_2
                output[name2]["assigned"] = []

        sorted_dict = dict(sorted(output.items(), key=lambda x: x[1]['remaining'], reverse=False)) # ascending

        cursor.close()
        self.connection.close()

        return sorted_dict

    def fetch_room_seats(self):
        cursor = self.connection.cursor()

        query = f"SELECT name,seating FROM seating_rooms WHERE availability = 1 "

        cursor.execute(query)

        rows = cursor.fetchall()
        output = {}
        for row in rows:
            name = row[0]
            pattern = json.loads(row[1])
            output[name] = pattern

        cursor.close()
        self.connection.close()

        return output


class ExamSchedule():
    def __init__(self):

        self.connection = DatabaseConnection().connect()

    def load_course_data(self):
        cursor = self.connection.cursor()

        query = f"SELECT course_code,registered_students,total_students FROM course_data  "

        cursor.execute(query)

        rows = cursor.fetchall()
        course_data={}
        for row in rows:
            code=row[0]
            students=json.loads(row[1])
            total_students=row[2]

            course_data[code] = {"students":students,"total_students":total_students}


        return course_data

    def fetch_exam_slot_courses(self, slot):
        cursor = self.connection.cursor()

        query = f"SELECT courses FROM exam_schedule WHERE slot = '{slot}' "

        cursor.execute(query)

        rows = cursor.fetchone()

        cursor.close()
        self.connection.close()

        return json.loads(rows[0])


    def fetch_exam_slot_course_items(self,slot):
        slot_courses = ExamSchedule().fetch_exam_slot_courses(slot = slot)
        cursor = self.connection.cursor()
        course_data = {}
        for course_code in slot_courses:
            query = f"SELECT registered_students,total_students FROM course_data WHERE course_code = '{course_code}' "

            cursor.execute(query)

            row = cursor.fetchone()

            students = json.loads(row[0])
            students.sort()
            total_students = row[1]

            course_data[course_code] = {"yet_to_assign": students, "remaining": total_students}

        return course_data


    def load_exam_packets(self,course_data):
        cursor = self.connection.cursor()

        query = f"SELECT slot,courses,total_students FROM exam_schedule  "

        cursor.execute(query)

        rows = cursor.fetchall()


        packets = {}
        for slot_data in rows:
            slot = slot_data[0]
            courses=json.loads(slot_data[1])
            packets[slot] = []
            for course in courses:
                packets[slot].append([course,1,course_data[course]['total_students']])

            packets[slot].sort(key=lambda x:x[2],reverse=True)



        cursor.close()
        self.connection.close()

        return packets

    def fetch_slots(self):
        cursor = self.connection.cursor()

        query = f"SELECT slot FROM exam_schedule  "

        cursor.execute(query)

        rows = cursor.fetchall()


        slots = [row[0] for row in rows]

        cursor.close()
        self.connection.close()
        return slots



class Seating():
    def __init__(self):
        self.connection = DatabaseConnection().connect()

    def autorun_write(self,assigned_rooms,not_allocated):
        cursor = self.connection.cursor()

        query = f"SELECT slot FROM exam_schedule  "

        cursor.execute(query)

        rows = cursor.fetchall()
        slots = [row[0] for row in rows]
        try:
            cursor.execute("DELETE FROM seating")
            for slot in slots:
                entry = []
                rooms = assigned_rooms[slot]
                not_assigned = not_allocated[slot]

                entry.append(slot)
                entry.append(json.dumps(rooms))
                entry.append(json.dumps(not_assigned))

                cursor.execute(f"INSERT INTO seating VALUES(?,?,?)", entry)

            self.connection.commit()
        except Exception as e:
            print(e)


        cursor.close()
        self.connection.close()



    def fetch_seating(self,slot):
        cursor = self.connection.cursor()

        query = f"SELECT rooms,not_allocated FROM seating WHERE slot = '{slot}'  "

        cursor.execute(query)

        row = cursor.fetchone()

        assigned= json.loads(row[0])
        not_allocated = json.loads(row[1])

        cursor.close()
        self.connection.close()

        return [assigned,not_allocated]

    def write_changes(self,slot,assigned,not_allocated):
        cursor = self.connection.cursor()
        rooms = json.dumps(assigned)
        na = json.dumps(not_allocated)
        query = f"UPDATE seating SET rooms = '{rooms}' , not_allocated = '{na}' WHERE slot = '{slot}' "

        cursor.execute(query)

        self.connection.commit()

        cursor.close()
        self.connection.close()

        return True

    def update_not_allocated(self,slot,not_allocated):
        cursor = self.connection.cursor()

        na = json.dumps(not_allocated)
        query = f"UPDATE seating SET not_allocated = '{na}' WHERE slot = '{slot}' "

        cursor.execute(query)

        self.connection.commit()

        cursor.close()
        self.connection.close()

        return True


class ExamDateTime():
    def __init__(self):
        self.connection = DatabaseConnection().connect()

    def refresh_dates(self):
        cursor = self.connection.cursor()

        query = f"SELECT slot FROM exam_schedule  "

        cursor.execute(query)

        rows = cursor.fetchall()
        slots = [row[0] for row in rows]
        try:
            cursor.execute("DELETE FROM exam_datetime")
            for slot in slots:
                entry = []

                entry.append(slot)
                entry.append("")
                entry.append("")

                cursor.execute(f"INSERT INTO exam_datetime VALUES(?,?,?)", entry)

            self.connection.commit()
        except Exception as e:
            print(e)

        cursor.close()
        self.connection.close()

    def fetch_dates(self):
        cursor = self.connection.cursor()

        query = f"SELECT slot,date,time FROM exam_datetime  "

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        self.connection.close()

        return rows

    def fetch_slot_datetime(self,slot):
        cursor = self.connection.cursor()

        query = f"SELECT date,time FROM exam_datetime WHERE slot = '{slot}' "

        cursor.execute(query)

        row = cursor.fetchone()

        cursor.close()
        self.connection.close()

        return row


    def update_date(self,slot,value):
        cursor = self.connection.cursor()

        update_query = f"UPDATE exam_datetime SET date = ? WHERE slot = ? "
        cursor.execute(update_query, (value, slot))

        self.connection.commit()

        cursor.close()
        self.connection.close()

    def update_time(self,slot,value):
        cursor = self.connection.cursor()

        update_query = f"UPDATE exam_datetime SET time = ? WHERE slot = ? "
        cursor.execute(update_query, (value, slot))

        self.connection.commit()

        cursor.close()
        self.connection.close()



if __name__ == "__main__":
    print(ExamDateTime().fetch_slot_datetime(slot= '12'))

