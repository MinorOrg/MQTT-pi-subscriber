import os
import sqlite3

# set up database connection
conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

# create table for data
c.execute('''CREATE TABLE IF NOT EXISTS wifi_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             distance_from_esp1 FLOAT,
             distance_from_esp2 FLOAT,
             distance_from_esp3 FLOAT,
             rssi_esp1 FLOAT,
             rssi_esp2 FLOAT,
             rssi_esp3 FLOAT)''')

# iterate over all files in directory
directory = './datas'
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        # extract distance data from filename
        distances = filename.split('.t')[0].split('x')
        distance_from_esp1 = float(distances[0])
        distance_from_esp2 = float(distances[1])
        distance_from_esp3 = float(distances[2])
        
        with open(os.path.join(directory, filename), 'r') as file:
            rssi_esp1 = None
            rssi_esp2 = None
            rssi_esp3 = None
            for line in file:
                if 'esp1rssi' in line:
                    rssi_esp1 = float(line.split(' ')[1])
                elif 'esp2rssi' in line:
                    rssi_esp2 = float(line.split(' ')[1])
                elif 'esp3rssi' in line:
                    rssi_esp3 = float(line.split(' ')[1])
            
            # insert data into table
            c.execute("INSERT INTO wifi_data (distance_from_esp1, distance_from_esp2, distance_from_esp3, rssi_esp1, rssi_esp2, rssi_esp3) VALUES (?, ?, ?, ?, ?, ?)", (distance_from_esp1, distance_from_esp2, distance_from_esp3, rssi_esp1, rssi_esp2, rssi_esp3))
            conn.commit()

# close database connection
conn.close()
