import sqlite3

def calculate_distance(rssi, rssi_distance):
    sorted_rssi_values = sorted(rssi_distance.keys(), reverse=True)
    for i in range(len(sorted_rssi_values) - 1):
        if sorted_rssi_values[i] >= rssi >= sorted_rssi_values[i + 1]:
            # Perform linear interpolation to estimate the distance
            x0 = sorted_rssi_values[i]
            x1 = sorted_rssi_values[i + 1]
            y0 = rssi_distance[x0]
            y1 = rssi_distance[x1]
            distance = y0 + (y1 - y0) * (rssi - x0) / (x1 - x0)
            return distance
        
    # Handle edge cases where RSSI is out of range of the dictionary
    if rssi >= sorted_rssi_values[0]:
        return rssi_distance[sorted_rssi_values[0]]
    elif rssi <= sorted_rssi_values[-1]:
        return rssi_distance[sorted_rssi_values[-1]]
    else:
        raise ValueError("RSSI value out of range of dictionary")


# Connect to the database
conn = sqlite3.connect('mydatabase.db')

# Get a cursor object
cur = conn.cursor()

# Select the two rows you want to calculate the lerp value between
cur.execute("SELECT distance_from_esp1, distance_from_esp2, distance_from_esp3, rssi_esp1, rssi_esp2, rssi_esp3 FROM wifi_data WHERE TRUE")
rows = cur.fetchall()
data_rows=rows[:10]
sample_rows=rows[10:]
c = conn.cursor()
c.execute('''CREATE TABLE calculated_distance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rssi_esp1 FLOAT,
    rssi_esp2 FLOAT,
    rssi_esp3 FLOAT,
    distance_esp1 FLOAT,
    distance_esp2 FLOAT,
    distance_esp3 FLOAT)''')
# distance_esp=[[row[0] for row in rows],[row[1] for row in rows],[row[2] for row in rows]]
rssi_esp=[[row[3] for row in sample_rows],[row[4] for row in sample_rows],[row[5] for row in sample_rows]]

rssi_dict=[{row[3]:row[0] for row in data_rows},{row[4]:row[1] for row in data_rows},{row[5]:row[2] for row in data_rows}]

for rssi in rssi_esp[0]:
    cal_distance= calculate_distance(rssi,rssi_dict[0])
    c.execute("INSERT INTO calculated_distance (rssi_esp1, distance_esp1) VALUES (?, ?)", (rssi, cal_distance))

for rssi in rssi_esp[1]:
    cal_distance= calculate_distance(rssi,rssi_dict[1])
    c.execute("INSERT INTO calculated_distance (rssi_esp2, distance_esp2) VALUES (?, ?)", (rssi, cal_distance))

for rssi in rssi_esp[2]:
    cal_distance= calculate_distance(rssi,rssi_dict[2])
    c.execute("INSERT INTO calculated_distance (rssi_esp3, distance_esp3) VALUES (?, ?)", (rssi, cal_distance))

    
conn.commit()
conn.close()




# # Calculate the distance and RSSI averages between the two rows
# distances_avg = []
# rssis_avg = []
# for i in range(3):
#     # Calculate the average distance and RSSI for each ESP module
#     distance_avg = (rows[0][i] + rows[1][i]) / 2
#     distances_avg.append(distance_avg)
#     rssi_avg = (rows[0][i+3] + rows[1][i+3]) / 2
#     rssis_avg.append(rssi_avg)

# # Calculate the lerp value between the two rows
# fraction = (distances_avg[1] - distances_avg[0]) / (max(distances_avg) - min(distances_avg))
# lerp_value = rssis_avg[0] + (rssis_avg[1] - rssis_avg[0]) * fraction

# # Close the database connection
# conn.close()

# # Print the lerp value
# print(lerp_value)
