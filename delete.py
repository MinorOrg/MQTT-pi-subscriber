import sqlite3

conn = sqlite3.connect('mydatabase.db')
cur = conn.cursor()
cur.execute('''DROP TABLE calculated_distance''')
conn.commit()
conn.close()
