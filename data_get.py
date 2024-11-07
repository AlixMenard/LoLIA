import sqlite3 as sql
import numpy as np

def get_league_season(league, year):

    sql_regular = f"SELECT * from {league} WHERE year={year} AND playoff=0"
    sql_po = f"SELECT * from {league} WHERE year={year} AND playoff=1"

    con = sql.connect("matches.db")
    cur = con.cursor()
    cur.execute(sql_regular)
    regular = np.array(cur.fetchall())
    regular = regular[:,5:]

    cur.execute(sql_po)
    po = np.array(cur.fetchall())
    po = po[:,5:]

    con.close()

    return regular, po