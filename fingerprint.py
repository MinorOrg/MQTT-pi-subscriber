import sqlite3
import numpy as np

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

# Retrieve the data for the two variables from the database
data = conn.execute('SELECT distance_from_esp1, rssi_esp1 FROM wifi_data').fetchall()

# Convert the data to a NumPy array
data = np.array(data)

# Calculate the correlation coefficient
corr_coef = np.corrcoef(data[:,0], data[:,1])[0,1]

# Close the database connection
conn.close()

# Print the correlation coefficient
print("Correlation coefficient:", corr_coef)
