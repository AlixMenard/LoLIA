import sqlite3 as sql
import numpy as np

def get_league_season(league, year, seq = False):

    sql_regular = f"SELECT * from {league} WHERE year={year} AND playoff=0"
    sql_po = f"SELECT * from {league} WHERE year={year} AND playoff=1"

    con = sql.connect("matches.db")
    cur = con.cursor()
    cur.execute(sql_regular)
    regular = np.array(cur.fetchall())
    if not seq:
        regular = regular[:,5:]

    cur.execute(sql_po)
    po = np.array(cur.fetchall())
    if not seq:
        po = po[:,5:]

    con.close()

    if seq:
        return sequence(regular, po)

    def smart_convert(x):
        # First convert to float
        num = float(x)
        # If it has no decimal part, convert to int
        if num.is_integer():
            return int(num)
        else:
            return num  # remains as float

    regular = np.vectorize(smart_convert)(regular)
    po = np.vectorize(smart_convert)(po)

    np.random.shuffle(regular)
    np.random.shuffle(po)

    return regular, po

def sequence(*args):
    for list in args:
        games = {}