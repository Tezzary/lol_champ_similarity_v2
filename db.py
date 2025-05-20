import sqlite3
con = sqlite3.connect("database.db")

cur = con.cursor()

def execute_query(query):
    try:
        res = cur.execute(query)
        con.commit()
        if (res is not None):
            return res.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")