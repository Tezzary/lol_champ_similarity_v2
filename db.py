import sqlite3
con = sqlite3.connect("database.db")

cur = con.cursor()

def execute_query(query):
    try:
        res = cur.execute(query)
        con.commit()
        if (res is not None):
            return {"success": True, "data": res.fetchall()}
        return {"success": True, "data": None}
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {"success": False, "data": str(e)}