import csv
import sqlite3
import json
csv_filepath= "seating_input.csv"
db_filepath= "Data.db"


def csv_to_db(csv_filepath="seating_input.csv", db_filepath="Data.db"):
    data = []
    with open(csv_filepath, newline='') as file:
        reader = csv.reader(file)
        for index, line in enumerate(reader):
            if index == 0:
                continue  # skip header

            # Skip completely blank rows
            if not any(cell.strip() for cell in line):
                continue

            # Take only the first 2 columns safely
            cleaned = [cell.strip() for cell in line[:2]]

            # Ensure both required fields are non-empty
            if len(cleaned) < 2 or any(c == "" for c in cleaned):
                continue

            cleaned.append(1)
            data.append(tuple(cleaned))

    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()

    for entry in data:
        cursor.execute("INSERT INTO seating_rooms VALUES (?,?,?)", entry)

    connection.commit()
    connection.close()



def clear_db(db_filepath= "Data.db"):
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()


    cursor.execute("DELETE FROM seating_rooms")

    connection.commit()
    connection.close()



def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_to_json(new_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4)


def dict_to_json():
    data = {}
    data["L209"] = {"capacity_1":152,"capacity_2":75,"max_capacity":300,
                    "seating":[("A",22),
                               ("B",24),
                               ("C",24),
                               ("D",24),
                               ("E",26),
                               ("F",26),
                               ("G",26),
                               ("H",20),
                               ("I",22),
                               ("J",22),
                               ("K",16),
                               ("L",18),
                               ("M",18),
                               ("N",16)]}

    data["L101"] = {"capacity_1":68,"capacity_2":34,"max_capacity":135,
                    "seating":[("A",16),
                               ("B", 16),
                               ("C", 16),
                               ("D", 16),
                               ("E", 18),
                               ("F", 18),
                               ("G", 18),
                               ("H", 18)]}

    data["L102"] = {"capacity_1": 68, "capacity_2": 34, "max_capacity": 135,
                    "seating": [("A", 16),
                                ("B", 16),
                                ("C", 16),
                                ("D", 16),
                                ("E", 18),
                                ("F", 18),
                                ("G", 18),
                                ("H", 18)]}

    data["L105"] = {"capacity_1": 68, "capacity_2": 34, "max_capacity": 135,
                    "seating": [("A", 16),
                                ("B", 16),
                                ("C", 16),
                                ("D", 16),
                                ("E", 18),
                                ("F", 18),
                                ("G", 18),
                                ("H", 18)]}

    data["L201"] = {"capacity_1": 68, "capacity_2": 34, "max_capacity": 135,
                    "seating": [("A", 16),
                                ("B", 16),
                                ("C", 16),
                                ("D", 16),
                                ("E", 18),
                                ("F", 18),
                                ("G", 18),
                                ("H", 18)]}

    data["L202"] = {"capacity_1": 68, "capacity_2": 34, "max_capacity": 135,
                    "seating": [("A", 16),
                                ("B", 16),
                                ("C", 16),
                                ("D", 16),
                                ("E", 18),
                                ("F", 18),
                                ("G", 18),
                                ("H", 18)]}

    data["L205"] = {"capacity_1": 68, "capacity_2": 34, "max_capacity": 135,
                    "seating": [("A", 16),
                                ("B", 16),
                                ("C", 16),
                                ("D", 16),
                                ("E", 18),
                                ("F", 18),
                                ("G", 18),
                                ("H", 18)]}

    data["L206"] = {"capacity_1": 68, "capacity_2": 34, "max_capacity": 135,
                    "seating": [("A", 16),
                                ("B", 16),
                                ("C", 16),
                                ("D", 16),
                                ("E", 18),
                                ("F", 18),
                                ("G", 18),
                                ("H", 18)]}

    data["L103"] = {"capacity_1": 31, "capacity_2": 15, "max_capacity": 60,
                    "seating": [("A", 10),
                                ("B", 10),
                                ("C", 10),
                                ("D", 10),
                                ("E", 10),
                                ("F", 12)]}

    data["L104"] = {"capacity_1": 31, "capacity_2": 15, "max_capacity": 60,
                    "seating": [("A", 10),
                                ("B", 10),
                                ("C", 10),
                                ("D", 10),
                                ("E", 10),
                                ("F", 12)]}

    data["L203"] = {"capacity_1": 31, "capacity_2": 15, "max_capacity": 60,
                    "seating": [("A", 10),
                                ("B", 10),
                                ("C", 10),
                                ("D", 10),
                                ("E", 10),
                                ("F", 12)]}
    data["L204"] = {"capacity_1": 31, "capacity_2": 15, "max_capacity": 60,
                    "seating": [("A", 10),
                                ("B", 10),
                                ("C", 10),
                                ("D", 10),
                                ("E", 10),
                                ("F", 12)]}
    data["L207"] = {"capacity_1": 31, "capacity_2": 15, "max_capacity": 60,
                    "seating": [("A", 10),
                                ("B", 10),
                                ("C", 10),
                                ("D", 10),
                                ("E", 10),
                                ("F", 12)]}
    data["L208"] = {"capacity_1": 31, "capacity_2": 15, "max_capacity": 60,
                    "seating": [("A", 10),
                                ("B", 10),
                                ("C", 10),
                                ("D", 10),
                                ("E", 10),
                                ("F", 12)]}








    write_to_json(data, 'seating_input.json')

if __name__ == "__main__":
    #clear_db()
    #csv_to_db()
    dict_to_json()
    data= load_json_file("seating_input.json")
    print(data)
